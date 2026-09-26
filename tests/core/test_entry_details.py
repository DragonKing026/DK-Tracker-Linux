"""Every option of one entry, for the edit window (live test of 0.10.0): what Kimai returns for
`GET /api/timesheets/{id}`, and a save that sends only what changed."""

import json
from dataclasses import replace
from datetime import date, timedelta

import httpx
import pytest

from dk_tracker.core.errors import ApiError, ErrorKind, TrackerError
from dk_tracker.core.models import EntryDetails

from .fakes import EXTRA_FIELDS, NOW, make_entry
from .test_kimai_client import client_for
from .test_tracker_refresh import make_tracker

GOOD = "Formularz rezerwacji — walidacja dat"
AT_9 = NOW.replace(hour=7, minute=0, second=0)  # 09:00 in Warsaw
# As Kimai 2.67.0 answers an account that may see rates (checked on the Docker instance).
RAW = {
    "activity": 1, "project": 1, "user": 2, "tags": ["frontend", "pilne"], "id": 92,
    "begin": "2026-09-25T09:00:00+0200", "end": "2026-09-25T10:30:00+0200", "duration": 5400,
    "break": 0, "description": GOOD, "rate": 0.0, "internalRate": 0.0, "fixedRate": None,
    "hourlyRate": 120.0, "exported": False, "billable": True,
    "metaFields": [{"name": "ticket", "value": "KSEF-12"}],
}  # fmt: skip


def test_details_read_everything_kimai_returns():
    details = EntryDetails.from_api(RAW)
    assert (details.id, details.project_id, details.activity_id, details.description) == (92, 1, 1, GOOD)
    assert details.tags == ("frontend", "pilne")
    assert details.meta == (("ticket", "KSEF-12"),)
    assert details.break_seconds == 0 and details.billable and not details.exported


def test_the_client_reads_one_entry_and_sets_a_meta_field():
    client, rec = client_for(lambda r: httpx.Response(200, json=RAW))
    assert client.entry_details(92).tags == ("frontend", "pilne")
    assert (rec.last.method, rec.last.url.path) == ("GET", "/api/timesheets/92")
    client.set_meta(92, "ticket", "KSEF-13")
    assert (rec.last.method, rec.last.url.path) == ("PATCH", "/api/timesheets/92/meta")
    assert json.loads(rec.last.read()) == {"name": "ticket", "value": "KSEF-13"}


# -- saving ------------------------------------------------------------------------------


def edited(tracker, client, **values):
    entry = client.add(make_entry(92, AT_9, AT_9 + timedelta(minutes=90), description=GOOD))
    client.details[92] = {"tags": ["frontend"], "metaFields": [{"name": "ticket", "value": "KSEF-12"}]}
    details = tracker.entry_details(entry)
    base = {
        "day": date(2026, 9, 25), "begin": "09:00", "end": "10:30", "project_id": 1, "activity_id": 1,
        "description": GOOD, "tags": "frontend", "billable": True,
        "meta": {"ticket": "KSEF-12"},
    }  # fmt: skip
    return tracker.save_details(details, {**base, **values})


def updates(client):
    return [call[2] for call in client.calls if call[0] == "update"]


def test_nothing_changed_sends_nothing():
    tracker, client, _ = make_tracker()
    edited(tracker, client)
    assert updates(client) == []


def test_only_what_changed_is_sent():
    tracker, client, _ = make_tracker()
    snapshot = edited(tracker, client, tags="frontend, pilne ,", end="11:00")
    assert updates(client) == [{"tags": "frontend,pilne", "end": "2026-09-25T11:00:00"}]
    assert snapshot.notice == "savedEntry"


def test_a_meta_field_goes_to_its_own_endpoint():
    tracker, client, _ = make_tracker()
    edited(tracker, client, meta={"ticket": "KSEF-13"})
    assert ("set_meta", 92, "ticket", "KSEF-13") in client.calls


def test_another_day_moves_the_entry():
    tracker, client, _ = make_tracker()
    edited(tracker, client, day=date(2026, 9, 24))
    assert updates(client) == [{"begin": "2026-09-24T09:00:00", "end": "2026-09-24T10:30:00"}]


@pytest.mark.parametrize(
    ("values", "key"),
    [
        ({"end": "08:00"}, "errEndBeforeBegin"),
        ({"description": "krótko"}, "errDescShort"),
    ],
)
def test_rules_are_checked_before_asking_kimai(values, key):
    tracker, client, _ = make_tracker()
    with pytest.raises(TrackerError) as error:
        edited(tracker, client, **values)
    assert error.value.key == key
    assert updates(client) == []


def test_fields_the_account_may_not_change_are_dropped_and_named():
    """Kimai rejects the whole form ("extra fields") and does not say which field: retry without
    the fields that depend on permissions, save the rest, say what was not saved."""
    tracker, client, _ = make_tracker()
    client.fail["update"] = [ApiError(ErrorKind.REJECTED, 400, EXTRA_FIELDS)]
    snapshot = edited(tracker, client, billable=False, description=f"{GOOD} — poprawka")
    assert updates(client) == [
        {"description": f"{GOOD} — poprawka", "billable": False},
        {"description": f"{GOOD} — poprawka"},
    ]
    assert snapshot.notice == "errFieldsDenied"


def test_an_exported_entry_is_not_saved():
    tracker, client, _ = make_tracker()
    entry = client.add(replace(make_entry(93, AT_9, AT_9 + timedelta(hours=1)), exported=True))
    details = replace(tracker.entry_details(entry), exported=True)
    with pytest.raises(TrackerError) as error:
        tracker.save_details(details, {"description": GOOD})
    assert error.value.key == "errExported"


def test_hours_with_seconds_are_not_sent_when_the_minutes_did_not_change():
    """Kimai keeps seconds (a start "now"); the window shows minutes: the same minutes are no change."""
    tracker, client, _ = make_tracker()
    begin = AT_9 + timedelta(seconds=3)
    entry = client.add(make_entry(94, begin, begin + timedelta(minutes=90), description=GOOD))
    details = tracker.entry_details(entry)
    tracker.save_details(details, {"day": date(2026, 9, 25), "begin": "09:00", "end": "10:30", "tags": "x"})
    assert updates(client) == [{"tags": "x"}]


def test_tags_kimai_dropped_are_named():
    """Kimai 2.67.0 silently leaves out a tag that does not exist when the account may not create
    tags (checked on the Docker instance): the save reads the entry again and says so."""
    tracker, client, _ = make_tracker()
    client.known_tags = {"frontend"}
    snapshot = edited(tracker, client, tags="frontend, całkiem-nowy")
    assert snapshot.notice == "errTagsDropped"
    assert snapshot.notice_params == (("tags", "całkiem-nowy"),)
