"""Plan 5: the controller and the main window — start, tray, closing, the list and its actions."""

from datetime import timedelta

from dk_tracker.core.settings import Settings
from dk_tracker.desktop.notifications import NotificationAction

from ..core.fakes import NOW, make_entry
from .test_app import URL, harness  # noqa: F401 - the fixture

GOOD = "Formularz rezerwacji — walidacja dat"


def booked(client):
    h = timedelta(hours=1)
    client.add(make_entry(1, NOW - 9 * h, NOW - 8 * h, description=GOOD))
    client.add(make_entry(2, NOW - 3 * h, NOW - 2 * h, description=f"{GOOD} 2"))
    client.add(make_entry(3, NOW - 10 * 24 * h, NOW - 10 * 24 * h + h, description=f"{GOOD} 3"))


def listed(h):
    model = h.controller.main_bridge.entries
    return [model.data(model.index(i, 0), 0x0100 + 5) for i in range(model.rowCount())]  # "entryId"


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
