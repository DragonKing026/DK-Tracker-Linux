"""Gallery of the calendar view (Plan 7): every state in both themes, rendered offscreen."""

import os
import sys
from dataclasses import replace
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, "/mnt/Programowanie/Moje Projekty/Kimai App/src")
sys.path.insert(0, "/mnt/Programowanie/Moje Projekty/Kimai App")

from PySide6.QtCore import QPointF, QSize, Qt  # noqa: E402
from PySide6.QtGui import QMouseEvent  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from dk_tracker.core.i18n import Translator  # noqa: E402
from dk_tracker.core.tracker import Snapshot  # noqa: E402
from dk_tracker.ui.main_window.bridge import MainBridge  # noqa: E402
from dk_tracker.ui.main_window.window import MainWindow  # noqa: E402
from dk_tracker.ui.theme import MAIN_DARK, MAIN_LIGHT  # noqa: E402
from tests.core.fakes import FakeClient, make_entry  # noqa: E402

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "gallery")
OUT.mkdir(parents=True, exist_ok=True)
WARSAW = ZoneInfo("Europe/Warsaw")
NOW = datetime(2026, 9, 25, 12, 40, tzinfo=UTC)  # Friday 14:40 in Warsaw
P = {1: ("Moduł rezerwacji", "#3b82f6"), 2: ("Sklep internetowy", "#22c55e"), 3: ("Administracja", "#a855f7"),
     4: ("Aplikacja mobilna", "#f59e0b"), 5: ("Wsparcie", "#ef4444")}  # fmt: skip


def e(i, day, h, m, minutes, project, text, **extra):
    begin = datetime(2026, 9, day, h, m, tzinfo=WARSAW).astimezone(UTC)
    end = None if minutes is None else begin + timedelta(minutes=minutes)
    name, color = P[project]
    return replace(make_entry(i, begin, end, description=text, project_id=project), project_name=name,
                   project_color=color, activity_name="Programowanie", **extra)  # fmt: skip



def s(i, h, m, sec, secs, project, text, running=False):
    begin = datetime(2026, 9, 25, h, m, sec, tzinfo=WARSAW).astimezone(UTC)
    name, color = P[project]
    return replace(make_entry(i, begin, None if running else begin + timedelta(seconds=secs), description=text,
                   project_id=project), project_name=name, project_color=color, activity_name="Programowanie")

NOW = datetime(2026, 9, 25, 9, 45, 50, tzinfo=UTC)  # 11:45:50
ENTRIES = [
    s(1, 8, 55, 10, 3900 + 30, 1, "Pierwszy 8:55:10–10:00:40"),
    s(2, 10, 0, 40, 15, 3, "Pomyłka 15 s"),
    s(3, 10, 0, 55, 3600 + 45 * 60 - 55 + 20, 2, "Następny od 10:00:55 do 11:45:20"),
    s(4, 11, 45, 30, 0, 4, "Trwający od 11:45:30", running=True),
    s(5, 8, 45, 0, 9 * 60, 5, "Krótki 8:45–8:54"),
    s(6, 8, 55, 0, 3, 5, "3 s o 8:55"),
]
app = QApplication([])
bridge = MainBridge()
t = Translator(os.environ.get("LANG_UI", "pl"))
bridge.render(Snapshot(user=FakeClient().user), configured=True, t=t, now=NOW, tz=WARSAW)
bridge.set_projects(FakeClient().projects_list)
window = MainWindow(bridge)
bridge.show_page("calendar")
page = bridge.calendar


def deliver():
    page.request()
    page.set_entries(page.days[0], page.days[-1], ENTRIES, tz=WARSAW, now=NOW)


def pump(n=20):
    for _ in range(n):
        app.processEvents()


def shot(name, size=QSize(1100, 800)):
    window.window.resize(size)
    window.show()
    pump()
    window.window.grabWindow().save(str(OUT / f"{name}.png"))

deliver()
page.setMode("day")
page.set_entries(page.days[0], page.days[-1], ENTRIES, tz=WARSAW, now=NOW)
pump(40)
shot("sekundy")
