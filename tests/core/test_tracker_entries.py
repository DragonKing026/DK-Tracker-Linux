"""Plan 5: the main window's entries — a period, typed in by hand, edited in place, deleted."""

from dataclasses import replace
from datetime import date, timedelta

import pytest

from dk_tracker.core.errors import TrackerError
from dk_tracker.core.settings import Memory

from .fakes import NOW, make_entry
from .test_tracker_refresh import make_tracker

GOOD = "Formularz rezerwacji — walidacja dat"
FRIDAY = date(2026, 9, 25)  # NOW is Friday 2026-09-25, 16:04 UTC (18:04 in Warsaw)


def calls(client, name):
    return [call for call in client.calls if call[0] == name]


def booked(client):
    """Morning and afternoon on Friday, one on Monday, one the week before, one running."""
    h = timedelta(hours=1)
    morning = client.add(make_entry(1, NOW - 9 * h, NOW - 8 * h, description=GOOD))
    afternoon = client.add(make_entry(2, NOW - 3 * h, NOW - 2 * h, description=GOOD))
    monday = client.add(make_entry(3, NOW - 4 * 24 * h, NOW - 4 * 24 * h + h, description=GOOD))
    earlier = client.add(make_entry(4, NOW - 9 * 24 * h, NOW - 9 * 24 * h + h, description=GOOD))
    client.add(make_entry(5, NOW - h / 2, description=GOOD))
    return morning, afternoon, monday, earlier


# -- a period ------------------------------------------------------------------


def test_entries_of_a_period_are_the_finished_ones_newest_first():
    tracker, client, _ = make_tracker()
    morning, afternoon, monday, _earlier = booked(client)
    entries = tracker.entries(date(2026, 9, 21), FRIDAY)
    assert entries == (afternoon, morning, monday)  # the running entry sits in the timer bar
    assert calls(client, "range")[-1][1:] == ("2026-09-21T00:00:00", "2026-09-25T23:59:59")


# -- typed in by hand ----------------------------------------------------------


def test_add_entry_books_the_typed_hours_on_that_day_in_the_kimai_zone():
    tracker, client, _ = make_tracker()
    snapshot = tracker.add_entry(
        day=FRIDAY,
        begin="09:00",
        end="10:30",
        project_id=1,
        activity_id=2,
        description=f"  {GOOD} ",
        billable=None,
    )
    assert calls(client, "create_entry") == [
        ("create_entry", 1, 2, GOOD, "2026-09-25T09:00:00", "2026-09-25T10:30:00", None)
    ]
    assert snapshot.notice == "savedEntry"


@pytest.mark.parametrize(
    ("begin", "end", "key"),
    [
        ("10:30", "09:00", "errEndBeforeBegin"),
        ("10:00", "10:00", "errEndBeforeBegin"),
        ("9", "10:00", "errInvalidTime"),
    ],
)
def test_add_entry_refuses_impossible_hours(begin, end, key):
    tracker, client, _ = make_tracker()
    with pytest.raises(TrackerError) as error:
        tracker.add_entry(
            day=FRIDAY, begin=begin, end=end, project_id=1, activity_id=2, description=GOOD, billable=None
        )
    assert error.value.key == key
    assert calls(client, "create_entry") == []


@pytest.mark.parametrize(
    ("project", "activity", "description", "key"),
    [(None, 2, GOOD, "errNoProject"), (1, None, GOOD, "errNoActivity"), (1, 2, "krótko", "errDescShort")],
)
def test_add_entry_follows_the_same_rules_as_a_start(project, activity, description, key):
    tracker, client, _ = make_tracker()
    with pytest.raises(TrackerError) as error:
        tracker.add_entry(
            day=FRIDAY,
            begin="09:00",
            end="10:00",
            project_id=project,
            activity_id=activity,
            description=description,
            billable=None,
        )
    assert error.value.key == key


def test_add_entry_with_a_refused_billable_is_saved_without_it_and_locks_the_switch():
    tracker, client, _ = make_tracker()
    client.billable_forbidden = True
    snapshot = tracker.add_entry(
        day=FRIDAY, begin="09:00", end="10:00", project_id=1, activity_id=2, description=GOOD, billable=False
    )
    assert [call[-1] for call in calls(client, "create_entry")] == [False, None]
    assert snapshot.billable_allowed is False
    assert snapshot.notice == "errBillableDenied"


