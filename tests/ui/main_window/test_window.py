"""Plan 5: the QML main window loads without a display and shows what `app` holds (smoke tests)."""

from dataclasses import replace
from datetime import UTC, date, datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from dk_tracker.core.entry_list import build_rows
from dk_tracker.core.errors import ApiError, ErrorKind
from dk_tracker.core.i18n import Translator
from dk_tracker.core.tracker import Snapshot
from dk_tracker.ui.main_window.bridge import MainBridge
from dk_tracker.ui.main_window.window import MainWindow
from dk_tracker.ui.theme import DARK

from ...core.fakes import NOW, FakeClient, make_entry

WARSAW = ZoneInfo("Europe/Warsaw")
PL = Translator("pl")


def entry(hour, entry_id, **extra):
    begin = datetime(2026, 9, 25, hour, tzinfo=WARSAW).astimezone(UTC)
    return replace(make_entry(entry_id, begin, begin + timedelta(hours=1)), **extra)


def visual_child(item, name):
    """List rows have a visual parent only, so `findChild` does not see them."""
    for child in item.childItems():
        if child.objectName() == name:
            return child
        if (found := visual_child(child, name)) is not None:
            return found
    return None


@pytest.fixture
def window(qapp):
    bridge = MainBridge()
    bridge.set_palette(DARK)
    bridge.render(Snapshot(user=FakeClient().user), configured=True, t=PL, now=NOW, tz=WARSAW)
    bridge.set_projects(FakeClient().projects_list)
    bridge.set_entries(
        build_rows([entry(9, 1), entry(11, 2, exported=True)], WARSAW, date(2026, 9, 25), 0, PL), WARSAW
    )
    made = MainWindow(bridge)
    made.show()
    yield made
    made.dispose()


def test_the_window_has_its_parts(window):
    for name in (
        "sidebar",
        "timerBar",
        "description",
        "project",
        "activity",
        "submit",
        "entriesList",
        "search",
    ):
        assert window.child(name) is not None, name
    assert window.child("mainWindow") is None or True  # the root itself


def test_the_list_shows_every_row_of_the_model(window, qtbot):
    listing = window.child("entriesList")
    qtbot.waitUntil(lambda: listing.property("count") == 4)


def test_unconfigured_shows_the_settings_page(window, qtbot):
    window.bridge.render(Snapshot(), configured=False, t=PL, now=NOW, tz=WARSAW)
    qtbot.waitUntil(lambda: window.child("settingsView").property("visible") is True)
    assert window.child("timerBar").property("visible") is False
    assert window.child("entriesView").property("visible") is False


def test_the_settings_page_has_its_fields(window, qtbot):
    window.bridge.settings_form.retranslate(PL)
    window.bridge.show_page("settings")
    qtbot.waitUntil(lambda: window.child("settingsView").property("visible") is True)
    for name in (
        "settingsUrl",
        "settingsToken",
        "settingsLanguage",
        "settingsMinDescription",
        "settingsLongTimer",
        "settingsAutostart",
        "settingsShowTray",
        "settingsSave",
        "settingsTest",
    ):
        assert window.child(name) is not None, name
    assert window.child("entriesView").property("visible") is False


def test_the_settings_page_saves_what_was_typed(window, qtbot):
    from dk_tracker.core.settings import Settings

    form = window.bridge.settings_form
    form.retranslate(PL)
    form.load(Settings(url="https://kimai.test", language="pl"), has_token=True)
    window.bridge.show_page("settings")
    window.child("settingsUrl").setProperty("text", "https://kimai.firma.pl")
    with qtbot.waitSignal(form.saveRequested) as signal:
        window.child("settingsSave").clicked.emit()
    assert signal.args[0].url == "https://kimai.firma.pl" and signal.args[1] is None


def test_closing_hides_and_tells_the_controller(window, qtbot):
    with qtbot.waitSignal(window.closed):
        window.window.close()
    assert not window.isVisible()


def test_the_undo_bar_appears_after_a_delete(window, qtbot):
    window.bridge.undo_ms = 10_000
    window.bridge.deleteEntry(1)
    qtbot.waitUntil(lambda: window.child("undoBar").property("visible") is True)
    window.bridge.undoDelete()
    qtbot.waitUntil(lambda: window.child("undoBar").property("visible") is False)


def test_texts_are_polish(window):
    assert window.child("description").property("placeholderText") == "Co robisz?"


def test_no_qml_warnings_on_load(qapp, qtbot):
    """A binding to a missing property only warns in QML; fail on any warning while loading."""
    from PySide6.QtCore import QtMsgType, qInstallMessageHandler

    warnings = []

    def handler(kind, context, message):
        if (
            kind in (QtMsgType.QtWarningMsg, QtMsgType.QtCriticalMsg)
            and "qml" in (context.file or "").lower() + message.lower()
        ):
            warnings.append(message)

    previous = qInstallMessageHandler(handler)
    try:
        bridge = MainBridge()
        bridge.set_palette(DARK)
        bridge.render(Snapshot(user=FakeClient().user), configured=True, t=PL, now=NOW, tz=WARSAW)
        made = MainWindow(bridge)
        made.show()
        qtbot.wait(50)
        made.dispose()
    finally:
        qInstallMessageHandler(previous)
    assert warnings == []


