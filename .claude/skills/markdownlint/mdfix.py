#!/usr/bin/env python3
"""markdownlint for this repository: check with the same rules as the VS Code extension, and
fix what can be fixed mechanically.

Usage (from the repository root):
  python3 .claude/skills/markdownlint/mdfix.py sprawdz            # npx markdownlint-cli2 → 0 errors?
  python3 .claude/skills/markdownlint/mdfix.py napraw [PLIK ...]  # tables, line length, then --fix

`napraw` does what markdownlint-cli2 --fix cannot: MD060 (tables in the "compact" style,
`| a | b |` and `| --- | --- |`) and MD013 (prose wrapped at 120 columns, never inside a
link or a code span, never starting a line with a character that changes its meaning).
The remaining fixable rules (MD012, MD022, MD031, MD032, MD050, …) go to `markdownlint-cli2 --fix`.
Rules: .markdownlint.jsonc; files: .markdownlint-cli2.jsonc.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

WIDTH = 120
ROOT = Path.cwd()
SKIP_DIRS = {".venv", "node_modules", ".superpowers", ".pytest_cache", ".ruff_cache", ".git"}
CLI = ["npx", "--yes", "markdownlint-cli2@0.23.2"]  # the version bundled in vscode-markdownlint 0.62.1

_FENCE = re.compile(r"^\s*(```|~~~)")
_QUOTE = re.compile(r"^((?:>\s?)+)")
_LIST = re.compile(r"^(\s*)([-*+]|\d+[.)])(\s+)(\[[ xX]\]\s+)?")
_PROTECTED = re.compile(r"!?\[[^\]]*\]\([^)]*\)|`[^`]*`")
_GLUE = "\x00"
_LONG_CODE = 60  # a longer code span may break between words (Markdown allows it)


def words(text: str) -> list[str]:
    """Whitespace-separated words; spaces inside links and short code spans do not split."""

    def protect(match: re.Match[str]) -> str:
        span = match.group(0)
        if span.startswith("`") and len(span) > _LONG_CODE:
            return span
        return span.replace(" ", _GLUE)

    return [word.replace(_GLUE, " ") for word in _PROTECTED.sub(protect, text).split()]


def risky(word: str) -> bool:
    """Would a line starting with this word become a list item, quote, heading, table or rule?"""
    return bool(
        re.fullmatch(r"[-+*]|\d+[.)]|#{1,6}|=+|-{3,}|_{3,}|\*{3,}", word) or word.startswith((">", "|"))
    )


def markdown_files() -> list[Path]:
    return sorted(
        path for path in ROOT.rglob("*.md") if not SKIP_DIRS & set(path.relative_to(ROOT).parts)
    )


# -- tables (MD060) ------------------------------------------------------------------------


def split_row(row: str) -> list[str]:
    """Cells of `| a | b |`; a pipe inside a code span or escaped with \\ is not a separator."""
    body = row.strip()
    body = body[1:] if body.startswith("|") else body
    body = body[:-1] if body.endswith("|") and not body.endswith("\\|") else body
    cells, current, in_code = [], "", False
    for index, char in enumerate(body):
        if char == "`":
            in_code = not in_code
        if char == "|" and not in_code and (index == 0 or body[index - 1] != "\\"):
            cells.append(current)
            current = ""
            continue
        current += char
    cells.append(current)
    return [cell.strip() for cell in cells]


def format_row(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def format_delimiter(cells: list[str]) -> str:
    out = []
    for cell in cells:
        left, right = cell.startswith(":"), cell.endswith(":")
        out.append((":" if left else "") + "---" + (":" if right else ""))
    return format_row(out)


def is_delimiter(cells: list[str]) -> bool:
    return all(re.fullmatch(r":?-{1,}:?", cell) for cell in cells) and bool(cells)


# -- line length (MD013) ---------------------------------------------------------------------


def prefixes(line: str) -> tuple[str, str, str]:
    """(prefix of the first line, prefix of continuation lines, text)."""
    quote = ""
    match = _QUOTE.match(line)
    if match:
        quote = match.group(1)
        if not quote.endswith(" "):
            quote += " "
        line = line[match.end() :]
    listing = _LIST.match(line)
    if listing:
        marker = listing.group(0)
        return quote + marker, quote + " " * len(marker), line[len(marker) :]
    indent = re.match(r"^\s*", line).group(0)
    return quote + indent, quote + indent, line[len(indent) :]


def wrap_line(line: str, width: int = WIDTH) -> list[str]:
    # An Obsidian callout's first line is its title: breaking it would move words into the body.
    if len(line) <= width or re.match(r"^(>\s?)+\[!\w+\]", line):
        return [line]
    first, rest, text = prefixes(line)
    atoms = words(text)
    if len(atoms) < 2:
        return [line]
    lines: list[str] = []
    current: list[str] = []
    prefix = first
    for atom in atoms:
        if not current or len(prefix) + len(" ".join([*current, atom])) <= width:
            current.append(atom)
            continue
        carried = [atom]
        # A word that would start a list, quote or heading takes the word before it along.
        while risky(carried[0]) and len(current) > 1:
            carried.insert(0, current.pop())
        if risky(carried[0]):
            current.extend(carried)
            continue
        lines.append(prefix + " ".join(current))
        prefix, current = rest, carried
    lines.append(prefix + " ".join(current))
    return lines


# -- file ---------------------------------------------------------------------------------------


def fix_text(text: str) -> str:
    out: list[str] = []
    lines = text.split("\n")
    in_fence = in_front = in_comment = False
    table: list[str] = []

    def flush_table() -> None:
        if not table:
            return
        rows = [split_row(_QUOTE.sub("", row)) for row in table]
        quote = (_QUOTE.match(table[0]) or [""])[0] if _QUOTE.match(table[0]) else ""
        for row, cells in zip(table, rows, strict=True):
            rendered = format_delimiter(cells) if is_delimiter(cells) else format_row(cells)
            out.append(quote + rendered)
        table.clear()

    for number, line in enumerate(lines):
        if number == 0 and line.strip() == "---":
            in_front = True
            out.append(line)
            continue
        if in_front:
            out.append(line)
            in_front = line.strip() != "---"
            continue
        if _FENCE.match(_QUOTE.sub("", line)):
            flush_table()
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        if "<!--" in line and "-->" not in line:
            in_comment = True
        if in_comment:
            out.append(line)
            in_comment = "-->" not in line
            continue
        bare = _QUOTE.sub("", line).strip()
        if bare.startswith("|"):
            table.append(line)
            continue
        flush_table()
        if bare.startswith("#"):
            out.append(line)
            continue
        out.extend(wrap_line(line))
    flush_table()
    return "\n".join(out)


def napraw(paths: list[Path]) -> None:
    changed = 0
    for path in paths:
        text = path.read_text(encoding="utf-8")
        fixed = fix_text(text)
        if fixed != text:
            path.write_text(fixed, encoding="utf-8")
            changed += 1
    print(f"Tabele i długość linii: poprawiono {changed} z {len(paths)} plików.")
    subprocess.run([*CLI, "--fix", *[str(p.relative_to(ROOT)) for p in paths]], check=False,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def sprawdz() -> int:
    result = subprocess.run(CLI, capture_output=True, text=True)
    output = (result.stdout + result.stderr).splitlines()
    errors = [line for line in output if re.search(r":\d+(:\d+)? (error )?MD\d+/", line)]
    for line in errors:
        print(line)
    print("markdownlint OK." if not errors else f"markdownlint: {len(errors)} błędów.")
    return 0 if not errors else 1


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in ("sprawdz", "napraw"):
        sys.exit(__doc__)
    if sys.argv[1] == "sprawdz":
        sys.exit(sprawdz())
    paths = [Path(p).resolve() for p in sys.argv[2:]] or markdown_files()
    napraw(paths)


if __name__ == "__main__":
    main()
