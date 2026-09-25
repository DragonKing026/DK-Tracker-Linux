#!/usr/bin/env python3
"""Keep YAML front matter of every Markdown document consistent.

Every .md file in the repository (outside .claude/, .git/ and build dirs) must
start with front matter holding at least:
  noteId: 32 hex chars   - the VS Code "notebook" extension adds one to any file
                           that lacks it, which leaves the file dirty in git
  tags:   list           - read by Obsidian and by that extension (not "tagi")

Templates (TODO/_szablon) carry the placeholder noteId "{{NOTEID}}", which the
skill creating a task replaces with a fresh id, so copies never share one.

Usage (from the repository root):
  python3 .claude/skills/frontmatter/frontmatter.py sprawdz   # report problems, exit 1 if any
  python3 .claude/skills/frontmatter/frontmatter.py napraw    # add/repair front matter in place
  python3 .claude/skills/frontmatter/frontmatter.py noteid    # print a fresh noteId
"""

from __future__ import annotations

import os
import re
import sys
import uuid
from pathlib import Path

ROOT = Path.cwd()
SKIP_DIRS = {".git", ".claude", "node_modules", ".venv", "venv", "build", "build-dir", ".pytest_cache", ".ruff_cache",
             ".flatpak-builder", ".obsidian"}
FRONT = re.compile(r"\A---\n(.*?\n)?---\n", re.S)
DATE = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}|\{\{DATA\}\}")
NOTE_ID = re.compile(r"^noteId:\s*\"?([0-9a-f]{32}|\{\{NOTEID\}\})\"?\s*$", re.M)


def markdown_files() -> list[Path]:
    found = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        found.extend(Path(dirpath) / n for n in filenames if n.endswith(".md"))
    return sorted(found)


def new_note_id() -> str:
    return uuid.uuid4().hex


def problems(text: str) -> list[str]:
    match = FRONT.match(text)
    if not match:
        return ["brak frontmattera"]
    body = match.group(1) or ""
    found = []
    if not NOTE_ID.search(body):
        found.append("brak noteId")
    for key in ("utworzono", "zaktualizowano", "zamknieto"):
        match = re.search(rf"^{key}:[ \t]*(\S.*)?$", body, re.M)
        if match and match.group(1) and not DATE.fullmatch(match.group(1).strip().strip('"')):
            found.append(f"{key} bez godziny (RRRR-MM-DD GG:MM)")
    if re.search(r"^tagi:", body, re.M):
        found.append("pole 'tagi' zamiast 'tags'")
    elif not re.search(r"^tags:", body, re.M):
        found.append("brak tags")
    return found


def repair(text: str, path: Path) -> str:
    match = FRONT.match(text)
    if not match:
        return f'---\nnoteId: "{new_note_id()}"\ntags: []\n---\n\n{text}'
    body = match.group(1) or ""
    body = re.sub(r"^tagi:", "tags:", body, flags=re.M)
    if not re.search(r"^tags:", body, re.M):
        body += "tags: []\n"
    if not NOTE_ID.search(body):
        placeholder = "{{NOTEID}}" in text or "_szablon" in str(path)
        body = f'noteId: "{"{{NOTEID}}" if placeholder else new_note_id()}"\n' + body
    return f"---\n{body}---\n" + text[match.end():]


def main(argv: list[str]) -> int:
    command = argv[0] if argv else ""
    if command == "noteid":
        print(new_note_id())
        return 0
    if command not in {"sprawdz", "napraw"}:
        print(__doc__)
        return 2
    count = 0
    for md in markdown_files():
        text = md.read_text(encoding="utf-8")
        found = problems(text)
        if not found:
            continue
        count += 1
        rel = md.relative_to(ROOT)
        if command == "napraw":
            md.write_text(repair(text, md), encoding="utf-8")
            print(f"NAPRAWIONO  {rel}  ({', '.join(found)})")
        else:
            print(f"PROBLEM  {rel}  ({', '.join(found)})")
    if command == "sprawdz":
        print("Frontmatter OK." if not count else f"\nPlików z problemami: {count}")
        return 1 if count else 0
    print(f"Naprawiono plików: {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
