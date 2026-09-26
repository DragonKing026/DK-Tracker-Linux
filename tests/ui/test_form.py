from dataclasses import replace
from datetime import timedelta
from zoneinfo import ZoneInfo

import pytest
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QFocusEvent
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication

from kimai_tray.core.i18n import Translator
from kimai_tray.core.models import Activity
from kimai_tray.core.tracker import Snapshot
from kimai_tray.ui.form import TrackerForm

from ..core.fakes import NOW, FakeClient, make_entry

WARSAW = ZoneInfo("Europe/Warsaw")
CLIENT = FakeClient()
CATALOG = Snapshot(
    user=CLIENT.user,
    projects=tuple(CLIENT.projects_list),
    non_billable_customers=frozenset({20}),
)
ACTIVITIES = [Activity(1, "Programowanie", True, None), Activity(2, "Spotkanie", True, None)]
RUNNING = make_entry(7, NOW - timedelta(minutes=82), description="Formularz rezerwacji pokoi")


@pytest.fixture
def form(qtbot):
    widget = TrackerForm(Translator("pl"))
    widget.save_delay_ms = 30
    qtbot.addWidget(widget)
    widget.set_catalog(CATALOG, remembered_project=1)
    widget.set_activities(ACTIVITIES, remembered_activity=1)
    widget.render(CATALOG, WARSAW, NOW)
    return widget


def press(widget, key, modifiers=Qt.KeyboardModifier.NoModifier):
    from PySide6.QtTest import QTest

    QTest.keyClick(widget, key, modifiers)


def test_enter_starts_with_the_chosen_project_and_activity(form, qtbot):
    form.description.setPlainText("Walidacja dat przyjazdu")
    with qtbot.waitSignal(form.startRequested) as signal:
        press(form.description, Qt.Key.Key_Return)
    assert signal.args[0] == {
        "project_id": 1,
        "activity_id": 1,
        "description": "Walidacja dat przyjazdu",
        "billable": None,  # an untouched switch is not sent (F-09)
    }


def test_shift_enter_adds_a_line(form, qtbot):
    form.description.setPlainText("a")
    with qtbot.assertNotEmitted(form.startRequested):
        press(form.description, Qt.Key.Key_Return, Qt.KeyboardModifier.ShiftModifier)
    assert "\n" in form.description.toPlainText()


def test_touched_billable_is_sent(form, qtbot):
    form.billable.click()
    with qtbot.waitSignal(form.startRequested) as signal:
        form.toggle.click()
    assert signal.args[0]["billable"] is False


def test_project_of_a_non_billable_customer_defaults_to_non_billable(form, qtbot):
    with qtbot.waitSignal(form.projectChosen) as signal:
        form.select_project(2)
    assert signal.args == [2]
    assert form.billable_value is False
    assert form.billable.property("on") == "false"


def test_customer_headers_cannot_be_chosen(form):
    model = form.project.model()
    headers = [row for row in range(model.rowCount()) if form.project.itemData(row) is None and row > 0]
    assert headers
    assert all(not model.item(row).isEnabled() for row in headers)


def test_running_entry_locks_pickers_and_shows_times(form):
    form.render(replace(CATALOG, running=(RUNNING,)), WARSAW, NOW)
    assert not form.project.isEnabled() and not form.activity.isEnabled()
    assert form.toggle.property("state") == "stop"
    assert not form.times.isHidden()
    assert form.begin.text() == "16:42"  # 14:42 UTC in Warsaw
    assert form.clock.text() == "1:22:00"
    assert form.description.toPlainText() == "Formularz rezerwacji pokoi"


def test_stop_sends_the_typed_end(form, qtbot):
    form.render(replace(CATALOG, running=(RUNNING,)), WARSAW, NOW)
    form.end.setText("17:30")
    with qtbot.waitSignal(form.stopRequested) as signal:
        form.toggle.click()
    assert signal.args == ["17:30"]


