from dataclasses import replace
from datetime import timedelta

import pytest
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest

from kimai_tray.core.errors import ApiError, ErrorKind
from kimai_tray.core.i18n import Translator
from kimai_tray.core.settings import Settings
from kimai_tray.core.tracker import Snapshot, Totals
from kimai_tray.ui import placement
from kimai_tray.ui.popup import QuickWindow
from kimai_tray.ui.state import AppState

from ..core.fakes import NOW, FakeClient, make_entry

USER = FakeClient().user
RUNNING = make_entry(7, NOW - timedelta(minutes=30))
IDLE = Snapshot(
    user=USER,
    totals=Totals(today=3600, week=7200),
    recent=(make_entry(3, NOW - timedelta(hours=3), NOW - timedelta(hours=2)),),
)


@pytest.fixture
def window(qtbot):
    state = AppState(Settings(url="https://kimai.test"), Translator("pl"))
    popup = QuickWindow(state, now=lambda: NOW)
    qtbot.addWidget(popup)
    state.update(configured=True, snapshot=IDLE)
    return state, popup


def test_unconfigured_shows_only_the_settings_button(window, qtbot):
    state, popup = window
    state.update(configured=False)
    assert not popup.unconfigured.isHidden()
    assert popup.form.isHidden() and popup.recent.isHidden()
    with qtbot.waitSignal(popup.settingsRequested):
        popup.open_settings.click()


def test_header_totals_include_the_running_entry(window):
    state, popup = window
    assert popup.today.text() == "Dziś 1:00"
    assert popup.week.text() == "Tydz. 2:00"
    state.update(snapshot=replace(IDLE, running=(RUNNING,)))
    assert popup.today.text() == "Dziś 1:30"


def test_totals_are_hidden_when_kimai_did_not_give_them(window):
    state, popup = window
    state.update(snapshot=replace(IDLE, totals=None))
    assert popup.today.isHidden()


def test_error_and_saved_messages(window, qtbot):
    _, popup = window
    popup.flash_delay_ms = 30
    popup.show_error("Wybierz projekt.")
    assert popup.error.text() == "Wybierz projekt." and not popup.error.isHidden()
    popup.form.description.setPlainText("x")  # typing clears a stale error
    assert popup.error.isHidden()
    popup.flash("Opis zapisany.")
    assert not popup.saved.isHidden()
    qtbot.waitUntil(popup.saved.isHidden)


def test_refresh_error_is_shown_in_the_window(window):
    state, popup = window
    state.update(snapshot=replace(IDLE, error=ApiError(ErrorKind.CONNECTION, 0, "down")))
    assert popup.error.text() == "Brak połączenia z Kimai."


def test_notice_from_the_tracker_is_flashed(window):
    state, popup = window
    state.update(snapshot=replace(IDLE, notice="savedDescription"))
    assert popup.saved.text() == "Opis zapisany."


def test_warnings_are_listed(window):
    state, popup = window
    state.update(warnings=[("warnTimezoneMissing", {"system": "CEST"})], secrets_problem="secretsLocked")
    assert "CEST" in popup.warning.text()
    assert "zablokowany" in popup.warning.text()


def test_escape_and_close_button_hide(window, qtbot):
    _, popup = window
    popup.show()
    QTest.keyClick(popup, Qt.Key.Key_Escape)
    assert not popup.isVisible()
    popup.show()
    popup.close_button.click()
    assert not popup.isVisible()


def test_footer_opens_kimai(window, qtbot):
    _, popup = window
    with qtbot.waitSignal(popup.openKimaiRequested):
        popup.all_entries.click()


def test_language_switch(window):
    state, popup = window
    state.update(t=Translator("en"))
    assert popup.today.text() == "Today 1:00"
    assert popup.all_entries.text() == "All my entries in Kimai"


@pytest.mark.parametrize(
    ("platform", "desktop", "tray", "layer", "mode"),
    [
        ("wayland", "KDE", True, True, "layer"),
        ("wayland", "KDE", True, False, "frameless"),
        ("wayland", "GNOME", True, True, "frameless"),
        ("xcb", "KDE", True, True, "frameless"),
        ("wayland", "KDE", False, True, "window"),
    ],
)
def test_window_mode(platform, desktop, tray, layer, mode):
    assert placement.choose_mode(platform, desktop, tray_available=tray, layer_available=layer) == mode


def test_modes_set_window_flags(window):
    _, popup = window
    placement.apply(popup, "window")
    assert not popup.windowFlags() & Qt.WindowType.FramelessWindowHint
    assert popup.hide_on_deactivate is False
    placement.apply(popup, "frameless")
    assert popup.windowFlags() & Qt.WindowType.FramelessWindowHint
    assert popup.hide_on_deactivate is True


def test_layer_shell_symbol_is_present_when_the_library_is():
    """ADR-0005: the C++ symbol is fragile; this fails loudly if a new layer-shell-qt renames it."""
    try:
        import ctypes

        library = ctypes.CDLL(placement.LAYER_LIBRARY)
    except OSError:
        pytest.skip("layer-shell-qt is not installed here")
    assert hasattr(library, placement.LAYER_SYMBOL)


def test_header_starts_with_the_kimai_logo(window):
    _, popup = window
    assert popup.logo.pixmap() is not None and not popup.logo.pixmap().isNull()
