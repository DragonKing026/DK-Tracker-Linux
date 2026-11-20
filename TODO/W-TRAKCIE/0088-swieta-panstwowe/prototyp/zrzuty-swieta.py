"""Zrzuty do zadania 0088 (święta państwowe): Ustawienia, Kalendarz i Podsumowania w obu motywach.

    .venv/bin/python TODO/W-TRAKCIE/0088-swieta-panstwowe/prototyp/zrzuty-swieta.py [katalog]

Okno bez ekranu (offscreen), dane zmyślone, święta wpisane z ręki (bez sieci): Polska, tydzień z środą
2026-11-11 (Narodowe Święto Niepodległości). Korzysta z danych i funkcji `scripts/zrzuty-okna.py`.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from datetime import UTC, date, datetime
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_SCALE_FACTOR", "1")
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "src"))

from PySide6.QtCore import QSize  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

spec = importlib.util.spec_from_file_location("zrzuty_okna", ROOT / "scripts" / "zrzuty-okna.py")
base = importlib.util.module_from_spec(spec)
sys.modules["zrzuty_okna"] = base
spec.loader.exec_module(base)

from dk_tracker.core.entry_list import build_rows  # noqa: E402
from dk_tracker.core.holidays import Holiday, HolidayData  # noqa: E402
from dk_tracker.core.i18n import Translator  # noqa: E402
from dk_tracker.core.models import Activity, Project, User  # noqa: E402
from dk_tracker.core.settings import Settings  # noqa: E402
from dk_tracker.core.tracker import Snapshot, Totals  # noqa: E402
from dk_tracker.ui.main_window.bridge import MainBridge  # noqa: E402
from dk_tracker.ui.main_window.window import MainWindow  # noqa: E402
from dk_tracker.ui.theme import MAIN_DARK, MAIN_LIGHT  # noqa: E402

TODAY = date(2026, 11, 12)  # Thursday
HOLIDAY = date(2026, 11, 11)
NOW = datetime(2026, 11, 12, 11, 0, tzinfo=UTC)  # 12:00 in Warsaw
WARSAW = base.WARSAW
base.TODAY = TODAY  # workdays() ends the current day at 14:05
DATA = HolidayData(
    "PL",
    "2026-11-12 11:58",
    (
        Holiday(date(2026, 11, 1), "Wszystkich Świętych", "All Saints' Day"),
        Holiday(HOLIDAY, "Narodowe Święto Niepodległości", "Independence Day"),
        Holiday(date(2026, 12, 25), "Boże Narodzenie (pierwszy dzień)", "Christmas Day"),
    ),
)


def pump(app: QApplication) -> None:
    for _ in range(30):
        app.processEvents()


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "zrzuty"
    out.mkdir(parents=True, exist_ok=True)
    app = QApplication([])
    t = Translator("pl")
    user = User(2, "anna", "Anna", "pl", "Europe/Warsaw")
    rng = base.random.Random(9)
    running = base.entry(900, datetime(2026, 11, 12, 11, 5, tzinfo=UTC), None, 1, rng)
    finished = [
        e for e in base.workdays(date(2026, 11, 2), TODAY) if e.begin.astimezone(WARSAW).date() != HOLIDAY
    ]
    snapshot = Snapshot(user=user, running=(running,), totals=Totals(today=3 * 3600, week=16 * 3600))

    bridge = MainBridge()
    bridge.set_palette(MAIN_DARK)
    bridge.render(snapshot, configured=True, t=t, now=NOW, tz=WARSAW)
    bridge.set_projects(
        [Project(i, n, c, base.CUSTOMERS[c][0], col, True) for i, (n, col, c) in base.PROJECTS.items()]
    )
    bridge.set_activities([Activity(i, n, True, None) for i, (n, _) in base.ACTIVITIES.items()])
    bridge.set_entries(
        build_rows(sorted(finished, key=lambda e: e.begin, reverse=True), WARSAW, TODAY, 0, t), WARSAW
    )
    bridge.set_holidays(DATA, "PL")
    window = MainWindow(bridge)
    window.show(base.SIZE)

    def shot(name: str, size: QSize = base.SIZE) -> None:
        window.window.resize(size)
        pump(app)
        window.window.grabWindow().save(str(out / name))

    form = bridge.settings_form
    form.retranslate(t)
    for theme, palette in (("ciemny", MAIN_DARK), ("jasny", MAIN_LIGHT)):
        bridge.set_palette(palette)
        tall = QSize(1180, 900)
        form.load(Settings(url="https://kimai.firma.pl", language="pl", holiday_country="PL"), has_token=True)
        form.show_holiday_status("Zsynchronizowano 2026-11-12 11:58", ok=True, busy=False)
        bridge.show_page("settings")
        shot(f"ustawienia-swieta-ok-{theme}.png", tall)
        form.show_holiday_status(
            "Nie udało się pobrać świąt: brak połączenia z date.nager.at", ok=False, busy=False
        )
        shot(f"ustawienia-swieta-blad-{theme}.png", tall)

        calendar = bridge.calendar
        calendar.request()
        calendar.set_entries(calendar.days[0], calendar.days[-1], [*finished, running], tz=WARSAW, now=NOW)
        bridge.show_page("calendar")
        shot(f"kalendarz-swieta-{theme}.png")

        summary = bridge.summary
        summary.request()
        summary.set_entries(
            summary.span.first, summary.span.last, [*finished, running], tz=WARSAW, now=NOW, norm=8 * 3600
        )
        bridge.show_page("summary")
        shot(f"podsumowania-swieta-{theme}.png")

        # Zakres: kalendarzyk wyboru daty z zaznaczonym świętem (11 listopada).
        summary.setPeriod("range")
        summary.set_entries(
            summary.span.first, summary.span.last, [*finished, running], tz=WARSAW, now=NOW, norm=8 * 3600
        )
        pump(app)
        field = window.child("summaryRangeFirst")
        field.clicked.emit()
        pump(app)
        shot(f"kalendarzyk-swieta-{theme}.png")
        summary.setPeriod("week")
    window.dispose()
    print(f"zapisano w {out}")


if __name__ == "__main__":
    main()
