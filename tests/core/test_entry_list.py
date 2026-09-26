"""Plan 5: the main window's list — weeks, then days, then entries, each with its total."""

from datetime import UTC, date, datetime, timedelta
from zoneinfo import ZoneInfo

from dk_tracker.core.entry_list import build_rows, first_day_of_week
from dk_tracker.core.i18n import Translator

from .fakes import make_entry

WARSAW = ZoneInfo("Europe/Warsaw")
PL = Translator("pl")
TODAY = date(2026, 9, 25)  # Friday


def at(day, hour, minutes=60, entry_id=1):
    begin = datetime(day.year, day.month, day.day, hour, tzinfo=WARSAW).astimezone(UTC)
    return make_entry(entry_id, begin, begin + timedelta(minutes=minutes))


def test_first_day_of_week_follows_the_account():
    assert first_day_of_week(TODAY, 0) == date(2026, 9, 21)  # Monday
    assert first_day_of_week(TODAY, 6) == date(2026, 9, 20)  # Sunday


def test_rows_are_weeks_then_days_then_entries_with_totals():
    friday_a, friday_b = at(TODAY, 9, 90, 1), at(TODAY, 13, 30, 2)
    monday = at(date(2026, 9, 21), 8, 60, 3)
    before = at(date(2026, 9, 18), 10, 45, 4)
    rows = build_rows([friday_b, friday_a, monday, before], WARSAW, TODAY, 0, PL)
    assert [(r.kind, r.label, r.total) for r in rows] == [
        ("week", "Ten tydzień", "3:00"),
        ("day", "Dziś", "2:00"),
        ("entry", "", "0:30"),
        ("entry", "", "1:30"),
        ("day", "pon., 21 wrz", "1:00"),
        ("entry", "", "1:00"),
        ("week", "Poprzedni tydzień", "0:45"),
        ("day", "pt., 18 wrz", "0:45"),
        ("entry", "", "0:45"),
    ]
    assert [r.entry.id for r in rows if r.kind == "entry"] == [2, 1, 3, 4]


def test_older_weeks_are_named_by_their_days():
    old = at(date(2026, 8, 12), 9, 60)
    rows = build_rows([old], WARSAW, TODAY, 0, PL)
    assert rows[0].label == "10 sie – 16 sie"
    assert rows[1].label == "śr., 12 sie"


def test_a_week_of_another_year_says_the_year():
    old = at(date(2025, 12, 30), 9, 60)
    assert build_rows([old], WARSAW, TODAY, 0, PL)[0].label == "29 gru 2025 – 4 sty 2026"


def test_every_row_has_a_stable_key_for_the_view():
    rows = build_rows([at(TODAY, 9, 60, 7)], WARSAW, TODAY, 0, PL)
    assert [r.key for r in rows] == ["week:2026-09-21", "day:2026-09-25", "entry:7"]


def test_english():
    rows = build_rows([at(TODAY, 9, 60)], WARSAW, TODAY, 0, Translator("en"))
    assert (rows[0].label, rows[1].label) == ("This week", "Today")
