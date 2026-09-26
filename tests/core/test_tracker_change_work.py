"""F-34: the running entry's project and activity can change (the add-on locks them)."""

from datetime import timedelta

import pytest

from dk_tracker.core.errors import TrackerError
from dk_tracker.core.settings import Memory

from .fakes import NOW, make_entry
from .test_tracker_refresh import make_tracker


def running_tracker(memory=None):
    tracker, client, saved = make_tracker(memory=memory)
    client.add(make_entry(7, NOW - timedelta(minutes=40), description="Formularz rezerwacji — walidacja dat"))
    tracker.load_catalog()
    tracker.refresh_full()
    return tracker, client


def updates(client):
    return [call for call in client.calls if call[0] == "update"]


def test_changing_the_project_saves_it_with_the_default_billable():
    tracker, client = running_tracker()
    snapshot = tracker.change_work(2, 1)  # "Administracja" belongs to a non-billable customer
    assert updates(client) == [("update", 7, {"project": 2, "activity": 1, "billable": False})]
    current = snapshot.current
    assert (current.project_id, current.project_name, current.activity_id) == (2, "Administracja", 1)
    assert current.billable is False
    assert snapshot.notice == "savedWork"


def test_changing_only_the_activity():
    tracker, client = running_tracker()
    snapshot = tracker.change_work(1, 2)
    assert updates(client) == [("update", 7, {"project": 1, "activity": 2, "billable": True})]
    assert snapshot.current.activity_name == "Spotkanie"


def test_nothing_is_sent_when_nothing_changes():
    tracker, client = running_tracker()
    tracker.change_work(1, 1)
    assert updates(client) == []


def test_without_billable_permission_the_flag_is_not_sent():
    tracker, client = running_tracker(Memory(billable_allowed=False))
    tracker.change_work(2, 1)
    assert updates(client) == [("update", 7, {"project": 2, "activity": 1})]


def test_a_refused_billable_locks_the_switch_and_the_change_is_saved_anyway():
    tracker, client = running_tracker()
    client.billable_forbidden = True
    snapshot = tracker.change_work(2, 1)
    assert updates(client)[-1] == ("update", 7, {"project": 2, "activity": 1})
    assert snapshot.current.project_id == 2
    assert snapshot.billable_allowed is False


def test_a_project_without_an_activity_is_refused():
    tracker, _client = running_tracker()
    with pytest.raises(TrackerError) as error:
        tracker.change_work(2, None)
    assert error.value.key == "errNoActivity"


def test_needs_a_running_entry():
    tracker, _client, _ = make_tracker()
    with pytest.raises(TrackerError):
        tracker.change_work(1, 1)
