"""Plan 5: the list models the QML main window draws (no QML needed here)."""

from datetime import UTC, date, datetime, timedelta
from zoneinfo import ZoneInfo

from dk_tracker.core.entry_list import build_rows
from dk_tracker.core.i18n import Translator
from dk_tracker.core.models import Activity
from dk_tracker.ui.main_window.models import ActivityModel, EntryListModel, ProjectModel

from ...core.fakes import FakeClient, make_entry

WARSAW = ZoneInfo("Europe/Warsaw")
TODAY = date(2026, 9, 25)


def at(hour, minutes, entry_id, **extra):
    begin = datetime(2026, 9, 25, hour, tzinfo=WARSAW).astimezone(UTC)
    return make_entry(entry_id, begin, begin + timedelta(minutes=minutes), **extra)


def roles(model, row):
    index = model.index(row, 0)
    return {bytes(name).decode(): model.data(index, role) for role, name in model.roleNames().items()}


def test_entry_rows_carry_what_a_row_shows(qapp):
    model = EntryListModel()
    rows = build_rows(
        [at(9, 90, 7, description="Kalendarz pokoi", billable=False)], WARSAW, TODAY, 0, Translator("pl")
    )
    model.set_rows(rows, WARSAW)
    assert model.rowCount() == 3
    assert roles(model, 0)["kind"] == "week" and roles(model, 0)["label"] == "Ten tydzień"
    entry = roles(model, 2)
    assert entry == {
        "kind": "entry",
        "key": "entry:7",
        "label": "",
        "total": "1:30",
        "entryId": 7,
        "description": "Kalendarz pokoi",
        "projectId": 1,
        "projectName": "Moduł rezerwacji",
        "projectColor": "#008000",
        "activityId": 1,
        "activityName": "Programowanie",
        "billable": False,
        "begin": "09:00",
        "end": "10:30",
        "exported": False,
    }


def test_hidden_entries_drop_out_until_shown_again(qapp):
    """The undo bar: a deleted row goes away at once and comes back on "Undo"."""
    model = EntryListModel()
    model.set_rows(build_rows([at(9, 60, 1), at(11, 60, 2)], WARSAW, TODAY, 0, Translator("pl")), WARSAW)
    model.hide_entry(2)
    assert [roles(model, i)["key"] for i in range(model.rowCount())] == [
        "week:2026-09-21",
        "day:2026-09-25",
        "entry:1",
    ]
    model.show_entry(2)
    assert model.rowCount() == 4


def test_an_entry_is_found_by_id(qapp):
    model = EntryListModel()
    first = at(9, 60, 1)
    model.set_rows(build_rows([first], WARSAW, TODAY, 0, Translator("pl")), WARSAW)
    assert model.entry(1) == first
    assert model.entry(99) is None


def test_projects_are_grouped_by_customer_and_filtered_like_the_popup(qapp):
    model = ProjectModel()
    model.set_projects(FakeClient().projects_list)
    assert [(roles(model, i)["kind"], roles(model, i)["name"]) for i in range(model.rowCount())] == [
        ("header", "Hotel Morski"),
        ("project", "Moduł rezerwacji"),
        ("header", "Sprawy wewnętrzne"),
        ("project", "Administracja"),
    ]
    model.set_filter("modul")  # no Polish letters, any case — as in the popup (F-06)
    assert [roles(model, i)["name"] for i in range(model.rowCount())] == ["Hotel Morski", "Moduł rezerwacji"]
    model.set_filter("sprawy")  # the customer's name matches all its projects
    assert [roles(model, i)["name"] for i in range(model.rowCount())] == [
        "Sprawy wewnętrzne",
        "Administracja",
    ]


def test_project_lookup(qapp):
    model = ProjectModel()
    model.set_projects(FakeClient().projects_list)
    assert model.project(2).name == "Administracja"
    assert model.project(None) is None


def test_activities_for_a_project(qapp):
    model = ActivityModel()
    model.set_activities([Activity(2, "Spotkanie", True, None), Activity(1, "Programowanie", True, None)])
    assert [roles(model, i)["name"] for i in range(model.rowCount())] == ["Spotkanie", "Programowanie"]
    assert roles(model, 0)["activityId"] == 2
