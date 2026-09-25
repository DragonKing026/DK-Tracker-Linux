from datetime import UTC, timedelta

import pytest

from kimai_tray.core.errors import ApiError, ErrorKind, TrackerError
from kimai_tray.core.settings import Memory, Settings

from .fakes import NOW, FakeClient, make_entry
from .test_tracker_refresh import make_tracker

GOOD = "Formularz rezerwacji — walidacja dat"


def starts(client):
    return [call for call in client.calls if call[0] == "start"]


def test_start_sends_now_in_kimai_account_zone():
    tracker, client, saved = make_tracker()
    snapshot = tracker.start(project_id=1, activity_id=1, description=f"  {GOOD}  ", billable=None)
    assert starts(client) == [("start", 1, 1, GOOD, "2026-09-25T18:04:02", None)]
    assert snapshot.current.description == GOOD
    assert (snapshot.notice, tracker.memory.last_project, tracker.memory.last_activity) == (None, 1, 1)
    assert saved[-1].last_project == 1


def test_start_for_utc_account_on_warsaw_machine_uses_utc_wall_clock():
    tracker, client, _ = make_tracker(FakeClient("UTC"))
    tracker.start(project_id=1, activity_id=1, description=GOOD, billable=None)
    assert starts(client)[0][4] == "2026-09-25T16:04:02"


@pytest.mark.parametrize(
    ("project", "activity", "description", "key", "params"),
    [
        (None, 1, GOOD, "errNoProject", {}),
        (1, None, GOOD, "errNoActivity", {}),
        (1, 1, "poprawki", "errDescGeneric", {"word": "poprawki"}),
        (1, 1, "krótko", "errDescShort", {"chars": 15}),
    ],
)
def test_start_refusals_never_reach_kimai(project, activity, description, key, params):
    tracker, client, _ = make_tracker()
    with pytest.raises(TrackerError) as caught:
        tracker.start(project_id=project, activity_id=activity, description=description, billable=None)
    assert (caught.value.key, caught.value.params) == (key, params)
    assert starts(client) == []


def test_start_retries_without_billable_and_locks_switch():
    tracker, client, saved = make_tracker()
    client.billable_forbidden = True
    snapshot = tracker.start(project_id=1, activity_id=1, description=GOOD, billable=False)
    assert [call[5] for call in starts(client)] == [False, None]
    assert (snapshot.notice, snapshot.billable_allowed, snapshot.current is not None) == (
        "errBillableDenied",
        False,
        True,
    )
    assert saved[-1].billable_allowed is False
    tracker.start(project_id=1, activity_id=1, description=GOOD, billable=True)
    assert starts(client)[-1][5] is None  # locked: not even tried


def test_start_other_rejection_is_not_retried():
    tracker, client, _ = make_tracker()
    client.fail["start"] = [ApiError(ErrorKind.REJECTED, 400, "Duration cannot be negative.")]
    with pytest.raises(ApiError):
        tracker.start(project_id=1, activity_id=1, description=GOOD, billable=False)
    assert len(starts(client)) == 1


def test_start_timeout_after_save_counts_as_started():
    tracker, client, _ = make_tracker()
    client.start_timeout = "after"
    snapshot = tracker.start(project_id=1, activity_id=1, description=GOOD, billable=None)
    assert snapshot.current.description == GOOD
    assert len(starts(client)) == 1  # never re-posted


def test_start_timeout_before_save_is_an_error():
    tracker, client, _ = make_tracker()
    client.start_timeout = "before"
    with pytest.raises(ApiError) as caught:
        tracker.start(project_id=1, activity_id=1, description=GOOD, billable=None)
    assert caught.value.kind is ErrorKind.TIMEOUT
    assert len(starts(client)) == 1


def test_stop_now():
    tracker, client, _ = make_tracker()
    running = client.add(make_entry(1, NOW - timedelta(hours=1)))
    tracker.refresh_active()
    snapshot = tracker.stop()
    assert ("stop", running.id) in client.calls
    assert snapshot.running == ()


def test_stop_with_end_time_in_account_zone():
    tracker, client, _ = make_tracker()
    client.add(make_entry(1, NOW - timedelta(hours=2)))  # began 16:04 Warsaw
    tracker.refresh_active()
    tracker.stop(end="17:30")
    assert ("update", 1, {"end": "2026-09-25T17:30:00"}) in client.calls


def test_stop_with_end_before_begin():
    tracker, client, _ = make_tracker()
    client.add(make_entry(1, NOW - timedelta(hours=2)))
    tracker.refresh_active()
    with pytest.raises(TrackerError) as caught:
        tracker.stop(end="15:00")
    assert caught.value.key == "errEndBeforeBegin"


@pytest.mark.parametrize("value", ["25:00", "7", "ab:cd", "07:60"])
def test_stop_with_invalid_end_time(value):
    tracker, client, _ = make_tracker()
    client.add(make_entry(1, NOW - timedelta(hours=2)))
    tracker.refresh_active()
    with pytest.raises(TrackerError) as caught:
        tracker.stop(end=value)
    assert caught.value.key == "errInvalidTime"


def test_stop_when_nothing_runs():
    tracker, _, _ = make_tracker()
    tracker.refresh_active()
    with pytest.raises(TrackerError) as caught:
        tracker.stop()
    assert caught.value.key == "errNothingRunning"


