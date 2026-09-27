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


def mouse(kind, item_name, x, y, buttons=Qt.MouseButton.LeftButton):
    item = window.window.findChild(object, item_name)
    point = item.mapToScene(QPointF(x, y))
    types = {"press": QMouseEvent.Type.MouseButtonPress, "move": QMouseEvent.Type.MouseMove,
             "release": QMouseEvent.Type.MouseButtonRelease}  # fmt: skip
    event = QMouseEvent(types[kind], point, point, Qt.MouseButton.LeftButton if kind != "move" else Qt.MouseButton.NoButton,
                        buttons, Qt.KeyboardModifier.NoModifier)  # fmt: skip
    QApplication.sendEvent(window.window, event)
    pump(5)


def grid_point(day, minutes):
    grid = window.window.findChild(object, "calendarGhost").parentItem()
    width = (grid.width() - 56) / len(page.days)
    return 56 + (day + 0.5) * width, minutes * 48 / 60


for theme, palette in (("ciemny", MAIN_DARK), ("jasny", MAIN_LIGHT)):
    bridge.set_palette(palette)
    page.setMode("week")
    page.setWorkweek(False)
    page.today()
    deliver()
    window.show()
    pump()
    view = window.child("calendarView")
    view.setProperty("scrolled", False)
    view.scrollToWork() if hasattr(view, "scrollToWork") else None
    shot(f"{theme}-tydzien")
    # a new entry dragged out on Wednesday afternoon
    x, y = grid_point(2, 16 * 60)
    grid = window.window.findChild(object, "calendarGhost").parentItem()
    point = grid.mapToScene(QPointF(x, y))
    for kind, dy in (("press", 0), ("move", 30), ("move", 90)):
        p = QPointF(point.x(), point.y() + dy)
        ev = QMouseEvent({"press": QMouseEvent.Type.MouseButtonPress, "move": QMouseEvent.Type.MouseMove}[kind], p, p,
                         Qt.MouseButton.LeftButton if kind == "press" else Qt.MouseButton.NoButton,
                         Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)  # fmt: skip
        QApplication.sendEvent(window.window, ev)
        pump(5)
    shot(f"{theme}-przeciaganie-nowego")
    p = QPointF(point.x(), point.y() + 90)
    QApplication.sendEvent(window.window, QMouseEvent(QMouseEvent.Type.MouseButtonRelease, p, p, Qt.MouseButton.LeftButton,
                                                      Qt.MouseButton.NoButton, Qt.KeyboardModifier.NoModifier))  # fmt: skip
    pump()
    shot(f"{theme}-dymek-nowego")
    window.window.findChild(object, "calendarPopup").close()
    pump()
    # a click on Monday's first block
    x, y = grid_point(1, 10 * 60)
    p = grid.mapToScene(QPointF(x - 30, y))
    for kind in (QMouseEvent.Type.MouseButtonPress, QMouseEvent.Type.MouseButtonRelease):
        QApplication.sendEvent(window.window, QMouseEvent(kind, p, p, Qt.MouseButton.LeftButton,
                                                          Qt.MouseButton.LeftButton if kind == QMouseEvent.Type.MouseButtonPress else Qt.MouseButton.NoButton,
                                                          Qt.KeyboardModifier.NoModifier))  # fmt: skip
        pump(5)
    shot(f"{theme}-dymek-wpisu")
    window.window.findChild(object, "calendarPopup").close()
    pump()
    page.setWorkweek(True)
    deliver()
    shot(f"{theme}-5-dni")
    page.setMode("day")
    deliver()
    shot(f"{theme}-dzien")
    page.setMode("week")
    page.setWorkweek(False)
    deliver()
    shot(f"{theme}-800", QSize(800, 560))
window.dispose()
print("saved to", OUT)
