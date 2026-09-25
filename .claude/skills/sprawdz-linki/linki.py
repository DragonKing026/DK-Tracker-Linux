#!/usr/bin/env python3
"""Check, repair and move-aware rewrite of relative Markdown links in this repo.

Usage (run from the repository root):
  python3 .claude/skills/sprawdz-linki/linki.py sprawdz            # report broken links
  python3 .claude/skills/sprawdz-linki/linki.py napraw             # fix broken links by unique file name
  python3 .claude/skills/sprawdz-linki/linki.py przenies SRC DST   # git mv + rewrite every affected link
  python3 .claude/skills/sprawdz-linki/linki.py wikilinki          # convert [[wikilinks]] to Markdown links

Links inside fenced code blocks, inline code and HTML comments are ignored, so examples in
skills and templates are never touched. External links (http, mailto) and
pure anchors (#...) are skipped.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote, unquote

ROOT = Path.cwd()
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "build", "build-dir", ".flatpak-builder", ".obsidian"}

LINK = re.compile(r"(!?)\[([^\]\n]*)\]\(([^)\s]+)\)")
WIKI = re.compile(r"(!?)\[\[([^\]\n]+?)\]\]")
FENCE = re.compile(r"^(\s*)(```|~~~)")


def markdown_files() -> list[Path]:
    found = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.endswith(".md"):
                found.append(Path(dirpath) / name)
    return sorted(found)


def all_files() -> list[Path]:
    found = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        found.extend(Path(dirpath) / name for name in filenames)
    return found


def code_mask(text: str) -> list[bool]:
    """True for every character that sits inside a fenced block or inline code."""
    mask = [False] * len(text)
    pos = 0
    in_fence = False
    for line in text.splitlines(keepends=True):
        if FENCE.match(line):
            in_fence = not in_fence
            for i in range(pos, pos + len(line)):
                mask[i] = True
        elif in_fence:
            for i in range(pos, pos + len(line)):
                mask[i] = True
        else:
            for m in re.finditer(r"(`+)(.+?)\1", line):
                for i in range(pos + m.start(), pos + m.end()):
                    mask[i] = True
        pos += len(line)
    for m in re.finditer(r"<!--.*?-->", text, re.S):
        for i in range(m.start(), m.end()):
            mask[i] = True
    return mask


def is_local(target: str) -> bool:
    return not (re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("#"))


def split_target(target: str) -> tuple[str, str]:
    path, _, fragment = target.partition("#")
    return unquote(path), (f"#{fragment}" if fragment else "")


def relative(from_file: Path, to_path: Path) -> str:
    rel = os.path.relpath(to_path, from_file.parent).replace(os.sep, "/")
    return quote(rel, safe="/.-_~()")


def iter_links(text: str):
    mask = code_mask(text)
    for m in LINK.finditer(text):
        if mask[m.start()]:
            continue
        if is_local(m.group(3)):
            yield m


def check() -> int:
    broken = 0
    for md in markdown_files():
        text = md.read_text(encoding="utf-8")
        for m in iter_links(text):
            path, _ = split_target(m.group(3))
            if path and not (md.parent / path).exists():
                line = text.count("\n", 0, m.start()) + 1
                print(f"BRAK  {md.relative_to(ROOT)}:{line}  →  {m.group(3)}")
                broken += 1
        mask = code_mask(text)
        for m in WIKI.finditer(text):
            if not mask[m.start()]:
                line = text.count("\n", 0, m.start()) + 1
                print(f"WIKI  {md.relative_to(ROOT)}:{line}  →  {m.group(0)}  (użyj linku markdown)")
                broken += 1
    print("Wszystkie linki OK." if not broken else f"\nProblemów: {broken}")
    return 1 if broken else 0


def repair() -> int:
    by_name: dict[str, list[Path]] = {}
    for f in all_files():
        by_name.setdefault(f.name, []).append(f)
    unresolved = 0
    for md in markdown_files():
        text = md.read_text(encoding="utf-8")
        changed = False

        def fix(m: re.Match) -> str:
            nonlocal changed, unresolved
            path, fragment = split_target(m.group(3))
            if not path or (md.parent / path).exists():
                return m.group(0)
            candidates = by_name.get(Path(path).name, [])
            if len(candidates) != 1:
                unresolved += 1
                print(f"NIE NAPRAWIONO  {md.relative_to(ROOT)}  →  {m.group(3)}  (kandydaci: {len(candidates)})")
                return m.group(0)
            changed = True
            new = relative(md, candidates[0]) + fragment
            print(f"NAPRAWIONO  {md.relative_to(ROOT)}  {m.group(3)}  →  {new}")
            return f"{m.group(1)}[{m.group(2)}]({new})"

        text = replace_links(text, fix)
        if changed:
            md.write_text(text, encoding="utf-8")
    return 1 if unresolved else 0


def replace_links(text: str, fn) -> str:
    mask = code_mask(text)
    out, last = [], 0
    for m in LINK.finditer(text):
        if mask[m.start()] or not is_local(m.group(3)):
            continue
        out.append(text[last:m.start()])
        out.append(fn(m))
        last = m.end()
    out.append(text[last:])
    return "".join(out)


def move(src: str, dst: str) -> int:
    src_p, dst_p = (ROOT / src).resolve(), (ROOT / dst).resolve()
    if not src_p.exists():
        print(f"Nie istnieje: {src}")
        return 1
    if dst_p.exists() and dst_p.is_dir() and not src_p.is_dir():
        dst_p = dst_p / src_p.name
    moved_files = [src_p] if src_p.is_file() else [p for p in all_files() if src_p in p.resolve().parents]

    def after(path: Path) -> Path:
        path = path.resolve()
        if path == src_p:
            return dst_p
        if src_p in path.parents:
            return dst_p / path.relative_to(src_p)
        return path

    # Read every Markdown file at its current location before anything moves.
    snapshot = {md.resolve(): md.read_text(encoding="utf-8") for md in markdown_files()}
    dst_p.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "mv", str(src_p), str(dst_p)], check=True)

    touched = 0
    for old_md, text in snapshot.items():
        new_md = after(old_md)

        def rewrite(m: re.Match) -> str:
            path, fragment = split_target(m.group(3))
            if not path:
                return m.group(0)
            old_target = (old_md.parent / path).resolve()
            new_target = after(old_target)
            new = relative(new_md, new_target) + fragment
            return m.group(0) if new == m.group(3) else f"{m.group(1)}[{m.group(2)}]({new})"

        new_text = replace_links(text, rewrite)
        if new_text != text:
            new_md.write_text(new_text, encoding="utf-8")
            touched += 1
            print(f"POPRAWIONO LINKI  {new_md.relative_to(ROOT)}")
    print(f"Przeniesiono {src} → {dst_p.relative_to(ROOT)}; plików z poprawionymi linkami: {touched}; "
          f"przeniesionych plików: {len(moved_files)}")
    return check()


def convert_wikilinks() -> int:
    md_by_stem: dict[str, list[Path]] = {}
    for f in all_files():
        md_by_stem.setdefault(f.name, []).append(f)
        if f.suffix == ".md":
            md_by_stem.setdefault(f.stem, []).append(f)
    failed = 0
    for md in markdown_files():
        text = md.read_text(encoding="utf-8")
        mask = code_mask(text)
        out, last, changed = [], 0, False
        for m in WIKI.finditer(text):
            if mask[m.start()]:
                continue
            bang, body = m.group(1), m.group(2).replace("\\|", "|")
            target, _, label = body.partition("|")
            target, _, heading = target.partition("#")
            target = target.strip()
            candidates = [ROOT / target, ROOT / f"{target}.md", md.parent / target, md.parent / f"{target}.md"]
            resolved = next((c for c in candidates if c.is_file()), None)
            if resolved is None:
                found = md_by_stem.get(Path(target).name, [])
                resolved = found[0] if len(found) == 1 else None
            if resolved is None:
                failed += 1
                print(f"NIE PRZEKONWERTOWANO  {md.relative_to(ROOT)}  →  {m.group(0)}")
                continue
            label = (label or heading or resolved.stem).strip()
            new = f"{bang}[{label}]({relative(md, resolved)})"
            out.append(text[last:m.start()])
            out.append(new)
            last = m.end()
            changed = True
        if changed:
            out.append(text[last:])
            md.write_text("".join(out), encoding="utf-8")
            print(f"PRZEKONWERTOWANO  {md.relative_to(ROOT)}")
    return 1 if failed else 0


def main(argv: list[str]) -> int:
    if not argv or argv[0] in {"-h", "--help"}:
        print(__doc__)
        return 0
    command = argv[0]
    if command == "sprawdz":
        return check()
    if command == "napraw":
        code = repair()
        return check() or code
    if command == "przenies" and len(argv) == 3:
        return move(argv[1], argv[2])
    if command == "wikilinki":
        code = convert_wikilinks()
        return check() or code
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
