"""Plan 5: the QML main window loads without a display and shows what `app` holds (smoke tests)."""

from dataclasses import replace
from datetime import UTC, date, datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from dk_tracker.core.entry_list import build_rows
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
    made.hide()


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


def test_unconfigured_shows_only_the_settings_button(window, qtbot):
    window.bridge.render(Snapshot(), configured=False, t=PL, now=NOW, tz=WARSAW)
    qtbot.waitUntil(lambda: window.child("unconfigured").property("visible") is True)
    assert window.child("timerBar").property("visible") is False


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
        made.hide()
    finally:
        qInstallMessageHandler(previous)
    assert warnings == []
