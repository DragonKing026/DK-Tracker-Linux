from datetime import UTC, datetime, timedelta

import pytest

from dk_tracker.core.errors import ApiError, ErrorKind
from dk_tracker.core.kimai_client import KimaiClient

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


def test_editing_an_exported_entry_is_forbidden_not_auth(kimai_env, user_tracker):
    project, activity = ids(user_tracker)
    entry = user_tracker.start(
        project_id=project, activity_id=activity, description=DESCRIPTION, billable=None
    ).current
    user = KimaiClient(kimai_env["KIMAI_TEST_URL"], kimai_env["KIMAI_TEST_USER_TOKEN"])
    admin = KimaiClient(kimai_env["KIMAI_TEST_URL"], kimai_env["KIMAI_TEST_ADMIN_TOKEN"])
    user.stop(entry.id)
    admin._request("PATCH", f"/api/timesheets/{entry.id}/export")  # admin marks it exported
    with pytest.raises(ApiError) as caught:
        user.update(entry.id, {"description": DESCRIPTION + " po eksporcie"})
    assert caught.value.kind is ErrorKind.FORBIDDEN
    assert any(e.id == entry.id and e.exported for e in user.latest(5))


def test_search_matches_every_word_of_the_users_own_descriptions(kimai_env, user_tracker):
    """F-33: `term` searches the description only; a team lead does not see the user's entries by default."""
    project, activity = ids(user_tracker)
    marker = f"szukaj{datetime.now(UTC):%H%M%S%f}"
    text = f"{DESCRIPTION} {marker} kalendarz"
    user_tracker.start(project_id=project, activity_id=activity, description=text, billable=None)
    user_tracker.stop()
    assert [entry.description for entry in user_tracker.search(f"{marker} kalendarz")] == [text]
    assert [entry.description for entry in user_tracker.search(marker.upper())] == [text]
    assert user_tracker.search(f"{marker} nieistniejące") == ()
    lead = KimaiClient(kimai_env["KIMAI_TEST_URL"], kimai_env["KIMAI_TEST_LEAD_TOKEN"])
    assert lead.search(marker) == []


def test_running_entry_moves_to_another_project_and_activity(user_tracker, lead_tracker):
    """F-34: Kimai takes `project` and `activity` in a PATCH of the running entry; `$` only from a lead."""
    for tracker, billable_sent in ((user_tracker, False), (lead_tracker, True)):
        project, activity = ids(tracker)
        tracker.start(project_id=project, activity_id=activity, description=DESCRIPTION, billable=None)
        other = next(p for p in tracker.snapshot.projects if p.name == "Administracja")
        meeting = next(a for a in tracker.activities(other.id) if a.id != activity)
        snapshot = tracker.change_work(other.id, meeting.id)
        current = snapshot.current
        assert (current.project_name, current.activity_name) == ("Administracja", meeting.name)
        if billable_sent:
            assert current.billable is False  # "Sprawy wewnętrzne" is a non-billable customer
        tracker.stop()


def _free_day(tracker, offset):
    """A past day of its own for each test, so runs on a kept instance do not meet each other."""
    day = datetime.now(UTC).date() - timedelta(days=400 + offset)
    for entry in tracker.entries(day, day):
        tracker.delete_entry(entry)
    return day


def test_an_entry_typed_in_by_hand_is_created_listed_and_deleted(user_tracker):
    """0.10.0: POST with begin and end, the week's list via `range`, DELETE."""
    project, activity = ids(user_tracker)
    day = _free_day(user_tracker, 1)
    user_tracker.add_entry(
        day=day,
        begin="09:00",
        end="10:30",
        project_id=project,
        activity_id=activity,
        description=DESCRIPTION,
        billable=None,
    )
    [entry] = user_tracker.entries(day, day)
    assert (entry.description, entry.project_id, entry.activity_id) == (DESCRIPTION, project, activity)
    assert (entry.end - entry.begin) == timedelta(minutes=90)
    user_tracker.delete_entry(entry)
    assert user_tracker.entries(day, day) == ()


