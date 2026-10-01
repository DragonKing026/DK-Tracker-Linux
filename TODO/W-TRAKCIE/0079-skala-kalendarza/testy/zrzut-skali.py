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


ENTRIES = [
    e(1, 21, 8, 0, 120, 1, "Formularz rezerwacji — walidacja dat"),
    e(2, 21, 9, 0, 60, 3, "Spotkanie zespołu"),
    e(3, 21, 10, 30, 150, 2, "Koszyk i płatności"),
    e(4, 21, 22, 0, 180, 5, "Awaria serwera w nocy"),
    e(5, 22, 7, 45, 45, 3, "Poczta"),
    e(6, 22, 9, 0, 240, 4, "Ekran logowania w aplikacji mobilnej — poprawki po testach"),
    e(7, 22, 14, 0, 90, 1, "Kalendarz dostępności pokoi"),
    e(8, 23, 8, 0, 480, 2, "Integracja z płatnościami"),
    e(9, 24, 9, 0, 30, 5, "Zgłoszenie #1432", exported=True),
    e(10, 24, 9, 15, 120, 1, "Przegląd kodu"),
    e(11, 24, 9, 30, 60, 3, "Rozmowa z klientem"),
    e(12, 24, 13, 0, 180, 4, "Powiadomienia push"),
    e(13, 25, 8, 30, 150, 2, "Raport sprzedaży"),
    e(14, 25, 12, 0, None, 1, "Formularz rezerwacji — testy"),
    e(15, 26, 10, 0, 120, 5, "Dyżur weekendowy"),
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



from PySide6.QtGui import QWheelEvent
from PySide6.QtCore import QPoint
deliver()
pump(40)
shot("skala-domyslna", QSize(1400, 800))
def wheel(x, y, notches, ctrl=True):
    pos = QPointF(x, y)
    ev = QWheelEvent(pos, window.window.mapToGlobal(pos), QPoint(0, 0), QPoint(0, 120 * notches),
                     Qt.MouseButton.NoButton, Qt.KeyboardModifier.ControlModifier if ctrl else Qt.KeyboardModifier.NoModifier,
                     Qt.ScrollPhase.NoScrollPhase, False)
    QApplication.sendEvent(window.window, ev)
    pump(10)
wheel(700, 500, 2)
shot("po-przyblizeniu", QSize(1400, 800))
print("hour height", page.hourHeight)
wheel(700, 500, -4)
shot("po-oddaleniu", QSize(1400, 800))
print("hour height", page.hourHeight)