def test_resume_switches_and_repeats_billable():
    tracker, client, _ = make_tracker()
    old = client.add(make_entry(1, NOW - timedelta(days=1), NOW - timedelta(hours=20), billable=False))
    current = client.add(make_entry(2, NOW - timedelta(minutes=10)))
    tracker.refresh_full()
    snapshot = tracker.resume(old)
    assert ("stop", current.id) in client.calls
    assert starts(client)[-1][1:4] == (old.project_id, old.activity_id, old.description)
    assert starts(client)[-1][5] is False
    assert snapshot.current.description == old.description


def test_resume_refused_before_anything_is_stopped():
    tracker, client, _ = make_tracker()
    old = client.add(make_entry(1, NOW - timedelta(days=1), NOW - timedelta(hours=20), description="fix"))
    client.add(make_entry(2, NOW - timedelta(minutes=10)))
    tracker.refresh_full()
    with pytest.raises(TrackerError):
        tracker.resume(old)
    assert not any(call[0] == "stop" for call in client.calls)


def test_update_description_rules_and_merge():
    tracker, client, _ = make_tracker()
    client.add(make_entry(1, NOW - timedelta(minutes=10)))
    tracker.refresh_active()
    assert tracker.update_description("Formularz rezerwacji pokoi") is None  # unchanged
    assert tracker.update_description("fix", quiet=True) is None
    with pytest.raises(TrackerError):
        tracker.update_description("fix")
    snapshot = tracker.update_description("Kalendarz dostępności pokoi")
    assert snapshot.current.description == "Kalendarz dostępności pokoi"
    assert snapshot.current.project_name == "Moduł rezerwacji"  # kept despite id-only reply
    assert snapshot.notice == "savedDescription"


def test_update_begin():
    tracker, client, _ = make_tracker()
    client.add(make_entry(1, NOW - timedelta(minutes=10)))
    tracker.refresh_active()
    with pytest.raises(TrackerError) as caught:
        tracker.update_begin("19:00")  # later than 18:04 now
    assert caught.value.key == "errBeginFuture"
    with pytest.raises(TrackerError) as caught:
        tracker.update_begin("7")
    assert caught.value.key == "errInvalidTime"
    snapshot = tracker.update_begin("17:00")
    assert ("update", 1, {"begin": "2026-09-25T17:00:00"}) in client.calls
    assert snapshot.notice == "savedTime"
    assert snapshot.current.begin.astimezone(UTC).hour == 15  # 17:00 Warsaw = 15:00 UTC


def test_set_billable_on_recent_entry():
    tracker, client, _ = make_tracker()
    client.add(make_entry(1, NOW - timedelta(hours=3), NOW - timedelta(hours=2)))
    tracker.refresh_full()
    snapshot = tracker.set_billable(1, False)
    assert snapshot.recent[0].billable is False
    assert snapshot.notice == "savedBillable"


def test_set_billable_denied_locks():
    tracker, client, saved = make_tracker()
    client.add(make_entry(1, NOW - timedelta(hours=3), NOW - timedelta(hours=2)))
    client.billable_forbidden = True
    tracker.refresh_full()
    with pytest.raises(TrackerError) as caught:
        tracker.set_billable(1, False)
    assert caught.value.key == "errBillableDenied"
    assert saved[-1].billable_allowed is False
    with pytest.raises(TrackerError) as caught:
        tracker.set_billable(1, False)
    assert caught.value.key == "billableLocked"


def test_apply_settings_clears_billable_lock_and_uses_new_client():
    tracker, _, saved = make_tracker(memory=Memory(billable_allowed=False))
    other = FakeClient()
    snapshot = tracker.apply_settings(Settings(url="https://inny.test/"), other)
    assert snapshot.billable_allowed is True
    assert saved[-1].billable_allowed is True
    assert tracker.settings.url == "https://inny.test"
    assert ("me",) in other.calls


def test_failed_resume_does_not_leave_a_stale_running_entry():
    tracker, client, _ = make_tracker()
    old = client.add(make_entry(1, NOW - timedelta(days=1), NOW - timedelta(hours=20)))
    client.add(make_entry(2, NOW - timedelta(minutes=10)))
    tracker.refresh_full()
    client.fail["start"] = [ApiError(ErrorKind.SERVER, 500)]
    with pytest.raises(ApiError):
        tracker.resume(old)
    assert tracker.snapshot.running == ()  # entry 2 was stopped before the start failed


def test_memory_that_cannot_be_saved_never_fails_an_action(caplog):
    client = FakeClient()

    def disk_full(memory):
        raise OSError(28, "No space left on device")

    from kimai_tray.core.tracker import Tracker

    tracker = Tracker(
        client,
        Settings(),
        Memory(),
        save_memory=disk_full,
        now=lambda: client.now,
        local_now=lambda: client.now.astimezone(UTC),
    )
    snapshot = tracker.start(
        project_id=1, activity_id=1, description=GOOD, billable=None
    )  # also saves locale
    assert snapshot.current.description == GOOD
    assert (tracker.memory.last_project, tracker.memory.kimai_locale) == (1, "pl")  # kept in memory
    assert len([call for call in client.calls if call[0] == "start"]) == 1
    assert "No space left on device" in caplog.text


def test_exported_entry_billable_is_refused_before_asking_kimai():
    from dataclasses import replace

    tracker, client, _ = make_tracker()
    client.add(replace(make_entry(1, NOW - timedelta(hours=3), NOW - timedelta(hours=2)), exported=True))
    tracker.refresh_full()
    with pytest.raises(TrackerError) as caught:
        tracker.set_billable(1, False)
    assert caught.value.key == "errExported"
    assert not any(call[0] == "update" for call in client.calls)
