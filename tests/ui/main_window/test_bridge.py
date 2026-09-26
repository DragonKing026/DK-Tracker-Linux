"""Plan 5: `app`, the object the QML main window talks to — state in, actions out, undo."""

from dataclasses import replace
from datetime import UTC, date, datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from dk_tracker.core.entry_list import build_rows
from dk_tracker.core.i18n import Translator
from dk_tracker.core.tracker import Snapshot, Totals
from dk_tracker.ui.main_window.bridge import MainBridge
from dk_tracker.ui.theme import DARK

from ...core.fakes import NOW, FakeClient, make_entry

WARSAW = ZoneInfo("Europe/Warsaw")
PL = Translator("pl")
CLIENT = FakeClient()
RUNNING = make_entry(9, NOW - timedelta(minutes=82), description="Formularz rezerwacji pokoi")
SNAPSHOT = Snapshot(user=CLIENT.user, running=(RUNNING,), totals=Totals(today=3600, week=7200))


def first(hour, entry_id):
    begin = datetime(2026, 9, 25, hour, tzinfo=WARSAW).astimezone(UTC)
    return make_entry(entry_id, begin, begin + timedelta(hours=1), description="Kalendarz dostępności pokoi")


@pytest.fixture
def bridge(qapp):
    made = MainBridge()
    made.undo_ms = 60
    made.render(SNAPSHOT, configured=True, t=PL, now=NOW, tz=WARSAW)
    made.set_entries(build_rows([first(9, 1), first(11, 2)], WARSAW, date(2026, 9, 25), 0, PL), WARSAW)
    return made


def test_view_shows_the_running_entry_and_the_totals(bridge):
    view = bridge.view
    assert (view["running"], view["description"], view["projectId"], view["begin"]) == (
        True, "Formularz rezerwacji pokoi", 1, "16:42"
    )  # fmt: skip
    assert (view["clock"], view["today"], view["week"]) == ("1:22:00", "Dziś 2:22", "Tydz. 3:22")
    assert view["configured"] and not view["offline"] and view["error"] == ""


def test_texts_follow_the_language(bridge):
    assert bridge.texts["recent"] == "Ostatnie wpisy"
    bridge.render(SNAPSHOT, configured=True, t=Translator("en"), now=NOW, tz=WARSAW)
    assert bridge.texts["recent"] == "Recent entries"


def test_palette_is_the_theme(bridge):
    bridge.set_palette(DARK)
    assert bridge.palette["bg"] == DARK["bg"]


def test_a_failed_refresh_puts_the_window_offline(bridge):
    from dk_tracker.core.errors import ApiError, ErrorKind

    bridge.render(
        replace(SNAPSHOT, error=ApiError(ErrorKind.CONNECTION, 0, "x")),
        configured=True,
        t=PL,
        now=NOW,
        tz=WARSAW,
    )
    assert bridge.view["offline"] is True
    assert bridge.view["error"] != ""


def test_start_passes_an_untouched_billable_as_none(bridge, qtbot):
    with qtbot.waitSignal(bridge.startRequested) as signal:
        bridge.start("Nowy formularz rezerwacji", 1, 2, None)
    assert signal.args == [
        {"project_id": 1, "activity_id": 2, "description": "Nowy formularz rezerwacji", "billable": None}
    ]


def test_add_manual_parses_the_day(bridge, qtbot):
    with qtbot.waitSignal(bridge.addRequested) as signal:
        bridge.addManual("2026-09-24", "09:00", "10:30", "Uzupełnienie wpisu", 1, 2, False)
    assert signal.args == [
        {
            "day": date(2026, 9, 24),
            "begin": "09:00",
            "end": "10:30",
            "description": "Uzupełnienie wpisu",
            "project_id": 1,
            "activity_id": 2,
            "billable": False,
        }
    ]


def test_edits_name_the_entry_and_the_change(bridge, qtbot):
    with qtbot.waitSignal(bridge.editRequested) as signal:
        bridge.editTimes(1, "09:15", "")
    assert signal.args == [1, {"begin": "09:15", "end": None}]
    with qtbot.waitSignal(bridge.editRequested) as signal:
        bridge.editWork(1, 2, 2)
    assert signal.args == [1, {"project_id": 2, "activity_id": 2}]


def test_delete_hides_the_row_and_undo_brings_it_back_without_asking_kimai(bridge, qtbot):
    bridge.deleteEntry(2)
    assert bridge.entries.entry(2) is not None  # still known, only hidden
    assert bridge.entries.rowCount() == 3
    assert bridge.view["undo"] != ""
    with qtbot.assertNotEmitted(bridge.deleteRequested, wait=120):
        bridge.undoDelete()
    assert bridge.entries.rowCount() == 4
    assert bridge.view["undo"] == ""


def test_delete_reaches_kimai_after_the_undo_time(bridge, qtbot):
    with qtbot.waitSignal(bridge.deleteRequested, timeout=1000) as signal:
        bridge.deleteEntry(2)
    assert signal.args == [2]
    assert bridge.view["undo"] == ""


def test_a_second_delete_sends_the_first_at_once(bridge, qtbot):
    bridge.undo_ms = 10_000
    bridge.deleteEntry(1)
    with qtbot.waitSignal(bridge.deleteRequested, timeout=200) as signal:
        bridge.deleteEntry(2)
    assert signal.args == [1]


def test_quitting_sends_a_pending_delete(bridge, qtbot):
    bridge.undo_ms = 10_000
    bridge.deleteEntry(2)
    with qtbot.waitSignal(bridge.deleteRequested, timeout=200) as signal:
        bridge.flush_deletes()
    assert signal.args == [2]


def test_duplicate_fills_the_timer_bar_for_a_manual_entry(bridge, qtbot):
    with qtbot.waitSignal(bridge.prefill) as signal:
        bridge.duplicate(1)
    assert signal.args == [
        {"description": "Kalendarz dostępności pokoi", "projectId": 1, "activityId": 1, "billable": True}
    ]


def test_row_errors_are_kept_per_entry_and_cleared_by_the_next_edit(bridge, qtbot):
    bridge.show_row_error(1, "Opis jest za krótki")
    assert bridge.rowErrors == {"1": "Opis jest za krótki"}
    with qtbot.waitSignal(bridge.editRequested):
        bridge.editDescription(1, "Kalendarz dostępności pokoi i testy")
    assert bridge.rowErrors == {}


def test_choosing_a_project_asks_for_its_activities(bridge, qtbot):
    with qtbot.waitSignal(bridge.activitiesRequested) as signal:
        bridge.chooseProject(2)
    assert signal.args == [2]


def test_a_refresh_during_the_undo_time_keeps_the_row_hidden(bridge):
    bridge.undo_ms = 10_000
    bridge.deleteEntry(2)
    bridge.set_entries(build_rows([first(9, 1), first(11, 2)], WARSAW, date(2026, 9, 25), 0, PL), WARSAW)
    assert bridge.entries.rowCount() == 3  # week, day, entry 1: entry 2 waits for "Undo"
