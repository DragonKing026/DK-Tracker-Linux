from datetime import timedelta

from PySide6.QtWidgets import QSystemTrayIcon

from ws_tracker_tray.core.i18n import Translator
from ws_tracker_tray.core.settings import Settings
from ws_tracker_tray.core.tracker import Snapshot
from ws_tracker_tray.ui.state import AppState
from ws_tracker_tray.ui.tray import Tray

from ..core.fakes import NOW, FakeClient, make_entry

USER = FakeClient().user
RUNNING = make_entry(7, NOW - timedelta(minutes=82))
DONE = make_entry(6, NOW - timedelta(hours=3), NOW - timedelta(hours=2))


def make(qtbot, **state):
    app_state = AppState(Settings(url="https://kimai.test"), Translator("pl"))
    app_state.update(configured=True, **state)
    tray = Tray(app_state, now=lambda: NOW)
    return app_state, tray


def test_running_entry_enables_stop_and_shows_the_time(qtbot):
    _, tray = make(qtbot, snapshot=Snapshot(user=USER, running=(RUNNING,), recent=(DONE,)))
    assert tray.status.label == "1:22"
    assert tray.stop_action.isEnabled()
    assert not tray.resume_action.isEnabled()
    assert tray.icon.toolTip().startswith("WS Tracker — 1:22:00")


def test_idle_with_history_enables_resume(qtbot):
    _, tray = make(qtbot, snapshot=Snapshot(user=USER, recent=(DONE,)))
    assert tray.status.kind == "idle"
    assert tray.resume_action.isEnabled()
    assert not tray.stop_action.isEnabled()


def test_unconfigured_disables_actions_that_need_kimai(qtbot):
    state, tray = make(qtbot)
    state.update(configured=False)
    assert tray.status.kind == "unconfigured"
    assert not tray.open_kimai_action.isEnabled()
    assert not tray.resume_action.isEnabled()


def test_menu_actions_emit_requests(qtbot):
    _, tray = make(qtbot, snapshot=Snapshot(user=USER, running=(RUNNING,)))
    with qtbot.waitSignal(tray.stopRequested):
        tray.stop_action.trigger()
    with qtbot.waitSignal(tray.settingsRequested):
        tray.settings_action.trigger()
    with qtbot.waitSignal(tray.quitRequested):
        tray.quit_action.trigger()


def test_left_click_opens_and_middle_click_does_nothing(qtbot):
    _, tray = make(qtbot)
    with qtbot.waitSignal(tray.openRequested):
        tray.icon.activated.emit(QSystemTrayIcon.ActivationReason.Trigger)
    with qtbot.assertNotEmitted(tray.openRequested), qtbot.assertNotEmitted(tray.stopRequested):
        tray.icon.activated.emit(QSystemTrayIcon.ActivationReason.MiddleClick)


def test_language_switch_retranslates_the_menu(qtbot):
    state, tray = make(qtbot)
    assert tray.quit_action.text() == "Zakończ"
    state.update(t=Translator("en"))
    assert tray.quit_action.text() == "Quit"


def test_icon_is_redrawn_only_when_the_label_changes(qtbot):
    state, tray = make(qtbot, snapshot=Snapshot(user=USER, running=(RUNNING,)))
    drawn = tray.drawn
    state.update(snapshot=Snapshot(user=USER, running=(RUNNING,)))
    assert tray.drawn == drawn


def test_clicks_on_the_icon_are_logged(qtbot, caplog):
    _, tray = make(qtbot)
    with caplog.at_level("INFO", logger="ws_tracker_tray.ui.tray"):
        tray.icon.activated.emit(QSystemTrayIcon.ActivationReason.Trigger)
    assert "Trigger" in caplog.text
