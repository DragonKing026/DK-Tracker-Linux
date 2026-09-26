from dataclasses import replace
from datetime import timedelta

import pytest
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest

from ws_tracker_tray.core.errors import ApiError, ErrorKind
from ws_tracker_tray.core.i18n import Translator
from ws_tracker_tray.core.settings import Settings
from ws_tracker_tray.core.tracker import Snapshot, Totals
from ws_tracker_tray.ui import placement
from ws_tracker_tray.ui.popup import QuickWindow
from ws_tracker_tray.ui.state import AppState

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


def mouse(widget, kind, global_pos, buttons):
    from PySide6.QtCore import QEvent, QPointF
    from PySide6.QtGui import QMouseEvent
    from PySide6.QtWidgets import QApplication

    event_type = {
        "press": QEvent.Type.MouseButtonPress,
        "move": QEvent.Type.MouseMove,
        "release": QEvent.Type.MouseButtonRelease,
    }[kind]
    local = QPointF(widget.mapFromGlobal(global_pos))
    event = QMouseEvent(
        event_type,
        local,
        QPointF(global_pos),
        Qt.MouseButton.LeftButton,
        buttons,
        Qt.KeyboardModifier.NoModifier,
    )
    QApplication.sendEvent(widget, event)


def drag(widget, dx, dy):
    from PySide6.QtCore import QPoint

    start = widget.mapToGlobal(QPoint(3, 3))
    held = Qt.MouseButton.LeftButton
    mouse(widget, "press", start, held)
    mouse(widget, "move", start + QPoint(dx, dy), held)
    mouse(widget, "release", start + QPoint(dx, dy), Qt.MouseButton.NoButton)


def test_grip_drag_grows_the_window_up_and_left(window, qtbot):
    from PySide6.QtCore import QSize

    _, popup = window
    popup.set_preferred_size(QSize(460, 600))
    popup.show()
    with qtbot.waitSignal(popup.sizeChosen) as signal:
        drag(popup.grip, -100, -50)
    assert popup.size() == QSize(560, 650)
    assert signal.args == [QSize(560, 650)]


def test_window_size_has_a_floor(window):
    from PySide6.QtCore import QSize

    _, popup = window
    popup.set_preferred_size(QSize(100, 100))
    assert popup.size() == popup.minimumSize()
    assert popup.minimumWidth() >= 400


def test_recent_list_takes_the_height_it_is_given(window):
    _, popup = window
    assert popup.recent.scroll.maximumHeight() > 10_000


def test_an_ordinary_window_is_resized_by_its_frame(window):
    _, popup = window
    placement.apply(popup, "window")
    assert popup.grip.isHidden()


def test_unconfigured_window_is_only_as_tall_as_its_content(window, qtbot):
    from PySide6.QtCore import QSize

    state, popup = window
    popup.set_preferred_size(QSize(460, 600))
    state.update(configured=False)
    popup.show()
    qtbot.waitExposed(popup)
    assert popup.height() < 300
    assert popup.header.height() <= popup.header.sizeHint().height() + 2  # no stretching into empty space
    state.update(configured=True)
    assert popup.size() == QSize(460, 600)  # the user's size comes back with the lists


def test_connection_error_strip_goes_away_when_kimai_is_back(window):
    state, popup = window
    state.update(snapshot=replace(IDLE, error=ApiError(ErrorKind.CONNECTION, 0, "down")))
    assert not popup.error.isHidden()
    state.update(snapshot=IDLE)
    assert popup.error.isHidden()


def test_an_action_error_is_not_wiped_by_a_refresh(window):
    state, popup = window
    popup.show_error("Wybierz projekt.")
    state.update(snapshot=IDLE)
    assert popup.error.text() == "Wybierz projekt."


def test_size_set_by_the_compositor_is_reported_after_a_pause(window, qtbot):
    from PySide6.QtCore import QSize

    state, popup = window
    popup.size_report_ms = 20
    popup.show()
    with qtbot.waitSignal(popup.sizeChosen) as signal:
        popup.resize(QSize(600, 700))  # e.g. a frameless window resized with startSystemResize
    assert signal.args == [QSize(600, 700)]


def test_every_save_flashes_even_with_the_same_message(window):
    state, popup = window
    state.update(snapshot=replace(IDLE, notice="savedDescription"))
    popup.saved.hide()
    state.update(snapshot=replace(IDLE, notice="savedDescription"))  # a second save: a new Snapshot
    assert not popup.saved.isHidden()


def test_a_tracker_error_notice_is_not_brought_back_by_other_updates(window):
    state, popup = window
    state.update(snapshot=replace(IDLE, notice="errBillableDenied"))
    assert not popup.error.isHidden()
    popup.clear_error()  # the user typed
    state.update(warnings=[])  # anything else redraws the window with the same Snapshot
    assert popup.error.isHidden()


def test_remembered_size_never_exceeds_the_screen(window):
    from PySide6.QtCore import QSize

    state, popup = window
    area = popup.screen().availableGeometry()
    popup.set_preferred_size(QSize(5000, 5000))  # remembered on a 4K monitor, started on a laptop
    assert popup.width() <= area.width() - 24
    assert popup.height() <= area.height() - 24


def test_grip_on_a_layer_surface_uses_the_position_in_the_grip(window, qtbot):
    """Wayland gives a layer surface no global position: the drag must not depend on it (it jumped)."""
    from PySide6.QtCore import QEvent, QPointF, QSize
    from PySide6.QtGui import QMouseEvent
    from PySide6.QtWidgets import QApplication

    _, popup = window
    popup.set_preferred_size(QSize(460, 600))
    popup.placement_mode = "layer"
    popup.show()
    nowhere = QPointF(0, 0)  # what a layer surface reports as the global cursor position

    def send(kind, x, y, buttons=Qt.MouseButton.LeftButton):
        event_type = {
            "press": QEvent.Type.MouseButtonPress,
            "move": QEvent.Type.MouseMove,
            "release": QEvent.Type.MouseButtonRelease,
        }[kind]
        event = QMouseEvent(
            event_type,
            QPointF(x, y),
            nowhere,
            Qt.MouseButton.LeftButton,
            buttons,
            Qt.KeyboardModifier.NoModifier,
        )
        QApplication.sendEvent(popup.grip, event)

    send("press", 3, 3)
    send("move", -17, -7)  # 20 px left, 10 px up
    assert popup.size() == QSize(480, 610)
    send("move", -7, -7)  # anchored bottom-right, the grip followed the cursor; 10 px more each way
    assert popup.size() == QSize(490, 620)
    with qtbot.waitSignal(popup.sizeChosen) as signal:
        send("release", -7, -7, Qt.MouseButton.NoButton)
    assert signal.args == [QSize(490, 620)]
