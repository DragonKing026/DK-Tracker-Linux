"""F-33: searching all of the user's entries in Kimai (only the description is searched there)."""

from dataclasses import replace
from datetime import timedelta

import pytest

from ws_tracker.core.errors import TrackerError

from .fakes import NOW, make_entry
from .test_tracker_refresh import make_tracker


def fill(client):
    old = client.add(
        make_entry(
            1,
            NOW - timedelta(days=90, hours=2),
            NOW - timedelta(days=90),
            description="Rezerwacja pokoi — stary formularz",
        )
    )
    new = client.add(
        make_entry(
            2,
            NOW - timedelta(days=2, hours=1),
            NOW - timedelta(days=2),
            description="Rezerwacja sal konferencyjnych",
        )
    )
    client.add(
        make_entry(
            3, NOW - timedelta(days=1, hours=1), NOW - timedelta(days=1), description="Spotkanie z klientem"
        )
    )
    running = client.add(
        make_entry(4, NOW - timedelta(minutes=30), description="Rezerwacja — poprawki kalendarza")
    )
    return old, new, running


def test_search_returns_finished_entries_newest_first():
    tracker, client, _ = make_tracker()
    old, new, _running = fill(client)
    assert tracker.search("  rezerwacja  ") == (new, old)  # the running entry sits in the tracker bar
    assert ("search", "rezerwacja", 50) in client.calls


def test_search_needs_two_characters():
    tracker, client, _ = make_tracker()
    assert tracker.search(" r ") == ()
    assert not [call for call in client.calls if call[0] == "search"]


def test_billable_works_on_a_search_result_outside_the_recent_list():
    tracker, client, _ = make_tracker()
    old, _new, _running = fill(client)
    client.entries[old.id] = replace(old, exported=True)
    assert tracker.snapshot.recent == ()  # known only from the search
    tracker.search("stary")
    with pytest.raises(TrackerError) as error:
        tracker.set_billable(old.id, False)
    assert error.value.key == "errExported"
