"""0090: short entries keep a line for their title; the scale goes no further out than they allow."""

import os
import sys
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from PySide6.QtCore import QSize  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from dk_tracker.core.i18n import Translator  # noqa: E402
from dk_tracker.core.tracker import Snapshot  # noqa: E402
from dk_tracker.ui.main_window.bridge import MainBridge  # noqa: E402
from dk_tracker.ui.main_window.window import MainWindow  # noqa: E402
from tests.core.fakes import FakeClient, make_entry  # noqa: E402
from tests.ui.main_window.test_window import visual_child  # noqa: E402

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
OUT.mkdir(parents=True, exist_ok=True)
WARSAW = ZoneInfo("Europe/Warsaw")
NOW = datetime(2026, 9, 25, 18, 0, tzinfo=UTC)  # Friday 20:00 in Warsaw
P = {1: ("Moduł rezerwacji", "#6b8e23"), 2: ("Sklep internetowy", "#22c55e"), 3: ("Wsparcie", "#ef4444")}


def e(i, h, m, minutes, project, text):
    begin = datetime(2026, 9, 25, h, m, tzinfo=WARSAW).astimezone(UTC)
    name, color = P[project]
    made = make_entry(i, begin, begin + timedelta(minutes=minutes), description=text, project_id=project)
    return replace(made, project_name=name, project_color=color, activity_name="Development")


SHORT = [  # all shorter than ~3 minutes: they do not hold the scale back
    e(1, 9, 0, 1, 3, "Minuta 9:00–9:01"),
    e(2, 9, 5, 115, 1, "Następny od 9:05 do 11:00"),
    e(3, 12, 0, 2, 2, "Łańcuch: pierwszy (2 min)"),
    e(4, 12, 3, 2, 3, "Łańcuch: drugi (2 min)"),
    e(5, 12, 6, 2, 2, "Łańcuch: trzeci (2 min)"),
    e(6, 12, 9, 90, 1, "Długi po łańcuchu"),
    e(7, 17, 30, 1, 3, "Samotny krótki o 17:30"),
]
TEN = [*SHORT, e(8, 15, 0, 10, 2, "Dziesięć minut: skala co najmniej 120 px")]

app = QApplication([])
bridge = MainBridge()
bridge.render(Snapshot(user=FakeClient().user), configured=True, t=Translator("pl"), now=NOW, tz=WARSAW)
bridge.set_projects(FakeClient().projects_list)
window = MainWindow(bridge)
bridge.show_page("calendar")
page = bridge.calendar
page.setMode("day")


def shot(name, entries, height):
    page.set_hour_height(height)
    page.request()
    page.set_entries(page.days[0], page.days[-1], entries, tz=WARSAW, now=NOW)
    window.window.resize(QSize(900, 820))
    window.show()
    for _ in range(40):
        app.processEvents()
    grid = visual_child(window.window.contentItem(), "calendarGrid")
    grid.setProperty("contentY", 8.5 * page.hourHeight)  # from 8:30
    for _ in range(10):
        app.processEvents()
    window.window.grabWindow().save(str(OUT / f"{name}.png"))
    print(name, "skala", page.hourHeight)


shot("po-najdalej-krotkie", SHORT, 32)
shot("po-najdalej-z-10-min", TEN, 32)
shot("po-96-px", SHORT, 96)
