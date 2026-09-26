"""Plan 5: finished entries for the main window — a whole period, created with an end, deleted."""

import json

import httpx
import pytest

from dk_tracker.core.errors import ApiError, ErrorKind

from .test_kimai_client import ENTRY, client_for


def test_range_asks_for_full_objects_so_rows_can_name_project_and_activity():
    client, rec = client_for(lambda r: httpx.Response(200, json=[ENTRY]))
    client.range("2026-09-21T00:00:00", "2026-09-27T23:59:59")
    assert dict(rec.last.url.params)["full"] == "true"


def test_create_entry_posts_begin_and_end():
    client, rec = client_for(lambda r: httpx.Response(200, json=dict(ENTRY, end="2026-09-25T17:34:00+0000")))
    entry = client.create_entry(
        project_id=1,
        activity_id=2,
        description="Uzupełnienie wpisu z przedpołudnia",
        begin="2026-09-25T09:00:00",
        end="2026-09-25T10:30:00",
        billable=None,
    )
    assert rec.last.method == "POST" and rec.last.url.path == "/api/timesheets"
    assert json.loads(rec.last.read()) == {
        "begin": "2026-09-25T09:00:00",
        "end": "2026-09-25T10:30:00",
        "project": 1,
        "activity": 2,
        "description": "Uzupełnienie wpisu z przedpołudnia",
    }
    assert entry.end is not None


def test_create_entry_sends_billable_only_when_chosen():
    client, rec = client_for(lambda r: httpx.Response(200, json=ENTRY))
    client.create_entry(project_id=1, activity_id=2, description="x" * 20, begin="a", end="b", billable=False)
    assert json.loads(rec.last.read())["billable"] is False


def test_delete_entry():
    client, rec = client_for(lambda r: httpx.Response(204))
    client.delete_entry(8)
    assert (rec.last.method, rec.last.url.path) == ("DELETE", "/api/timesheets/8")


def test_delete_of_a_foreign_or_exported_entry_is_forbidden():
    client, _ = client_for(lambda r: httpx.Response(403, json={"message": "Access denied."}))
    with pytest.raises(ApiError) as error:
        client.delete_entry(8)
    assert error.value.kind is ErrorKind.FORBIDDEN
