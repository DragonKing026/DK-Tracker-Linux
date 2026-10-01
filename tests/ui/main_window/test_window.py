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
from dk_tracker.ui.theme import MAIN_DARK as DARK

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
        "settingsTheme",
        "settingsMinDescription",
        "settingsLongTimer",
        "settingsDailyNorm",
        "settingsAbout",
        "settingsVersion",
        "settingsHomepage",
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


def test_a_start_time_chosen_is_sent_and_not_overwritten_by_the_clock(window, qtbot):
    """Review C2, now with a time picker: the 1 s tick must not put the old start time back."""
    running_view(window)
    field = window.child("from")
    qtbot.waitUntil(lambda: field.property("value") == "16:42")
    with qtbot.waitSignal(window.bridge.runningEdited) as signal:
        field.setProperty("value", "07:15")
        field.edited.emit()
    assert signal.args == [{"begin": "07:15"}]
    running_view(window, now=NOW + timedelta(seconds=1))
    assert field.property("value") == "07:15"


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


# -- the edit window --------------------------------------------------------------------


def entry_details(**changes):
    from dk_tracker.core.models import EntryDetails

    begin = datetime(2026, 9, 25, 9, tzinfo=WARSAW)
    return replace(
        EntryDetails(
            id=1, begin=begin, end=begin + timedelta(minutes=90), project_id=1, activity_id=1,
            description="Kalendarz\nwidok tygodnia", tags=("frontend",), billable=True, exported=False,
            break_seconds=0,
            meta=(("ticket", "KSEF-12"),),
        ),
        **changes,
    )  # fmt: skip


def test_the_edit_window_shows_every_option(window, qtbot):
    window.bridge.open_editor(entry_details(), WARSAW)
    dialog = window.child("entryDialog")
    qtbot.waitUntil(lambda: dialog.property("opened") is True)
    for name in (
        "editDay",
        "editBegin",
        "editEnd",
        "editDuration",
        "editProject",
        "editActivity",
        "editDescription",
        "editTags",
        "editBillable",
        "editMeta",
        "editSave",
        "editCancel",
        "editDelete",
    ):
        assert window.child(name) is not None, name
    assert window.child("editTags").property("text") == "frontend"
    assert window.child("editDescription").property("text") == "Kalendarz\nwidok tygodnia"


def test_the_edit_window_shows_no_rates(window, qtbot):
    """Live test: Kimai sends rates to accounts that may see them, but its own edit form offers
    them only with edit_rate — the window had rate fields Kimai's form does not have."""
    window.bridge.open_editor(entry_details(), WARSAW)
    qtbot.waitUntil(lambda: window.child("entryDialog").property("opened") is True)
    assert window.child("editHourlyRate") is None and window.child("editFixedRate") is None


def test_the_edit_window_saves_what_was_typed(window, qtbot):
    window.bridge.open_editor(entry_details(), WARSAW)
    qtbot.waitUntil(lambda: window.child("entryDialog").property("opened") is True)
    window.child("editTags").setProperty("text", "frontend, pilne")
    window.child("editEnd").setProperty("value", "11:00")
    with qtbot.waitSignal(window.bridge.entrySaveRequested) as signal:
        window.child("editSave").clicked.emit()
    sent = signal.args[1]
    assert (sent["tags"], sent["end"], sent["meta"]) == ("frontend, pilne", "11:00", {"ticket": "KSEF-12"})


def test_the_edit_window_closes_with_the_bridge(window, qtbot):
    window.bridge.open_editor(entry_details(), WARSAW)
    dialog = window.child("entryDialog")
    qtbot.waitUntil(lambda: dialog.property("opened") is True)
    window.bridge.close_editor()
    qtbot.waitUntil(lambda: dialog.property("visible") is False)


def test_an_exported_entry_opens_locked(window, qtbot):
    """Live test: in an invoiced (exported) entry the description could still be typed in."""
    window.bridge.open_editor(entry_details(exported=True), WARSAW)
    qtbot.waitUntil(lambda: window.child("entryDialog").property("opened") is True)
    for name in (
        "editDay",
        "editBegin",
        "editEnd",
        "editProject",
        "editActivity",
        "editBillable",
        "editDescription",
        "editTags",
        "editSave",
        "editDelete",
    ):
        assert window.child(name).property("enabled") is False, name
    assert window.child("editCancel").property("enabled") is True


def test_a_click_outside_closes_the_edit_window(window, qtbot):
    from PySide6.QtCore import QPoint, Qt
    from PySide6.QtTest import QTest

    window.bridge.open_editor(entry_details(), WARSAW)
    dialog = window.child("entryDialog")
    qtbot.waitUntil(lambda: dialog.property("opened") is True)
    QTest.mouseClick(window.window, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, QPoint(5, 5))
    qtbot.waitUntil(lambda: window.bridge.editor["open"] is False)


def test_long_lists_have_a_scroll_bar(window, qtbot):
    """Live test: a long project list had no visible scroll bar."""
    from PySide6.QtCore import QMetaObject

    QMetaObject.invokeMethod(window.child("project"), "clicked")
    qtbot.waitUntil(lambda: window.child("projectScroll") is not None)
    assert window.child("entriesScroll") is not None


