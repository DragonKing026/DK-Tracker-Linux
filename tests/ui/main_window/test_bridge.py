"""Plan 5: `app`, the object the QML main window talks to — state in, actions out, undo."""

from dataclasses import replace
from datetime import UTC, date, datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from dk_tracker.core.entry_list import build_rows
from dk_tracker.core.i18n import Translator
from dk_tracker.core.tracker import Snapshot, Totals
from dk_tracker.ui.main_window.bridge import MainBridge
from dk_tracker.ui.theme import MAIN_DARK as DARK

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


def test_a_refresh_waits_while_a_field_is_being_edited(bridge):
    """Spec, section 5: the minute's refresh does not overwrite an edit in progress."""
    bridge.setEditing(True)
    bridge.set_entries(build_rows([first(8, 3)], WARSAW, date(2026, 9, 25), 0, PL), WARSAW)
    assert bridge.entries.entry(3) is None and bridge.entries.entry(1) is not None
    bridge.setEditing(False)
    assert bridge.entries.entry(3) is not None and bridge.entries.entry(1) is None


# -- review fixes ------------------------------------------------------------------------


def test_a_failed_load_clears_after_the_next_successful_one(bridge):
    """Review I1: a failed background load stuck in the error bar after the connection came back."""
    bridge.show_load_error("Brak połączenia")
    bridge.render(SNAPSHOT, configured=True, t=PL, now=NOW, tz=WARSAW)
    assert bridge.view["error"] == "Brak połączenia"
    bridge.set_entries(build_rows([first(9, 1)], WARSAW, date(2026, 9, 25), 0, PL), WARSAW)
    assert bridge.view["error"] == ""


def test_an_action_error_is_not_cleared_by_a_load(bridge):
    bridge.show_error("Wpis wyeksportowany")
    bridge.set_entries(build_rows([first(9, 1)], WARSAW, date(2026, 9, 25), 0, PL), WARSAW)
    assert bridge.view["error"] == "Wpis wyeksportowany"


def test_a_delete_keeps_its_entry_when_the_list_changes_meanwhile(bridge, qtbot):
    """Review I3: a search during the undo time replaced the list and the delete was lost."""
    bridge.undo_ms = 10_000
    bridge.deleteEntry(2)
    bridge.set_entries(build_rows([first(9, 1)], WARSAW, date(2026, 9, 25), 0, PL), WARSAW)
    with qtbot.waitSignal(bridge.deleteRequested) as signal:
        bridge.flush_deletes()
    assert signal.args == [2]
    assert bridge.deleted_entry(2).id == 2


def test_an_impossible_day_is_reported_not_raised(bridge, qtbot):
    """Review I6: date.fromisoformat raised inside the slot; the user saw nothing."""
    with qtbot.assertNotEmitted(bridge.addRequested):
        bridge.addManual("2026-13-01", "09:00", "10:00", "Opis wpisu ręcznego", 1, 1, None)
    assert bridge.view["error"] == PL("errInvalidDay")


def test_a_row_picker_has_its_own_activities(bridge, qtbot):
    """Review I4: one activity list for the timer bar and the rows — a row's project changed the bar's."""
    with qtbot.waitSignal(bridge.rowActivitiesRequested) as signal:
        bridge.chooseRowProject(2)
    assert signal.args == [2]
    bridge.set_row_activities(CLIENT.activities_list)
    assert bridge.rowActivities.rowCount() == 2
    assert bridge.activities.rowCount() == 0


# -- settings as a page (live test of 0.10.0) --------------------------------------------


def test_the_window_starts_on_the_entries_and_switches_to_the_settings(bridge):
    assert bridge.view["page"] == "entries"
    bridge.show_page("settings")
    assert bridge.view["page"] == "settings"
    bridge.showPage("entries")
    assert bridge.view["page"] == "entries"


def test_without_a_configuration_only_the_settings_page_is_shown(bridge):
    bridge.render(Snapshot(), configured=False, t=PL, now=NOW, tz=WARSAW)
    assert bridge.view["page"] == "settings"
    bridge.showPage("entries")
    assert bridge.view["page"] == "settings"


def test_the_settings_page_has_its_form(bridge):
    assert bridge.settingsForm is bridge.settings_form


# -- the edit window (live test of 0.10.0) ------------------------------------------------


def details(**changes):
    from dk_tracker.core.models import EntryDetails

    begin = datetime(2026, 9, 25, 9, tzinfo=WARSAW)
    base = EntryDetails(
        id=1, begin=begin, end=begin + timedelta(minutes=90), project_id=1, activity_id=2,
        description="Kalendarz dostępności pokoi\nwidok tygodnia", tags=("frontend", "pilne"), billable=True,
        exported=False, break_seconds=0,
        meta=(("ticket", "KSEF-12"),),
    )  # fmt: skip
    return replace(base, **changes)


def test_clicking_a_row_asks_for_the_entry(bridge, qtbot):
    with qtbot.waitSignal(bridge.entryOpenRequested) as signal:
        bridge.openEntry(2)
    assert signal.args == [2]


def test_the_editor_shows_every_option_of_the_entry(bridge):
    bridge.open_editor(details(), WARSAW)
    editor = bridge.editor
    assert editor["open"] is True and editor["entryId"] == 1
    assert (editor["day"], editor["begin"], editor["end"], editor["duration"]) == (
        "2026-09-25",
        "09:00",
        "10:30",
        "1:30",
    )
    assert editor["description"] == "Kalendarz dostępności pokoi\nwidok tygodnia"
    assert editor["tags"] == "frontend, pilne"
    assert not {"ratesVisible", "fixedRate", "hourlyRate"} & set(editor)  # as Kimai's own form: no rates
    assert editor["meta"] == [{"name": "ticket", "value": "KSEF-12"}]


def test_saving_the_editor_sends_what_was_typed(bridge, qtbot):
    bridge.open_editor(details(), WARSAW)
    values = dict(bridge.editor, day="2026-09-24", tags="frontend", meta=[{"name": "ticket", "value": "X"}])
    with qtbot.waitSignal(bridge.entrySaveRequested) as signal:
        bridge.saveEntry(values)
    entry_id, sent = signal.args
    assert entry_id == 1
    assert sent["day"] == date(2026, 9, 24) and sent["tags"] == "frontend" and sent["meta"] == {"ticket": "X"}
    assert (sent["project_id"], sent["activity_id"]) == (1, 2)
    assert bridge.editor["busy"] is True


def test_an_error_keeps_the_editor_open(bridge):
    bridge.open_editor(details(), WARSAW)
    bridge.editor_error("Kimai odmówił")
    assert bridge.editor["open"] is True and bridge.editor["error"] == "Kimai odmówił"
    assert bridge.editor["busy"] is False
    bridge.close_editor()
    assert bridge.editor["open"] is False


def test_an_impossible_day_in_the_editor_is_reported(bridge, qtbot):
    bridge.open_editor(details(), WARSAW)
    with qtbot.assertNotEmitted(bridge.entrySaveRequested):
        bridge.saveEntry(dict(bridge.editor, day="2026-02-30"))
    assert bridge.editor["error"] == PL("errInvalidDay")
