from datetime import UTC, datetime, timedelta

from kimai_tray.core.errors import ApiError, ErrorKind
from kimai_tray.core.models import Entry
from kimai_tray.core.notification_policy import (
    ACTION,
    CONNECTION,
    LONG_TIMER,
    PolicyState,
    action_confirmation,
    evaluate,
)
from kimai_tray.core.settings import Settings
from kimai_tray.core.tracker import Snapshot

BEGIN = datetime(2026, 9, 25, 6, 0, tzinfo=UTC)
ENTRY = Entry(
    7,
    BEGIN,
    None,
    0,
    "Formularz rezerwacji pokoi",
    True,
    1,
    "Moduł rezerwacji",
    None,
    1,
    "Programowanie",
    "pl",
)
SETTINGS = Settings()


def run(snapshot, state=None, *, hours, settings=SETTINGS):
    return evaluate(snapshot, settings, state or PolicyState(), BEGIN + timedelta(hours=hours))


def test_nothing_when_idle():
    assert run(Snapshot(), hours=10) == ([], PolicyState())


def test_long_timer_fires_at_threshold_then_every_hour():
    running = Snapshot(running=(ENTRY,))
    notes, state = run(running, hours=7.99)
    assert notes == []
    notes, state = run(running, state, hours=8)
    assert [n.id for n in notes] == [LONG_TIMER]
    assert notes[0].title_key == "notifLongTimerTitle"
    assert notes[0].params == {
        "time": "8:00",
        "project": "Moduł rezerwacji",
        "description": ENTRY.description,
    }
    assert notes[0].actions == ("stop", "keep")
    notes, state = run(running, state, hours=8.5)
    assert notes == []
    notes, state = run(running, state, hours=9)
    assert [n.params["time"] for n in notes] == ["9:00"]


def test_app_started_late_fires_once_and_moves_threshold_past_now():
    notes, state = run(Snapshot(running=(ENTRY,)), hours=10.5)
    assert len(notes) == 1
    assert state.next_threshold[ENTRY.id] == 11 * 3600


def test_long_timer_disabled():
    assert run(Snapshot(running=(ENTRY,)), hours=12, settings=Settings(long_timer_hours=0))[0] == []


def test_state_forgets_entries_that_stopped():
    _, state = run(Snapshot(running=(ENTRY,)), hours=8)
    _, state = run(Snapshot(), state, hours=9)
    assert state.next_threshold == {}


def test_connection_lost_after_three_failures_and_restored_once():
    error = ApiError(ErrorKind.CONNECTION, 0)
    notes, state = run(Snapshot(error=error, failures=2), hours=0)
    assert notes == []
    notes, state = run(Snapshot(error=error, failures=3), state, hours=0)
    assert [(n.id, n.title_key) for n in notes] == [(CONNECTION, "notifConnectionLost")]
    notes, state = run(Snapshot(error=error, failures=4), state, hours=0)
    assert notes == []
    notes, state = run(Snapshot(), state, hours=0)
    assert [(n.id, n.title_key) for n in notes] == [(CONNECTION, "notifConnectionRestored")]
    assert state.connection_alerted is False


def test_auth_failure_alerts_immediately_with_settings_action():
    notes, _ = run(Snapshot(error=ApiError(ErrorKind.AUTH, 401), failures=1), hours=0)
    assert [(n.title_key, n.actions) for n in notes] == [("notifAuthFailed", ("settings",))]


def test_connection_alerts_disabled():
    settings = Settings(notify_connection=False)
    assert run(Snapshot(error=ApiError(ErrorKind.AUTH, 401), failures=5), hours=0, settings=settings)[0] == []


def test_action_confirmation():
    now = BEGIN + timedelta(hours=1, minutes=22)
    started = action_confirmation("start", ENTRY, SETTINGS, now)
    assert (started.id, started.title_key) == (ACTION, "notifStarted")
    assert started.params == {"description": ENTRY.description, "project": "Moduł rezerwacji"}
    stopped = action_confirmation("stop", ENTRY, SETTINGS, now)
    assert (stopped.title_key, stopped.params["time"]) == ("notifStopped", "1:22")
    assert action_confirmation("start", ENTRY, Settings(notify_menu_actions=False), now) is None
