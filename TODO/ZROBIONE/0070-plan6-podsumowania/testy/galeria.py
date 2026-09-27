"""Gallery of the summary view (Plan 6): every state in both themes, rendered offscreen."""

import os
import random
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
NOW = datetime(2026, 9, 25, 16, 0, tzinfo=UTC)
PROJECTS = [
    (1, "Moduł rezerwacji", "#3b82f6", 10, "Hotel Morski", "#2196F3"),
    (2, "Sklep internetowy", "#22c55e", 11, "Piekarnia Zdrój", "#8bc34a"),
    (3, "Administracja", "#a855f7", 20, "Sprawy wewnętrzne", "#9c27b0"),
    (4, "Aplikacja mobilna — bardzo długa nazwa projektu", "#f59e0b", 10, "Hotel Morski", "#2196F3"),
    (5, "Wsparcie", "#ef4444", 12, "Biuro Rachunkowe Nowak", "#f44336"),
]
ACTIVITIES = [(1, "Programowanie", "#718096"), (2, "Spotkanie", "#e91e63"), (3, "Testy", "#009688")]


def make(entries_days: int, seed: int):
    rng = random.Random(seed)
    made, n = [], 1
    start = date(2026, 9, 25) - timedelta(days=entries_days)
    for offset in range(entries_days + 1):
        day = start + timedelta(days=offset)
        if day.weekday() >= 5 and rng.random() < 0.85:
            continue
        hour = 8
        for _ in range(rng.randint(2, 4)):
            p = rng.choice(PROJECTS)
            a = rng.choice(ACTIVITIES)
            minutes = rng.choice([30, 45, 60, 90, 120, 150, 180])
            begin = datetime(day.year, day.month, day.day, hour, tzinfo=WARSAW).astimezone(UTC)
            end = begin + timedelta(minutes=minutes)
            if end > NOW:
                continue
            made.append(
                replace(
                    make_entry(n, begin, end, billable=p[0] != 3 and rng.random() > 0.1, project_id=p[0],
                               activity_id=a[0]),
                    project_name=p[1], project_color=p[2], customer_id=p[3], customer_name=p[4],
                    customer_color=p[5], activity_name=a[1], activity_color=a[2],
                )
            )
            n += 1
            hour += minutes // 60 + 1
    return made


ALL = make(400, 7)
app = QApplication([])
bridge = MainBridge()
client = FakeClient()
t = Translator(os.environ.get("LANG_UI", "pl"))
bridge.render(Snapshot(user=client.user), configured=True, t=t, now=NOW, tz=WARSAW)
window = MainWindow(bridge)
bridge.show_page("summary")


def deliver(norm=8 * 3600, entries=None):
    page = bridge.summary
    page.request()
    page.set_entries(page.span.first, page.span.last, ALL if entries is None else entries, tz=WARSAW, now=NOW,
                     norm=norm)


def shot(name, size=QSize(1100, 900)):
    window.window.resize(size)
    window.show()
    for _ in range(20):
        app.processEvents()
    image = window.window.grabWindow()
    image.save(str(OUT / f"{name}.png"))


def hover_bar(index):
    chart = window.window.findChild(object, "barChart")
    from PySide6.QtQuick import QQuickItem  # noqa: F401

    bars = chart.property("bars")
    slot = chart.property("slot")
    x = chart.property("plotX") + (index + 0.5) * slot
    point = chart.mapToScene(QPointF(x, chart.height() - 60))
    event = QMouseEvent(QMouseEvent.Type.MouseMove, point, point, Qt.MouseButton.NoButton,
                        Qt.MouseButton.NoButton, Qt.KeyboardModifier.NoModifier)
    QApplication.sendEvent(window.window, event)
    for _ in range(10):
        app.processEvents()
    return len(bars)


for theme, palette in (("ciemny", MAIN_DARK), ("jasny", MAIN_LIGHT)):
    bridge.set_palette(palette)
    page = bridge.summary
    page.setPeriod("week")
    page.today()
    deliver()
    shot(f"{theme}-tydzien")
    hover_bar(1)
    shot(f"{theme}-tydzien-dymek")
    page.setPeriod("month")
    deliver()
    shot(f"{theme}-miesiac")
    page.setGroup("customer")
    shot(f"{theme}-miesiac-klient")
    page.setGroup("project")
    page.setPeriod("year")
    deliver()
    shot(f"{theme}-rok")
    hover_bar(8)
    shot(f"{theme}-rok-dymek")
    page.setRange("2026-07-20", "2026-09-25")
    deliver()
    shot(f"{theme}-zakres")
    page.setPeriod("week")
    page.step(-60)
    deliver(entries=[])
    shot(f"{theme}-pusty")
    page.today()
    shot(f"{theme}-wczytywanie")
    deliver(norm=0)
    shot(f"{theme}-800", QSize(800, 560))
window.dispose()
print("saved to", OUT)
