"""Screenshots of the main window for the README, the MetaInfo file and the project page.

    .venv/bin/python scripts/zrzuty-okna.py [docs/assets/zrzuty]

Renders the window without a display (offscreen) in the dark theme, with made-up customers,
projects and entries — never real ones. Writes okno-glowne-wpisy.png, okno-glowne-edycja.png (the
edit window over the entries), okno-glowne-podsumowania.png and okno-glowne-kalendarz.png at twice
the window's size, so they stay sharp on the page.
"""

from __future__ import annotations

import os
import random
import sys
from dataclasses import replace
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_SCALE_FACTOR", "2")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from PySide6.QtCore import QSize  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from dk_tracker.core.entry_list import build_rows  # noqa: E402
from dk_tracker.core.i18n import Translator  # noqa: E402
from dk_tracker.core.models import Activity, Entry, EntryDetails, Project, Tag, User  # noqa: E402
from dk_tracker.core.tracker import Snapshot, Totals  # noqa: E402
from dk_tracker.ui.main_window.bridge import MainBridge  # noqa: E402
from dk_tracker.ui.main_window.window import MainWindow  # noqa: E402
from dk_tracker.ui.theme import MAIN_DARK  # noqa: E402

WARSAW = ZoneInfo("Europe/Warsaw")
NOW = datetime(2026, 9, 25, 12, 52, tzinfo=UTC)  # Friday 14:52 in Warsaw
TODAY = date(2026, 9, 25)
SIZE = QSize(1180, 760)
CUSTOMERS = {
    10: ("Hotel Morski", "#2196F3"),
    11: ("Piekarnia Zdrój", "#8bc34a"),
    12: ("Biuro Nowak", "#f44336"),
}
PROJECTS = {  # id: name, colour, customer
    1: ("Moduł rezerwacji", "#3b82f6", 10),
    2: ("Sklep internetowy", "#22c55e", 11),
    3: ("Aplikacja mobilna", "#f59e0b", 10),
    4: ("Wsparcie", "#ef4444", 12),
    5: ("Sprawy wewnętrzne", "#a855f7", 12),
}
ACTIVITIES = {1: ("Programowanie", "#718096"), 2: ("Spotkanie", "#e91e63"), 3: ("Testy", "#009688")}
TEXTS = {
    1: [
        "Formularz rezerwacji — walidacja dat przyjazdu",
        "Kalendarz dostępności pokoi",
        "Poprawki po przeglądzie",
    ],
    2: ["Koszyk i płatności online", "Integracja z kurierem", "Karta produktu — zdjęcia i warianty"],
    3: ["Ekran logowania i odzyskiwanie hasła", "Powiadomienia push", "Poprawki po testach na iOS"],
    4: ["Zgłoszenie #1432 — faktury w PDF", "Aktualizacja serwera", "Kopia zapasowa bazy"],
    5: ["Spotkanie zespołu", "Planowanie sprintu", "Przegląd kodu"],
}


def entry(entry_id: int, begin: datetime, minutes: int | None, project: int, rng: random.Random) -> Entry:
    name, color, customer = PROJECTS[project]
    activity = 2 if project == 5 else rng.choice((1, 1, 3))
    end = None if minutes is None else begin + timedelta(minutes=minutes)
    return Entry(
        id=entry_id,
        begin=begin,
        end=end,
        duration=0 if end is None else minutes * 60,
        description=rng.choice(TEXTS[project]),
        billable=project != 5,
        project_id=project,
        project_name=name,
        project_color=color,
        activity_id=activity,
        activity_name=ACTIVITIES[activity][0],
        user_language="pl",
        customer_id=customer,
        customer_name=CUSTOMERS[customer][0],
        customer_color=CUSTOMERS[customer][1],
        activity_color=ACTIVITIES[activity][1],
    )


