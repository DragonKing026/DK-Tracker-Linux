"""Plan 5: the controller and the main window — start, tray, closing, the list and its actions."""

from datetime import timedelta

from dk_tracker.core.errors import ApiError, ErrorKind
from dk_tracker.core.settings import Settings
from dk_tracker.desktop.notifications import NotificationAction

from ..core.fakes import NOW, make_entry
from .test_app import URL, Harness, harness  # noqa: F401 - the fixture

GOOD = "Formularz rezerwacji — walidacja dat"


def booked(client):
    h = timedelta(hours=1)
    client.add(make_entry(1, NOW - 9 * h, NOW - 8 * h, description=GOOD))
    client.add(make_entry(2, NOW - 3 * h, NOW - 2 * h, description=f"{GOOD} 2"))
    client.add(make_entry(3, NOW - 10 * 24 * h, NOW - 10 * 24 * h + h, description=f"{GOOD} 3"))


def listed(h):
    model = h.controller.main_bridge.entries
    return [model.data(model.index(i, 0), 0x0100 + 5) for i in range(model.rowCount())]  # "entryId"


def settled(h):
    """Until the list stops loading older weeks by itself (the QML list asks while it is short)."""
    weeks = None
    while weeks != h.controller._weeks:
        weeks = h.controller._weeks
        for _ in range(3):
            h.settle()


def entry_ids(h):
    return [row for row in listed(h) if row]


def opened(harness_factory, **kwargs):
    h = harness_factory(**kwargs)
    booked(h.client)
    h.controller.show_main_window()
    h.settle()
    return h


# -- start, tray, closing --------------------------------------------------------------


def test_a_start_from_the_menu_opens_the_main_window(harness, qtbot):  # noqa: F811
    h = harness()
    h.controller.start(hidden=False)
    h.settle()
    assert h.controller.main_window.isVisible()
    assert not h.controller.popup.isVisible()


def test_a_start_from_the_menu_loads_projects_and_entries_once_the_token_arrives(qtbot):
    """Review C1: the window opened before the wallet answered, and nothing loaded afterwards."""
    h = Harness(qtbot)
    booked(h.client)
    try:
        h.controller.start(hidden=False)  # the token is read in the background
        h.settle()
        assert h.controller.main_bridge.projects.rowCount() > 0
        assert entry_ids(h)[:2] == [2, 1]
        assert h.controller.main_bridge.view["page"] == "entries"  # live test: it stayed on the settings
    finally:
        h.controller.shutdown()


def test_autostart_with_a_tray_stays_in_the_tray(harness):  # noqa: F811
    h = harness()  # the harness starts hidden, as autostart does
    assert h.controller.main_window is None or not h.controller.main_window.isVisible()


def test_the_tray_can_be_turned_off(harness, qtbot):  # noqa: F811
    h = harness(settings=Settings(url=URL, language="pl", show_tray=False))
    assert h.controller.tray is None
    assert h.controller.main_window.isVisible()
    with qtbot.waitSignal(h.controller.quitRequested):
        h.controller.main_window.window.close()


def test_with_a_tray_closing_the_main_window_keeps_the_app_running(harness, qtbot):  # noqa: F811
    h = opened(harness)
    with qtbot.assertNotEmitted(h.controller.quitRequested):
        h.controller.main_window.window.close()
    assert not h.controller.main_window.isVisible()
    assert h.saved_memory[-1].main_width > 0  # the size is remembered


def test_the_tray_menu_and_the_popup_link_open_the_main_window(harness):  # noqa: F811
    h = harness()
    h.controller.tray.open_main_action.trigger()
    assert h.controller.main_window.isVisible()
    h.controller.main_window.hide()
    h.controller.show_popup()
    h.controller.popup.all_entries.click()
    assert h.controller.main_window.isVisible()
    assert not h.controller.popup.isVisible()


def test_clicking_a_notification_opens_the_main_window(harness):  # noqa: F811
    h = harness()
    h.controller.on_notification(NotificationAction("action.1790000000", "open", None))
    assert h.controller.main_window.isVisible()


def test_turning_the_tray_off_in_the_settings_shows_the_main_window(harness):  # noqa: F811
    h = harness()
    h.controller.save_settings(Settings(url=URL, language="pl", show_tray=False), None)
    h.settle()
    assert h.controller.tray is None
    assert h.controller.main_window.isVisible()


# -- the list ------------------------------------------------------------------------


def test_the_main_window_lists_the_newest_entries_first(harness):  # noqa: F811
    """A short list fills the window by itself: older weeks load until it scrolls (Toggl-style)."""
    h = opened(harness)
    assert entry_ids(h) == [2, 1, 3]


def test_scrolling_down_loads_the_week_before(harness):  # noqa: F811
    h = opened(harness)
    h.controller.main_bridge.loadMore()
    h.settle()
    assert entry_ids(h) == [2, 1, 3]


def test_loading_stops_after_empty_weeks(harness):  # noqa: F811
    h = opened(harness)
    for _ in range(12):
        h.controller.main_bridge.loadMore()
        h.settle()
    ranges = [call for call in h.client.calls if call[0] == "range" and call[1] < "2026-09-21"]
    assert len(ranges) <= 9  # one week back found entry 3, then eight empty weeks at most