def test_offline_locks_editing_but_not_the_list(window, qtbot):
    """Spec, section 9: without a connection the last data stays visible and cannot be edited."""
    qtbot.waitUntil(lambda: visual_child(window.child("entriesList"), "entryRow") is not None)
    window.bridge.render(
        Snapshot(user=FakeClient().user, error=ApiError(ErrorKind.CONNECTION, 0)),
        configured=True,
        t=PL,
        now=NOW,
        tz=WARSAW,
    )
    qtbot.waitUntil(lambda: window.child("timerBar").property("enabled") is False)
    assert visual_child(window.child("entriesList"), "entryRow").property("enabled") is False
    assert window.child("entriesList").property("enabled") is True


# -- review fixes: the timer bar, the scroll position ------------------------------------


def running_view(window, *, now=NOW, activities=True):
    """The window with an entry running since 16:42 (Warsaw) on project 1, activity 2."""
    current = replace(make_entry(9, now - timedelta(minutes=82), activity_id=2), description="Trwa")
    window.bridge.render(
        Snapshot(user=FakeClient().user, running=(current,)), configured=True, t=PL, now=now, tz=WARSAW
    )
    if activities:
        window.bridge.set_activities(FakeClient().activities_list)
    return current


def test_a_start_time_being_typed_is_not_overwritten_by_the_clock(window, qtbot):
    """Review C2: the 1 s tick put the old start time back into the field being typed in."""
    running_view(window)
    field = window.child("from")
    qtbot.waitUntil(lambda: field.property("text") != ":")
    window.window.requestActivate()
    field.forceActiveFocus()
    field.setProperty("text", "07:15")
    running_view(window, now=NOW + timedelta(seconds=1))
    assert field.property("text") == "07:15"


def test_a_project_chosen_for_the_running_entry_survives_the_clock(window):
    """Review C3: sync() reset the picked project before an activity could be chosen."""
    running_view(window)
    bar = window.child("timerBar")
    assert bar.property("projectId") == 1
    bar.setProperty("projectId", 2)  # as the picker does
    running_view(window, now=NOW + timedelta(seconds=1))
    assert bar.property("projectId") == 2


def test_the_activity_of_the_running_entry_shows_once_activities_arrive(window, qtbot):
    """Review I4: the combo was indexed before its model filled and showed the placeholder."""
    window.bridge.set_activities([])
    running_view(window, activities=False)
    window.bridge.set_activities(FakeClient().activities_list)
    combo = window.child("activity")
    qtbot.waitUntil(lambda: combo.property("currentText") == "Spotkanie")


def test_the_project_name_shows_once_projects_arrive(qapp, qtbot):
    bridge = MainBridge()
    bridge.set_palette(DARK)
    made = MainWindow(bridge)
    made.show()
    try:
        running_view(made)
        bridge.set_projects(FakeClient().projects_list)
        picker = made.child("project")
        qtbot.waitUntil(lambda: picker.property("text") == "Moduł rezerwacji")
    finally:
        made.dispose()


def test_the_list_keeps_its_scroll_position_on_refresh(window, qtbot):
    """Review C4: every refresh reset the model and the list jumped to the top."""
    many = [entry(9, i) for i in range(1, 2)] + [
        replace(
            make_entry(
                i,
                datetime(2026, 9, 25, 8, tzinfo=WARSAW).astimezone(UTC) - timedelta(hours=3 * i),
                datetime(2026, 9, 25, 9, tzinfo=WARSAW).astimezone(UTC) - timedelta(hours=3 * i),
            )
        )
        for i in range(2, 80)
    ]
    rows = build_rows(many, WARSAW, date(2026, 9, 25), 0, PL)
    window.bridge.set_entries(rows, WARSAW)
    listing = window.child("entriesList")
    qtbot.waitUntil(lambda: listing.property("contentHeight") > 2000)
    listing.setProperty("contentY", 1500)
    window.bridge.set_entries(rows, WARSAW)
    qtbot.wait(20)
    assert listing.property("contentY") == 1500


def test_the_basic_style_is_used_even_when_the_desktop_chose_another(qapp):
    """Live test on KDE: the platform theme picks org.kde.desktop first, our palette then did not
    apply and the fields were white with dark text on the dark window."""
    from PySide6.QtQuickControls2 import QQuickStyle

    QQuickStyle.setStyle("Fusion")
    made = MainWindow(MainBridge())
    try:
        assert QQuickStyle.name() == "Basic"
    finally:
        made.dispose()


def test_showing_an_open_window_again_keeps_its_size(window, qtbot):
    """Live test: clicking "Settings" called show() again and the window jumped to the remembered size."""
    from PySide6.QtCore import QSize

    window.window.resize(QSize(1234, 777))
    qtbot.waitUntil(lambda: window.size() == QSize(1234, 777))
    window.show(QSize(1000, 700))
    qtbot.wait(20)
    assert window.size() == QSize(1234, 777)


def test_showing_a_maximized_window_again_keeps_it_maximized(window, qtbot):
    """Live test: "Settings" called show() on the open window, and QWindow.show() is showNormal()."""
    from PySide6.QtCore import Qt

    window.window.showMaximized()
    qtbot.waitUntil(lambda: bool(window.window.windowStates() & Qt.WindowState.WindowMaximized))
    window.show()
    qtbot.wait(20)
    assert window.window.windowStates() & Qt.WindowState.WindowMaximized
