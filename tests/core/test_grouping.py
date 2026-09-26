from datetime import UTC, date, datetime
from zoneinfo import ZoneInfo

from dk_tracker.core.grouping import day_total, group_by_day, group_projects, sort_key
from dk_tracker.core.models import Entry, Project

WAW = ZoneInfo("Europe/Warsaw")


def entry(entry_id, begin, duration=600):
    return Entry(entry_id, begin, begin, duration, "opis", True, 1, "P", None, 1, "A", None)


def project(project_id, name, customer):
    return Project(project_id, name, 1, customer, None, True)


def test_group_by_day_keeps_arrival_order_and_uses_zone():
    e1 = entry(1, datetime(2026, 9, 25, 14, 0, tzinfo=UTC))
    e2 = entry(2, datetime(2026, 9, 24, 22, 30, tzinfo=UTC))  # 00:30 on the 25th in Warsaw
    e3 = entry(3, datetime(2026, 9, 24, 8, 0, tzinfo=UTC))
    assert group_by_day([e1, e2, e3], WAW) == [(date(2026, 9, 25), [e1, e2]), (date(2026, 9, 24), [e3])]


def test_day_total():
    assert (
        day_total(
            [
                entry(1, datetime(2026, 9, 25, tzinfo=UTC), 600),
                entry(2, datetime(2026, 9, 25, tzinfo=UTC), 30),
            ]
        )
        == 630
    )


def test_sort_key_ignores_case_and_diacritics():
    assert sorted(["Żabka", "apteka", "Hotel"], key=sort_key) == ["apteka", "Hotel", "Żabka"]


def test_group_projects_sorts_customers_and_projects():
    projects = [
        project(1, "Sklep", "Żabka"),
        project(2, "Rezerwacje", "Hotel Morski"),
        project(3, "API", "Hotel Morski"),
    ]
    grouped = group_projects(projects)
    assert [customer for customer, _ in grouped] == ["Hotel Morski", "Żabka"]
    assert [p.name for p in grouped[0][1]] == ["API", "Rezerwacje"]
