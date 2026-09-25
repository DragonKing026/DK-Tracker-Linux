from datetime import UTC, datetime, timedelta

import pytest

from kimai_tray.core.errors import ApiError, ErrorKind
from kimai_tray.core.kimai_client import KimaiClient

pytestmark = pytest.mark.kimai
DESCRIPTION = "Test kontraktowy — formularz rezerwacji"


def ids(tracker):
    project = next(p for p in tracker.snapshot.projects if p.name == "Moduł rezerwacji")
    activity = next(a for a in tracker.activities(project.id) if a.name == "Programowanie")
    return project.id, activity.id


def test_me_exposes_timezone_and_language(kimai_env):
    client = KimaiClient(kimai_env["KIMAI_TEST_URL"], kimai_env["KIMAI_TEST_USER_TOKEN"])
    me = client.me()
    assert (me.username, me.timezone) == ("jan", "UTC")
    assert me.language


def test_bad_token_is_auth_error(kimai_env):
    with pytest.raises(ApiError) as caught:
        KimaiClient(kimai_env["KIMAI_TEST_URL"], "not-a-token").active()
    assert caught.value.kind is ErrorKind.AUTH


def test_start_is_recorded_now_in_real_time(user_tracker):
    project, activity = ids(user_tracker)
    snapshot = user_tracker.start(
        project_id=project, activity_id=activity, description=DESCRIPTION, billable=None
    )
    assert snapshot.current is not None
    assert abs(snapshot.current.begin - datetime.now(UTC)) < timedelta(minutes=2)


def test_plain_user_billable_falls_back_and_locks(user_tracker):
    project, activity = ids(user_tracker)
    snapshot = user_tracker.start(
        project_id=project, activity_id=activity, description=DESCRIPTION, billable=False
    )
    assert (snapshot.notice, snapshot.billable_allowed) == ("errBillableDenied", False)
    assert snapshot.current is not None


def test_teamlead_can_set_billable(lead_tracker):
    project, activity = ids(lead_tracker)
    snapshot = lead_tracker.start(
        project_id=project, activity_id=activity, description=DESCRIPTION, billable=False
    )
    assert snapshot.current.billable is False
    snapshot = lead_tracker.set_billable(snapshot.current.id, True)
    assert snapshot.current.billable is True


def test_second_start_stops_the_first(user_tracker):
    project, activity = ids(user_tracker)
    user_tracker.start(project_id=project, activity_id=activity, description=DESCRIPTION, billable=None)
    snapshot = user_tracker.start(
        project_id=project, activity_id=activity, description=DESCRIPTION + " 2", billable=None
    )
    assert len(snapshot.running) == 1
    assert snapshot.current.description == DESCRIPTION + " 2"


def test_stop_and_totals(user_tracker):
    project, activity = ids(user_tracker)
    user_tracker.start(project_id=project, activity_id=activity, description=DESCRIPTION, billable=None)
    snapshot = user_tracker.stop()
    assert snapshot.running == ()
    assert snapshot.totals is not None
    assert snapshot.totals.week >= snapshot.totals.today
    assert any(entry.description == DESCRIPTION for entry in snapshot.recent)


def test_stopping_a_stopped_entry_is_not_an_error(kimai_env, user_tracker):
    project, activity = ids(user_tracker)
    entry = user_tracker.start(
        project_id=project, activity_id=activity, description=DESCRIPTION, billable=None
    ).current
    client = KimaiClient(kimai_env["KIMAI_TEST_URL"], kimai_env["KIMAI_TEST_USER_TOKEN"])
    client.stop(entry.id)
    assert client.stop(entry.id).end is not None