def test_typing_saves_quietly_after_a_pause(form, qtbot):
    form.render(replace(CATALOG, running=(RUNNING,)), WARSAW, NOW)
    with qtbot.waitSignal(form.descriptionCommitted) as signal:
        form.description.setPlainText("Formularz rezerwacji — walidacja")
    assert signal.args == ["Formularz rezerwacji — walidacja", True]


def test_leaving_the_field_saves_loudly(form, qtbot):
    form.render(replace(CATALOG, running=(RUNNING,)), WARSAW, NOW)
    form.description.blockSignals(True)
    form.description.setPlainText("Nowy opis zadania dla klienta")
    form.description.blockSignals(False)
    with qtbot.waitSignal(form.descriptionCommitted) as signal:
        QApplication.sendEvent(form.description, QFocusEvent(QEvent.Type.FocusOut))
    assert signal.args == ["Nowy opis zadania dla klienta", False]


def test_enter_on_a_running_entry_saves_instead_of_starting(form, qtbot):
    form.render(replace(CATALOG, running=(RUNNING,)), WARSAW, NOW)
    form.description.blockSignals(True)
    form.description.setPlainText("Formularz rezerwacji — poprawka dat")
    form.description.blockSignals(False)
    with qtbot.assertNotEmitted(form.startRequested), qtbot.waitSignal(form.descriptionCommitted) as signal:
        press(form.description, Qt.Key.Key_Return)
    assert signal.args == ["Formularz rezerwacji — poprawka dat", False]


def test_unchanged_description_is_not_saved(form, qtbot):
    form.render(replace(CATALOG, running=(RUNNING,)), WARSAW, NOW)
    with qtbot.assertNotEmitted(form.descriptionCommitted, wait=100):
        press(form.description, Qt.Key.Key_Return)


def test_billable_on_a_running_entry_is_saved_at_once(form, qtbot):
    form.render(replace(CATALOG, running=(RUNNING,)), WARSAW, NOW)
    with qtbot.waitSignal(form.billableChanged) as signal:
        form.billable.click()
    assert signal.args == [False]


def test_begin_edit_is_committed(form, qtbot):
    form.render(replace(CATALOG, running=(RUNNING,)), WARSAW, NOW)
    form.begin.setText("16:30")
    with qtbot.waitSignal(form.beginCommitted) as signal:
        form.begin.editingFinished.emit()
    assert signal.args == ["16:30"]


def test_refresh_keeps_what_the_user_is_typing(form):
    form.render(replace(CATALOG, running=(RUNNING,)), WARSAW, NOW)
    form.description.setPlainText("w trakcie pisania")
    form.render(replace(CATALOG, running=(RUNNING,)), WARSAW, NOW)
    assert form.description.toPlainText() == "w trakcie pisania"


def test_stopping_clears_the_form(form):
    form.render(replace(CATALOG, running=(RUNNING,)), WARSAW, NOW)
    form.end.setText("17:30")
    form.render(CATALOG, WARSAW, NOW)
    assert form.description.toPlainText() == ""
    assert form.end.text() == ""
    assert form.times.isHidden()
    assert form.project.isEnabled()


def test_idle_render_keeps_a_typed_description(form):
    form.description.setPlainText("zaczynam za chwilę")
    form.render(CATALOG, WARSAW, NOW)
    assert form.description.toPlainText() == "zaczynam za chwilę"


def test_locked_billable_is_disabled(form):
    form.render(replace(CATALOG, billable_allowed=False), WARSAW, NOW)
    assert not form.billable.isEnabled()
    assert form.billable.toolTip().startswith("Twoje konto Kimai nie ma uprawnienia")


def test_language_switch(form):
    form.retranslate(Translator("en"))
    assert form.description.placeholderText() == "What are you working on?"


def test_short_description_has_no_scroll_bar(form):
    form.description.setPlainText("jedna linia")
    assert form.description.verticalScrollBarPolicy() == Qt.ScrollBarPolicy.ScrollBarAlwaysOff
    form.description.setPlainText("\n".join(["linia"] * 12))
    assert form.description.height() == 96
    assert form.description.verticalScrollBarPolicy() == Qt.ScrollBarPolicy.ScrollBarAsNeeded


