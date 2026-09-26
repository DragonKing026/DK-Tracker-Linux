"""The screenshot for README and Discover: the quick window, dark theme, made-up data only."""
import sys
from dataclasses import replace
from datetime import timedelta
sys.path.insert(0, ".")
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QApplication
app = QApplication([])
app.styleHints().setColorScheme(Qt.ColorScheme.Dark)
from dk_tracker.core.i18n import Translator
from dk_tracker.core.settings import Settings
from dk_tracker.core.models import Activity
from dk_tracker.core.tracker import Snapshot, Totals
import dk_tracker.ui.popup as popup_module
from dk_tracker.ui.theme import palette_for
popup_module.palette_for = lambda _scheme, window: palette_for(Qt.ColorScheme.Dark, window)
from dk_tracker.ui.popup import QuickWindow
from dk_tracker.ui.state import AppState
from tests.core.fakes import NOW, FakeClient, make_entry
c = FakeClient()
H = timedelta(hours=1)
running = make_entry(1, NOW - timedelta(minutes=47), description="Formularz rezerwacji — walidacja dat przyjazdu")
recent = (
    make_entry(2, NOW - 4 * H, NOW - 2.5 * H, description="Kalendarz dostępności pokoi: poprawki po przeglądzie z recepcją, w tym obsługa pokoi łączonych i blokad na remont"),
    make_entry(3, NOW - 6 * H, NOW - 5 * H, description="Spotkanie z klientem — zakres drugiego etapu", activity_id=2),
    replace(make_entry(4, NOW - 26 * H, NOW - 23.5 * H, description="Integracja płatności online, testy zwrotów", billable=False), project_name="Integracja z KSeF", project_color="#008080"),
    make_entry(5, NOW - 29 * H, NOW - 27 * H, description="Formularz rezerwacji — komunikaty błędów"),
)
recent = tuple(replace(e, activity_name="Spotkanie") if e.activity_id == 2 else e for e in recent)
snap = Snapshot(user=c.user, running=(running,), recent=recent, totals=Totals(today=6 * 3600 + 13 * 60, week=31 * 3600 + 40 * 60), projects=tuple(c.projects_list), non_billable_customers=frozenset({20}))
state = AppState(Settings(url="https://kimai.example.com"), Translator("pl"))
w = QuickWindow(state, now=lambda: NOW)
w.form.set_catalog(snap, remembered_project=1)
w.form.set_activities([Activity(1, "Programowanie", True, None), Activity(2, "Spotkanie", True, None)], 1)
state.update(configured=True, snapshot=snap)
w.set_preferred_size(QSize(480, 640)); w.show()
for _ in range(5): app.processEvents()
w.grab().save(sys.argv[1])