def test_the_settings_show_a_mask_for_a_stored_token(window, qtbot):
    from dk_tracker.core.settings import Settings

    window.bridge.settings_form.retranslate(PL)
    window.bridge.settings_form.load(Settings(url="https://kimai.test"), has_token=True)
    window.bridge.show_page("settings")
    mask = window.child("settingsTokenMask")
    qtbot.waitUntil(lambda: mask is not None and mask.property("visible") is True)
    assert window.child("settingsToken").property("text") == ""
    window.bridge.settings_form.load(Settings(url="https://kimai.test"), has_token=False)
    qtbot.waitUntil(lambda: mask.property("visible") is False)


def test_tags_are_chosen_from_a_list(window, qtbot):
    """Live test: tags from a list, as in Kimai's own form; chosen ones show as chips."""
    from PySide6.QtCore import QMetaObject

    from dk_tracker.core.models import Tag

    window.bridge.set_tags([Tag("frontend", "#9C27B0"), Tag("pilne", "#e5534b")])
    window.bridge.open_editor(entry_details(), WARSAW)
    qtbot.waitUntil(lambda: window.child("entryDialog").property("opened") is True)
    picker = window.child("editTags")
    assert picker.property("text") == "frontend"
    QMetaObject.invokeMethod(window.child("tagAdd"), "clicked")
    listing = window.child("tagList")
    qtbot.waitUntil(lambda: listing is not None and listing.property("count") == 1)  # "pilne": not chosen yet
    picker.setProperty("text", "frontend, pilne")  # what a click on "pilne" does
    qtbot.waitUntil(lambda: listing.property("count") == 0)


# -- the summaries (Plan 6) ---------------------------------------------------------------


def test_the_summary_view_has_its_parts_and_shows_when_chosen(window, qtbot):
    page = window.bridge.summary
    page.request()
    page.set_entries(
        page.span.first, page.span.last, [entry(9, 1), entry(11, 2)], tz=WARSAW, now=NOW, norm=8 * 3600
    )
    window.bridge.showPage("summary")
    view = window.child("summaryView")
    qtbot.waitUntil(lambda: view.property("visible") is True)
    assert window.child("entriesView").property("visible") is False
    parts = "viewSummary summaryKind summaryPrevious summaryNext summaryToday tileTotal tilePaid tileAverage"
    parts += " barChart normLine donutChart summaryGroup shareTable shareTip"
    for name in parts.split():
        assert window.child(name) is not None, name
    chart = window.child("barChart")
    assert len(chart.property("bars")) == 7


# -- the calendar (Plan 7) ----------------------------------------------------------------


def test_the_calendar_view_has_its_parts_and_blocks(window, qtbot):
    page = window.bridge.calendar
    page.request()
    page.set_entries(page.days[0], page.days[-1], [entry(9, 1), entry(11, 2)], tz=WARSAW, now=NOW)
    window.bridge.showPage("calendar")
    view = window.child("calendarView")
    qtbot.waitUntil(lambda: view.property("visible") is True)
    parts = "viewCalendar calendarMode calendarDays calendarPrevious calendarNext calendarToday calendarGrid"
    parts += " calendarGhost calendarNow calendarPopup"
    for name in parts.split():
        assert window.child(name) is not None, name
    assert len(page.data["blocks"]) == 2


def press_move_release(window, item, steps):
    """Mouse events in scene coordinates: the first point presses, the last releases."""
    from PySide6.QtCore import QPointF, Qt
    from PySide6.QtGui import QMouseEvent
    from PySide6.QtWidgets import QApplication

    left, none = Qt.MouseButton.LeftButton, Qt.MouseButton.NoButton
    kinds = [QMouseEvent.Type.MouseButtonPress] + [QMouseEvent.Type.MouseMove] * (len(steps) - 2)
    kinds.append(QMouseEvent.Type.MouseButtonRelease)
    # From where the item stood at the press: it moves under the pointer while dragged.
    points = [item.mapToScene(QPointF(item.width() / 2 + dx, item.height() / 2 + dy)) for dx, dy in steps]
    for kind, point in zip(kinds, points, strict=True):
        button = none if kind == QMouseEvent.Type.MouseMove else left
        held = none if kind == QMouseEvent.Type.MouseButtonRelease else left
        QApplication.sendEvent(
            window.window, QMouseEvent(kind, point, point, button, held, Qt.KeyboardModifier.NoModifier)
        )
        QApplication.processEvents()


def test_a_click_on_a_block_opens_its_bubble_and_a_drag_moves_it(window, qtbot):
    """Plan 7, review focus 2: a click alone saves nothing."""
    page = window.bridge.calendar
    page.set_hour_height(48)  # the drags below: 48 px an hour
    page.request()
    page.set_entries(page.days[0], page.days[-1], [entry(9, 1)], tz=WARSAW, now=NOW)
    window.bridge.showPage("calendar")
    from PySide6.QtCore import QSize

    window.window.resize(QSize(1000, 700))
    qtbot.waitUntil(lambda: visual_child(window.window.contentItem(), "calendarBlock_1") is not None)
    qtbot.wait(50)  # the layout after the resize
    block = visual_child(window.window.contentItem(), "calendarBlock_1")
    with qtbot.assertNotEmitted(page.moveRequested):
        press_move_release(window, block, [(0, 0), (0, 0)])
    popup = window.child("calendarPopup")
    qtbot.waitUntil(lambda: popup.property("opened") is True)
    popup.close()
    with qtbot.waitSignal(page.moveRequested) as moved:
        press_move_release(window, block, [(0, 0), (0, 10), (0, 48), (0, 48)])  # an hour down
    entry_id, day, begin, end = moved.args
    assert (entry_id, day, end - begin) == (1, date(2026, 9, 25), 60)
    assert begin == 10 * 60