def workdays(first: date, last: date) -> list[Entry]:
    """Three to five entries a working day, 8:00 onwards, with gaps; today until the running one."""
    rng = random.Random(3)
    made, number = [], 1
    day = first
    while day <= last:
        if day.weekday() < 5:
            minute = 8 * 60 + rng.choice((0, 15, 30))
            stop = 14 * 60 + 5 if day == TODAY else 16 * 60 + 30
            while minute < stop:
                length = min(rng.choice((45, 60, 90, 120, 150)), stop - minute)
                begin = datetime(day.year, day.month, day.day, minute // 60, minute % 60, tzinfo=WARSAW)
                made.append(
                    entry(number, begin.astimezone(UTC), length, rng.choice((1, 1, 2, 3, 3, 4, 5)), rng)
                )
                number += 1
                minute += length + rng.choice((0, 0, 15, 30))
        day += timedelta(days=1)
    return made


def pump(app: QApplication) -> None:
    for _ in range(30):
        app.processEvents()


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "docs" / "assets" / "zrzuty"
    app = QApplication([])
    user = User(2, "anna", "Anna", "pl", "Europe/Warsaw")
    rng = random.Random(9)
    running = entry(900, datetime(2026, 9, 25, 14, 5, tzinfo=WARSAW).astimezone(UTC), None, 1, rng)
    running = replace(running, description="Formularz rezerwacji — walidacja dat przyjazdu", activity_id=1,
                      activity_name="Programowanie")  # fmt: skip
    finished = workdays(date(2026, 8, 31), TODAY)
    snapshot = Snapshot(
        user=user, running=(running,), totals=Totals(today=5 * 3600 + 20 * 60, week=31 * 3600)
    )
    t = Translator("pl")

    bridge = MainBridge()
    bridge.set_palette(MAIN_DARK)
    bridge.render(snapshot, configured=True, t=t, now=NOW, tz=WARSAW)
    bridge.set_projects([Project(i, n, c, CUSTOMERS[c][0], col, True) for i, (n, col, c) in PROJECTS.items()])
    bridge.set_activities([Activity(i, name, True, None) for i, (name, _) in ACTIVITIES.items()])
    week = [e for e in finished if e.begin >= datetime(2026, 9, 14, tzinfo=WARSAW)]
    bridge.set_entries(
        build_rows(sorted(week, key=lambda e: e.begin, reverse=True), WARSAW, TODAY, 0, t), WARSAW
    )
    window = MainWindow(bridge)
    window.show(SIZE)

    def shot(name: str) -> None:
        window.window.resize(SIZE)
        pump(app)
        window.window.grabWindow().save(str(out / name))

    bridge.show_page("entries")
    shot("okno-glowne-wpisy.png")

    # The edit window of one entry, with tags and a custom field of the server.
    edited = finished[-2]
    bridge.set_tags([Tag("rezerwacje", "#3b82f6"), Tag("walidacja", "#22c55e"), Tag("pilne", "#ef4444")])
    bridge.set_row_activities([Activity(i, name, True, None) for i, (name, _) in ACTIVITIES.items()])
    bridge.open_editor(
        EntryDetails(
            id=edited.id, begin=edited.begin, end=edited.end, project_id=1, activity_id=1,
            description="Formularz rezerwacji — walidacja dat przyjazdu i wyjazdu, komunikaty błędów",
            tags=("rezerwacje", "walidacja"), billable=True, exported=False, break_seconds=0,
            meta=(("Zgłoszenie", "HM-214"),),
        ),
        WARSAW,
    )  # fmt: skip
    shot("okno-glowne-edycja.png")
    bridge.close_editor()

    summary = bridge.summary
    summary.setPeriod("month")
    summary.set_entries(summary.span.first, summary.span.last, [*finished, running], tz=WARSAW, now=NOW,
                        norm=8 * 3600)  # fmt: skip
    bridge.show_page("summary")
    shot("okno-glowne-podsumowania.png")

    calendar = bridge.calendar
    calendar.request()
    calendar.set_entries(calendar.days[0], calendar.days[-1], [*finished, running], tz=WARSAW, now=NOW)
    bridge.show_page("calendar")
    shot("okno-glowne-kalendarz.png")
    window.dispose()
    print(f"saved to {out}")


if __name__ == "__main__":
    main()
