#!/usr/bin/env python3
"""TODO task bookkeeping: status changes, folder moves and the board, driven by front matter.

Usage (from the repository root):
  python3 .claude/skills/zmien-status-zadania/zadanie.py status NNNN <status> [--wpis "tekst"]
  python3 .claude/skills/zmien-status-zadania/zadanie.py tablica
  python3 .claude/skills/zmien-status-zadania/zadanie.py numer        # next free task number

Statuses and folders:
  pomysl, do-zrobienia      -> TODO/DO-ZROBIENIA/
  w-trakcie, zablokowane    -> TODO/W-TRAKCIE/
  zrobione, porzucone       -> TODO/ZROBIONE/

The board (TODO/README.md) is regenerated between the markers
<!-- tablica:start --> and <!-- tablica:end --> from each task's front matter
(numer, tytul, status, priorytet, zalezy_od, zamknieto). Folders are moved with
linki.py, so every link to and inside the task is fixed.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
TODO = ROOT / "TODO"
LINKI = ROOT / ".claude" / "skills" / "sprawdz-linki" / "linki.py"
FOLDER = {
    "pomysl": "DO-ZROBIENIA",
    "do-zrobienia": "DO-ZROBIENIA",
    "w-trakcie": "W-TRAKCIE",
    "zablokowane": "W-TRAKCIE",
    "zrobione": "ZROBIONE",
    "porzucone": "ZROBIONE",
}
EMOJI = {
    "pomysl": "💡",
    "do-zrobienia": "📋",
    "w-trakcie": "🔨",
    "zablokowane": "⛔",
    "zrobione": "✅",
    "porzucone": "🗑️",
}
START, END = "<!-- tablica:start -->", "<!-- tablica:end -->"


def today() -> str:
    return dt.date.today().isoformat()


def task_files() -> list[Path]:
    return sorted(
        path
        for folder in sorted(set(FOLDER.values()))
        for path in (TODO / folder).glob("[0-9][0-9][0-9][0-9]-*/todo.md")
    )


def front(text: str) -> dict[str, str]:
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    data: dict[str, str] = {}
    for line in (match.group(1) if match else "").splitlines():
        key, sep, value = line.partition(":")
        if sep and not line.startswith(" "):
            data[key.strip()] = value.strip().strip('"')
    return data


def set_field(text: str, key: str, value: str) -> str:
    head_end = text.index("\n---\n", 4)
    head, rest = text[:head_end], text[head_end:]
    pattern = re.compile(rf"^{re.escape(key)}:.*$", re.M)
    line = f"{key}: {value}"
    head = pattern.sub(line, head) if pattern.search(head) else head + "\n" + line
    return head + rest


def find(number: str) -> Path:
    matches = [path for path in task_files() if path.parent.name.startswith(f"{number}-")]
    if len(matches) != 1:
        sys.exit(f"Nie znaleziono jednoznacznie zadania {number} (znaleziono {len(matches)}).")
    return matches[0]


def add_log(text: str, entry: str) -> str:
    heading = f"### {today()}"
    marker = "\n## Dziennik\n"
    if marker not in text:
        return text + f"\n## Dziennik\n\n{heading}\n- {entry}\n"
    start = text.index(marker) + len(marker)
    next_section = text.find("\n## ", start)
    section_end = len(text) if next_section == -1 else next_section
    section = text[start:section_end]
    if heading in section:
        section = section.rstrip("\n") + f"\n- {entry}\n"
    else:
        section = section.rstrip("\n") + f"\n\n{heading}\n- {entry}\n"
    return text[:start] + section + text[section_end:]


def change_status(number: str, status: str, entry: str | None) -> None:
    if status not in FOLDER:
        sys.exit(f"Nieznany status: {status}. Dozwolone: {', '.join(FOLDER)}")
    path = find(number)
    text = path.read_text(encoding="utf-8")
    old = front(text).get("status", "")
    text = set_field(text, "status", status)
    text = set_field(text, "zaktualizowano", today())
    if FOLDER[status] == "ZROBIONE":
        text = set_field(text, "zamknieto", today())
    text = re.sub(r"(> \*\*)[^*]+(\*\* · priorytet)", rf"\g<1>{status}\g<2>", text, count=1)
    text = add_log(text, entry or f"Status: {old} → {status}.")
    path.write_text(text, encoding="utf-8")

    target = TODO / FOLDER[status] / path.parent.name
    if target != path.parent:
        subprocess.run(
            [sys.executable, str(LINKI), "przenies", str(path.parent.relative_to(ROOT)), str(target.relative_to(ROOT))],
            check=True,
        )
    rebuild_board()
    print(f"{number}: {old} → {status} ({FOLDER[status]}/)")


def rebuild_board() -> None:
    board = TODO / "README.md"
    text = board.read_text(encoding="utf-8")
    if START not in text or END not in text:
        sys.exit(f"Brak znaczników {START} / {END} w {board}.")
    tasks = []
    for path in task_files():
        data = front(path.read_text(encoding="utf-8"))
        tasks.append((data.get("numer", path.parent.name[:4]), path, data))
    by_number = {number: path for number, path, _ in tasks}

    def link(path: Path, label: str) -> str:
        return f"[{label}]({path.relative_to(TODO).as_posix()})"

    def deps(data: dict[str, str]) -> str:
        found = re.findall(r"(\d{4})", data.get("zalezy_od", ""))
        if not found:
            return "—"
        parts = []
        for number in found:
            path = by_number.get(number)
            if path is None:
                parts.append(number)
                continue
            done = " ✅" if path.parent.parent.name == "ZROBIONE" else ""
            parts.append(link(path, number) + done)
        return ", ".join(parts)

    def rows(folder: str, closed: bool) -> list[str]:
        selected = [(n, p, d) for n, p, d in tasks if p.parent.parent.name == folder]
        if closed:
            lines = ["| Nr | Zadanie | Status | Zamknięto |", "|---|---|---|---|"]
            lines += [
                f"| {n} | {link(p, d.get('tytul', p.parent.name))} | {EMOJI.get(d.get('status', ''), '')} "
                f"{d.get('status', '')} | {d.get('zamknieto', '')} |"
                for n, p, d in selected
            ]
        else:
            lines = ["| Nr | Zadanie | Status | Priorytet | Zależy od |", "|---|---|---|---|---|"]
            lines += [
                f"| {n} | {link(p, d.get('tytul', p.parent.name))} | {EMOJI.get(d.get('status', ''), '')} "
                f"{d.get('status', '')} | {d.get('priorytet', '')} | {deps(d)} |"
                for n, p, d in selected
            ]
        return lines

    generated = "\n".join(
        [START, "", "## W trakcie", "", *rows("W-TRAKCIE", False), "", "## Do zrobienia", "",
         *rows("DO-ZROBIENIA", False), "", "## Zrobione", "", *rows("ZROBIONE", True), "", END]
    )
    head, _, tail = text.partition(START)
    _, _, tail = tail.partition(END)
    board.write_text(set_field(head, "zaktualizowano", today()) + generated + tail, encoding="utf-8")


def next_number() -> str:
    numbers = [int(path.parent.name[:4]) for path in task_files()]
    return f"{max(numbers, default=0) + 1:04d}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    status = sub.add_parser("status")
    status.add_argument("numer")
    status.add_argument("status")
    status.add_argument("--wpis")
    sub.add_parser("tablica")
    sub.add_parser("numer")
    args = parser.parse_args()
    if args.command == "status":
        change_status(args.numer, args.status, args.wpis)
    elif args.command == "tablica":
        rebuild_board()
    else:
        print(next_number())


if __name__ == "__main__":
    main()