def visible_rows(popup):
    view = popup.view
    return [view.model().index(row, 0).data() for row in range(view.model().rowCount())]


def test_opening_the_list_puts_a_search_field_on_top(form, qtbot):
    form.show()
    form.project.showPopup()
    popup = form.project.popup
    qtbot.waitUntil(popup.isVisible)
    assert popup.search.placeholderText() == "Szukaj projektu…"
    assert popup.search.hasFocus()
    assert "Moduł rezerwacji" in visible_rows(popup)
    form.project.hidePopup()


def test_typing_filters_by_project_or_customer_ignoring_case_and_polish_letters(form, qtbot):
    form.show()
    form.project.showPopup()
    popup = form.project.popup
    QTest.keyClicks(popup.search, "MODUL")
    assert visible_rows(popup) == ["Hotel Morski", "Moduł rezerwacji"]
    popup.search.clear()
    QTest.keyClicks(popup.search, "wewn")  # the customer's name finds its projects
    assert visible_rows(popup) == ["Sprawy wewnętrzne", "Administracja"]
    form.project.hidePopup()


def test_enter_picks_the_first_match(form, qtbot):
    form.show()
    form.project.showPopup()
    popup = form.project.popup
    QTest.keyClicks(popup.search, "admin")
    with qtbot.waitSignal(form.projectChosen) as signal:
        QTest.keyClick(popup.search, Qt.Key.Key_Return)
    assert signal.args == [2]
    assert form.project.currentData() == 2
    assert not popup.isVisible()


def test_arrow_keys_move_through_projects_only(form, qtbot):
    form.show()
    form.project.showPopup()
    popup = form.project.popup
    QTest.keyClick(popup.search, Qt.Key.Key_Down)
    first = popup.view.currentIndex().data()
    assert first not in ("Hotel Morski", "Sprawy wewnętrzne")  # customers are headers, not choices
    form.project.hidePopup()


def test_search_text_is_cleared_for_the_next_opening(form, qtbot):
    form.show()
    form.project.showPopup()
    QTest.keyClicks(form.project.popup.search, "xyz")
    form.project.hidePopup()
    form.project.showPopup()
    assert form.project.popup.search.text() == ""
    form.project.hidePopup()


def test_search_placeholder_follows_the_language(form):
    form.retranslate(Translator("en"))
    assert form.project.popup.search.placeholderText() == "Search projects…"


def test_the_choose_a_project_row_is_never_a_search_result(form, qtbot):
    form.show()
    form.project.showPopup()
    QTest.keyClicks(form.project.popup.search, "projekt")
    assert "+ projekt" not in visible_rows(form.project.popup)
    form.project.hidePopup()


def test_search_stays_fast_with_thousands_of_projects(form, qtbot):
    import time

    from kimai_tray.core.models import Project

    many = tuple(
        Project(1000 + n, f"Projekt {n}", 10 + n // 50, f"Klient {n // 50}", None, True) for n in range(3000)
    )
    form.set_catalog(replace(CATALOG, projects=many), remembered_project=None)
    form.show()
    form.project.showPopup()
    started = time.perf_counter()
    QTest.keyClicks(form.project.popup.search, "2999")
    assert time.perf_counter() - started < 1.0
    assert visible_rows(form.project.popup) == ["Klient 59", "Projekt 2999"]
    form.project.hidePopup()


def test_running_entry_outside_the_catalog_keeps_its_project_after_a_reload(form):
    outside = replace(RUNNING, project_id=99, project_name="Archiwalny projekt")
    form.render(replace(CATALOG, running=(outside,)), WARSAW, NOW)
    form.set_catalog(CATALOG, remembered_project=1)
    assert form.project.currentData() == 99
    assert form.project.currentText() == "Archiwalny projekt"