# -- edited in place -----------------------------------------------------------


def test_edit_entry_sends_only_what_changed():
    tracker, client, _ = make_tracker()
    morning, *_ = booked(client)
    snapshot = tracker.edit_entry(
        morning,
        description=f"{GOOD} i testy",
        begin="09:15",
        end=None,
        project_id=2,
        activity_id=2,
        billable=False,
    )
    assert calls(client, "update") == [
        (
            "update",
            1,
            {
                "description": f"{GOOD} i testy",
                "project": 2,
                "activity": 2,
                "begin": "2026-09-25T09:15:00",
                "billable": False,
            },
        )
    ]
    assert snapshot.notice == "savedEntry"


def test_edit_entry_keeps_the_day_and_checks_the_hours():
    tracker, client, _ = make_tracker()
    morning, *_ = booked(client)  # 09:04–10:04 in Warsaw
    tracker.edit_entry(morning, end="12:00")
    assert calls(client, "update")[-1][2] == {"end": "2026-09-25T12:00:00"}
    with pytest.raises(TrackerError) as error:
        tracker.edit_entry(morning, begin="11:00", end="10:00")
    assert error.value.key == "errEndBeforeBegin"


def test_edit_without_a_change_sends_nothing():
    tracker, client, _ = make_tracker()
    morning, *_ = booked(client)
    tracker.edit_entry(morning, description=GOOD, project_id=1, activity_id=1, billable=True)
    assert calls(client, "update") == []


def test_edit_checks_the_description_like_a_start():
    tracker, client, _ = make_tracker()
    morning, *_ = booked(client)
    with pytest.raises(TrackerError) as error:
        tracker.edit_entry(morning, description="poprawki")
    assert (error.value.key, error.value.params) == ("errDescGeneric", {"word": "poprawki"})


def test_an_exported_entry_is_not_edited_or_deleted():
    tracker, client, _ = make_tracker()
    morning, *_ = booked(client)
    exported = replace(morning, exported=True)
    for action in (
        lambda: tracker.edit_entry(exported, description=f"{GOOD} 2"),
        lambda: tracker.delete_entry(exported),
    ):
        with pytest.raises(TrackerError) as error:
            action()
        assert error.value.key == "errExported"
    assert calls(client, "update") == calls(client, "delete_entry") == []


def test_billable_without_permission_is_refused_before_asking_kimai():
    tracker, client, _ = make_tracker(memory=Memory(billable_allowed=False))
    morning, *_ = booked(client)
    with pytest.raises(TrackerError) as error:
        tracker.edit_entry(morning, billable=False)
    assert error.value.key == "billableLocked"


def test_a_billable_refused_by_kimai_locks_the_switch():
    tracker, client, _ = make_tracker()
    morning, *_ = booked(client)
    client.billable_forbidden = True
    with pytest.raises(TrackerError) as error:
        tracker.edit_entry(morning, billable=False)
    assert error.value.key == "errBillableDenied"
    assert tracker.snapshot.billable_allowed is False


# -- deleted -------------------------------------------------------------------


def test_delete_entry():
    tracker, client, _ = make_tracker()
    morning, *_ = booked(client)
    tracker.delete_entry(morning)
    assert calls(client, "delete_entry") == [("delete_entry", 1)]
    assert 1 not in client.entries


# -- the days the clocks change (Kimai's zone: Europe/Warsaw) --------------------


@pytest.mark.parametrize(
    ("day", "begin", "end"),
    [
        (date(2026, 10, 25), "02:30", "02:45"),  # 02:00–03:00 happens twice: the first one is meant
        (date(2026, 10, 25), "01:30", "03:30"),
        (date(2026, 3, 29), "01:30", "03:30"),  # 02:00–03:00 does not exist
    ],
)
def test_hours_typed_on_a_day_the_clocks_change_are_sent_as_typed(day, begin, end):
    tracker, client, _ = make_tracker()
    tracker.add_entry(
        day=day, begin=begin, end=end, project_id=1, activity_id=2, description=GOOD, billable=None
    )
    [call] = calls(client, "create_entry")
    assert call[4:6] == (f"{day}T{begin}:00", f"{day}T{end}:00")