def test_search_in_the_main_window_lists_the_results(harness):  # noqa: F811
    h = opened(harness)
    h.controller.main_bridge.search("walidacja dat 3")
    h.settle()
    assert entry_ids(h) == [3]
    h.controller.main_bridge.search("")
    h.settle()
    assert entry_ids(h)[:2] == [2, 1]


# -- actions -------------------------------------------------------------------------


def test_an_entry_typed_in_by_hand_is_added_and_listed(harness):  # noqa: F811
    h = opened(harness)
    h.controller.main_bridge.addManual("2026-09-25", "06:00", "07:00", f"{GOOD} rano", 1, 1, None)
    h.settle()
    assert [c[0] for c in h.client.calls].count("create_entry") == 1
    assert len(entry_ids(h)) == 4


def test_an_edit_that_breaks_a_rule_is_shown_under_its_row(harness):  # noqa: F811
    h = opened(harness)
    h.controller.main_bridge.editDescription(1, "krótko")
    h.settle()
    assert h.controller.main_bridge.rowErrors["1"].startswith("Opis jest za krótki")


def test_an_edit_reaches_kimai_and_the_list_follows(harness):  # noqa: F811
    h = opened(harness)
    h.controller.main_bridge.editTimes(1, "", "12:00")
    h.settle()
    assert ("update", 1, {"end": "2026-09-25T12:00:00"}) in h.client.calls


def test_a_delete_reaches_kimai_after_the_undo_bar(harness, qtbot):  # noqa: F811
    h = opened(harness)
    h.controller.main_bridge.undo_ms = 20
    h.controller.main_bridge.deleteEntry(2)
    qtbot.waitUntil(lambda: ("delete_entry", 2) in h.client.calls)
    h.settle()
    assert entry_ids(h) == [1, 3]


def test_quitting_sends_a_pending_delete(harness):  # noqa: F811
    h = opened(harness)
    h.controller.main_bridge.undo_ms = 60_000
    h.controller.main_bridge.deleteEntry(2)
    h.controller.shutdown()
    assert ("delete_entry", 2) in h.client.calls


def test_resume_from_the_list(harness):  # noqa: F811
    h = opened(harness)
    h.controller.main_bridge.resume(1)
    h.settle()
    assert h.state.snapshot.current.description == GOOD


def test_the_timer_bar_starts_and_edits_the_running_entry(harness):  # noqa: F811
    h = opened(harness)
    h.controller.main_bridge.start(f"{GOOD} nowy", 1, 1, None)
    h.settle()
    assert h.state.snapshot.current.description == f"{GOOD} nowy"
    h.controller.main_bridge.runningDescription(f"{GOOD} poprawiony")
    h.settle()
    assert h.state.snapshot.current.description == f"{GOOD} poprawiony"
    assert h.controller.main_bridge.view["description"] == f"{GOOD} poprawiony"


def test_scrolling_through_search_results_does_not_load_weeks(harness):  # noqa: F811
    h = opened(harness)
    h.controller.main_bridge.search("walidacja dat 3")
    h.settle()
    before = len([call for call in h.client.calls if call[0] == "range"])
    h.controller.main_bridge.loadMore()
    h.settle()
    assert len([call for call in h.client.calls if call[0] == "range"]) == before
    assert entry_ids(h) == [3]


# -- review fixes ------------------------------------------------------------------------


def test_a_failed_delete_brings_the_row_back_with_the_error(harness, qtbot):  # noqa: F811
    """Review I2: the row stayed hidden for good and its error went to a row nobody saw."""
    h = opened(harness)
    h.client.fail["delete_entry"] = [ApiError(ErrorKind.FORBIDDEN, 403, "Access denied")]
    h.controller.main_bridge.undo_ms = 20
    h.controller.main_bridge.deleteEntry(2)
    qtbot.waitUntil(lambda: ("delete_entry", 2) in h.client.calls)
    h.settle()
    assert 2 in entry_ids(h)
    assert h.controller.main_bridge.view["error"] != ""


def test_a_delete_during_a_search_still_reaches_kimai(harness, qtbot):  # noqa: F811
    """Review I3: the search replaced the list, the entry was not found and nothing was sent."""
    h = opened(harness)
    h.controller.main_bridge.undo_ms = 10_000
    h.controller.main_bridge.deleteEntry(2)
    h.controller.main_bridge.search("walidacja dat 3")
    h.settle()
    h.controller.main_bridge.flush_deletes()
    h.settle()
    assert ("delete_entry", 2) in h.client.calls


def test_a_failed_refresh_clears_once_kimai_answers_again(harness):  # noqa: F811
    """Review I1: "no connection" stayed after the connection came back."""
    h = opened(harness)
    h.client.fail["range"] = [ApiError(ErrorKind.CONNECTION, 0, "offline") for _ in range(20)]
    h.controller._on_poll()
    h.settle()
    assert h.controller.main_bridge.view["error"] != ""
    h.client.fail["range"] = []  # the connection is back
    h.controller._on_poll()
    h.settle()
    assert h.controller.main_bridge.view["error"] == ""