def test_a_finished_entry_gets_new_hours_and_another_project(user_tracker):
    """0.10.0: PATCH begin/end/project/activity of a finished entry."""
    project, activity = ids(user_tracker)
    day = _free_day(user_tracker, 2)
    user_tracker.add_entry(
        day=day,
        begin="09:00",
        end="10:00",
        project_id=project,
        activity_id=activity,
        description=DESCRIPTION,
        billable=None,
    )
    [entry] = user_tracker.entries(day, day)
    other = next(p for p in user_tracker.snapshot.projects if p.name == "Administracja")
    meeting = user_tracker.activities(other.id)[0]
    user_tracker.edit_entry(entry, begin="08:15", end="11:45", project_id=other.id, activity_id=meeting.id)
    [edited] = user_tracker.entries(day, day)
    assert edited.id == entry.id
    assert (edited.project_name, edited.activity_id) == ("Administracja", meeting.id)
    assert edited.end - edited.begin == timedelta(hours=3, minutes=30)
    user_tracker.delete_entry(edited)


def test_overlapping_entries_follow_the_server_rule(user_tracker):
    """Kimai allows overlapping entries by default (timesheet.rules.allow_overlapping_records)."""
    project, activity = ids(user_tracker)
    day = _free_day(user_tracker, 3)
    for begin, end in (("09:00", "11:00"), ("10:00", "12:00")):
        user_tracker.add_entry(
            day=day,
            begin=begin,
            end=end,
            project_id=project,
            activity_id=activity,
            description=DESCRIPTION,
            billable=None,
        )
    found = user_tracker.entries(day, day)
    assert len(found) == 2
    for entry in found:
        user_tracker.delete_entry(entry)


def test_the_edit_window_reads_and_saves_tags_of_an_entry(kimai_env, user_tracker):
    """Live test of 0.10.0: tags from GET /api/timesheets/{id}, saved as a comma list."""
    project, activity = ids(user_tracker)
    day = _free_day(user_tracker, 4)
    admin = KimaiClient(kimai_env["KIMAI_TEST_URL"], kimai_env["KIMAI_TEST_ADMIN_TOKEN"])
    try:
        admin._request("POST", "/api/tags", json={"name": "kontrakt"})  # an existing tag
    except ApiError:
        pass  # already made by an earlier run on a kept instance
    user_tracker.add_entry(
        day=day,
        begin="09:00",
        end="10:00",
        project_id=project,
        activity_id=activity,
        description=DESCRIPTION,
        billable=None,
    )
    [entry] = user_tracker.entries(day, day)
    details = user_tracker.entry_details(entry)
    assert details.tags == ()
    user_tracker.save_details(details, {"tags": "kontrakt"})
    assert user_tracker.entry_details(entry).tags == ("kontrakt",)
    user_tracker.delete_entry(entry)


def test_a_new_tag_from_a_plain_user_is_left_out_and_named(user_tracker):
    """Kimai 2.67.0 drops a tag that does not exist, without an error, for an account that may not
    create tags; the save reads the entry again and says which tags are missing."""
    project, activity = ids(user_tracker)
    day = _free_day(user_tracker, 6)
    user_tracker.add_entry(
        day=day,
        begin="09:00",
        end="10:00",
        project_id=project,
        activity_id=activity,
        description=DESCRIPTION,
        billable=None,
    )
    [entry] = user_tracker.entries(day, day)
    marker = f"nowy{datetime.now(UTC):%H%M%S%f}"
    snapshot = user_tracker.save_details(user_tracker.entry_details(entry), {"tags": marker})
    assert (snapshot.notice, snapshot.notice_params) == ("errTagsDropped", (("tags", marker),))
    user_tracker.delete_entry(entry)


def test_the_tags_to_choose_are_the_visible_ones(kimai_env, user_tracker):
    """/api/tags/find with an empty name: every visible tag, with its colour; hidden ones are left out."""
    admin = KimaiClient(kimai_env["KIMAI_TEST_URL"], kimai_env["KIMAI_TEST_ADMIN_TOKEN"])
    marker = f"widoczny{datetime.now(UTC):%H%M%S%f}"
    admin._request("POST", "/api/tags", json={"name": marker, "visible": True})
    tags = {tag.name: tag for tag in user_tracker.tags()}
    assert marker in tags and tags[marker].color.startswith("#")
    assert "kontrakt" not in tags  # made without "visible" by an earlier test: hidden
    admin.close()
