from datetime import UTC, datetime

from dk_tracker.core.models import Activity, Customer, Entry, Project, User

ACTIVE_ENTRY = {  # GET /api/timesheets/active — related objects expanded
    "id": 7,
    "begin": "2026-09-25T15:54:19+0000",
    "end": None,
    "duration": 0,
    "description": "Formularz rezerwacji",
    "billable": True,
    "project": {"id": 1, "name": "Moduł rezerwacji", "color": "#008000", "customer": {"id": 1}},
    "activity": {"id": 1, "name": "Programowanie"},
    "user": {"id": 2, "language": "pl"},
}
POSTED_ENTRY = {  # POST/PATCH responses — related objects as bare ids
    "id": 8,
    "begin": "2026-09-25T16:04:00+0000",
    "end": "2026-09-25T16:05:00+0000",
    "duration": 60,
    "description": "Drugi wpis",
    "billable": False,
    "project": 2,
    "activity": 1,
    "user": 2,
}


def test_entry_from_expanded_payload():
    entry = Entry.from_api(ACTIVE_ENTRY)
    assert entry.begin == datetime(2026, 9, 25, 15, 54, 19, tzinfo=UTC)
    assert entry.running is True
    assert (entry.project_id, entry.project_name, entry.project_color) == (1, "Moduł rezerwacji", "#008000")
    assert (entry.activity_id, entry.activity_name) == (1, "Programowanie")
    assert entry.user_language == "pl"


def test_entry_from_ids_payload():
    entry = Entry.from_api(POSTED_ENTRY)
    assert entry.running is False
    assert entry.end == datetime(2026, 9, 25, 16, 5, tzinfo=UTC)
    assert (entry.project_id, entry.project_name, entry.activity_id) == (2, None, 1)
    assert (entry.duration, entry.billable, entry.user_language) == (60, False, None)


def test_entry_tolerates_missing_fields():
    entry = Entry.from_api(
        {"id": 9, "begin": "2026-09-25T10:00:00+0200", "description": None, "project": None, "activity": None}
    )
    assert (entry.description, entry.project_id, entry.activity_id, entry.duration) == ("", None, None, 0)
    assert entry.billable is True
    assert entry.end is None


def test_user_display_name_prefers_alias():
    data = {"id": 2, "username": "jan", "alias": None, "language": "pl", "timezone": "Europe/Warsaw"}
    assert User.from_api(data).display_name == "jan"
    assert User.from_api({**data, "alias": "Jan K."}).display_name == "Jan K."


def test_user_defaults_when_fields_missing():
    user = User.from_api({"id": 1, "username": "admin"})
    assert (user.language, user.timezone, user.alias) == ("en", "", None)  # unknown, not UTC


def test_project_customer_name_sources():
    base = {"id": 3, "name": "KSeF", "customer": 1, "color": None, "billable": True}
    assert Project.from_api({**base, "parentTitle": "Hotel Morski"}).customer_name == "Hotel Morski"
    assert Project.from_api({**base, "customer": {"id": 1, "name": "Apteka"}}).customer_name == "Apteka"
    assert Project.from_api(base).customer_name == "-"
    assert Project.from_api(base).customer_id == 1
    assert Project.from_api(base).color is None


def test_activity_and_customer():
    activity = Activity.from_api({"id": 5, "name": "Spotkanie", "billable": False, "project": None})
    assert (activity.billable, activity.project_id) == (False, None)
    assert Customer.from_api({"id": 2, "name": "Sprawy wewnętrzne", "billable": False}).billable is False
    assert Customer.from_api({"id": 1, "name": "Hotel"}).billable is True


def test_user_timezone_from_preferences_when_field_missing():
    data = {
        "id": 1,
        "username": "jan",
        "preferences": [
            {"name": "first_weekday", "value": "monday"},
            {"name": "timezone", "value": "Europe/Warsaw"},
        ],
    }
    assert User.from_api(data).timezone == "Europe/Warsaw"


def test_user_timezone_field_wins_over_preferences():
    data = {
        "id": 1,
        "username": "jan",
        "timezone": "UTC",
        "preferences": [{"name": "timezone", "value": "Europe/Warsaw"}],
    }
    assert User.from_api(data).timezone == "UTC"


def test_user_timezone_ignores_broken_preferences():
    assert (
        User.from_api(
            {"id": 1, "username": "jan", "preferences": [None, {"name": "timezone", "value": None}]}
        ).timezone
        == ""
    )


def test_entry_exported_flag():
    assert Entry.from_api({**POSTED_ENTRY, "exported": True}).exported is True
    assert Entry.from_api(POSTED_ENTRY).exported is False


def test_user_first_weekday_from_preferences():
    prefs = {
        "id": 1,
        "username": "jan",
        "timezone": "UTC",
        "preferences": [{"name": "first_weekday", "value": "sunday"}],
    }
    assert User.from_api(prefs).first_weekday == "sunday"
    assert User.from_api({"id": 1, "username": "jan"}).first_weekday == "monday"