def test_empty_weeks_are_skipped_until_an_entry_or_the_limit(harness):  # noqa: F811
    """Review I5: loading stopped at the first empty week while the list was still short."""
    h = harness()
    h.client.add(make_entry(7, NOW - timedelta(days=30), NOW - timedelta(days=30) + timedelta(hours=1)))
    h.controller.show_main_window()
    h.settle()
    assert 7 in entry_ids(h)


def test_a_row_picker_gets_the_activities_of_its_project(harness):  # noqa: F811
    h = opened(harness)
    h.controller.main_bridge.chooseRowProject(2)
    h.settle()
    assert h.controller.main_bridge.rowActivities.rowCount() == 2


def test_the_minute_refresh_does_not_load_older_weeks(harness):  # noqa: F811
    """A list taller than the window: the minute's refresh reloads it, no older week is asked for.
    (A short list does ask — the QML list is at its end — until it fills the window.)"""
    h = harness()
    for n in range(30):
        begin = NOW - timedelta(hours=9) + timedelta(minutes=10 * n)
        h.client.add(make_entry(200 + n, begin, begin + timedelta(minutes=5), description=f"{GOOD} {n}"))
    for week in range(1, 13):  # one entry a week back: loading older weeks always finds something
        begin = NOW - timedelta(weeks=week)
        h.client.add(make_entry(300 + week, begin, begin + timedelta(hours=1), description=f"{GOOD} w{week}"))
    h.controller.show_main_window()
    settled(h)
    for _ in range(2):  # scrolled down: older weeks in the list
        h.controller._load_more()
        settled(h)
    weeks = h.controller._weeks
    assert weeks >= 3
    for _ in range(3):
        h.controller._on_poll()
        h.settle()
    assert h.controller._weeks == weeks


# -- the edit window --------------------------------------------------------------------


def test_clicking_a_row_opens_the_edit_window_with_what_kimai_has(harness):  # noqa: F811
    h = opened(harness)
    h.client.details[2] = {"tags": ["frontend"], "metaFields": [{"name": "ticket", "value": "KSEF-1"}]}
    h.controller.main_bridge.openEntry(2)
    h.settle()
    editor = h.controller.main_bridge.editor
    assert editor["open"] is True and editor["entryId"] == 2
    assert editor["tags"] == "frontend" and editor["meta"] == [{"name": "ticket", "value": "KSEF-1"}]
    assert ("entry_details", 2) in h.client.calls


def test_saving_the_edit_window_reaches_kimai_and_closes_it(harness):  # noqa: F811
    h = opened(harness)
    h.controller.main_bridge.openEntry(2)
    h.settle()
    h.controller.main_bridge.saveEntry(dict(h.controller.main_bridge.editor, tags="frontend, pilne"))
    h.settle()
    assert ("update", 2, {"tags": "frontend,pilne"}) in h.client.calls
    assert h.controller.main_bridge.editor["open"] is False


def test_a_refused_save_keeps_the_edit_window_open_with_the_reason(harness):  # noqa: F811
    h = opened(harness)
    h.controller.main_bridge.openEntry(2)
    h.settle()
    h.client.fail["update"] = [ApiError(ErrorKind.FORBIDDEN, 403, "Access denied")]
    h.controller.main_bridge.saveEntry(dict(h.controller.main_bridge.editor, tags="frontend"))
    h.settle()
    editor = h.controller.main_bridge.editor
    assert editor["open"] is True and editor["error"] != "" and editor["busy"] is False


def test_tags_kimai_left_out_are_told_in_the_main_window(harness):  # noqa: F811
    h = opened(harness)
    h.client.known_tags = {"frontend"}
    h.controller.main_bridge.openEntry(2)
    h.settle()
    h.controller.main_bridge.saveEntry(dict(h.controller.main_bridge.editor, tags="frontend, nowy"))
    h.settle()
    assert "nowy" in h.controller.main_bridge.view["error"]


def test_a_theme_chosen_in_the_settings_applies_to_both_windows_at_once(harness):  # noqa: F811
    from dk_tracker.ui.theme import DARK, LIGHT, MAIN_DARK, MAIN_LIGHT

    h = opened(harness)
    for theme, main, popup in (("light", MAIN_LIGHT, LIGHT), ("dark", MAIN_DARK, DARK)):
        h.controller.save_settings(Settings(url=URL, language="pl", theme=theme), None)
        h.settle()
        assert h.controller.main_bridge.palette["bg"] == main["bg"]
        assert popup["surface"] in h.controller.popup.styleSheet()


def test_opening_an_entry_brings_the_tags_to_choose(harness):  # noqa: F811
    from dk_tracker.core.models import Tag

    h = opened(harness)
    h.client.tags_list = [Tag("frontend", "#9C27B0")]
    h.controller.main_bridge.openEntry(2)
    h.settle()
    assert h.controller.main_bridge.tagOptions == [{"name": "frontend", "color": "#9C27B0"}]
