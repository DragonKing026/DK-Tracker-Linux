"""Plan 7: the calendar — the days shown, the blocks and their columns, snapping (spec 0.10, section 8)."""

from dataclasses import replace
from datetime import UTC, date, datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from dk_tracker.core.calendar import day_totals, hhmm_of, layout, shifted, snap, span_label, view_days
from dk_tracker.core.i18n import Translator

from .fakes import make_entry

WARSAW = ZoneInfo("Europe/Warsaw")
PL = Translator("pl")
NOW = datetime(2026, 9, 25, 16, 0, tzinfo=UTC)  # Friday 18:00 in Warsaw
TODAY = date(2026, 9, 25)
MONDAY, SUNDAY = 0, 6


def at(day, hour, minute=0):
    return datetime(day.year, day.month, day.day, hour, minute, tzinfo=WARSAW).astimezone(UTC)


def entry(entry_id, day, hour, minutes, *, start_minute=0, running=False):
    begin = at(day, hour, start_minute)
    return make_entry(entry_id, begin, None if running else begin + timedelta(minutes=minutes))


# -- the days ------------------------------------------------------------------------------


def test_a_week_of_seven_days_starts_on_the_accounts_first_weekday():
    assert view_days("week", TODAY, MONDAY, workweek=False) == [
        date(2026, 9, 21) + timedelta(days=i) for i in range(7)
    ]
    assert view_days("week", TODAY, SUNDAY, workweek=False)[0] == date(2026, 9, 20)


def test_five_days_are_monday_to_friday_whatever_the_first_weekday():
    days = [date(2026, 9, 21) + timedelta(days=i) for i in range(5)]
    assert view_days("week", TODAY, MONDAY, workweek=True) == days
    assert view_days("week", TODAY, SUNDAY, workweek=True) == days


def test_a_day_is_one_day():
    assert view_days("day", TODAY, MONDAY, workweek=True) == [TODAY]


def test_the_arrows_move_by_a_day_or_a_week():
    assert shifted("day", TODAY, -1) == date(2026, 9, 24)
    assert shifted("week", TODAY, 1) == date(2026, 10, 2)


def test_labels():
    assert span_label([TODAY], TODAY, PL) == "pt., 25 wrz 2026"
    assert span_label(view_days("week", TODAY, MONDAY, workweek=False), TODAY, PL) == "21 – 27 wrz 2026"


# -- snapping and hours ------------------------------------------------------------------


SNAPS = [
    (7, 15, 0),
    (8, 15, 15),
    (452, 15, 450),
    (1439, 15, 1440),
    (-5, 15, 0),
    (2000, 15, 1440),
    (452.6, 1, 453),
]


@pytest.mark.parametrize(("minutes", "step", "snapped"), SNAPS)
def test_snap_to_quarter_hours_or_exact_minutes(minutes, step, snapped):
    assert snap(minutes, step) == snapped


def test_hours_as_text_with_midnight_as_24():
    assert (hhmm_of(0), hhmm_of(455), hhmm_of(1440)) == ("00:00", "07:35", "24:00")


# -- the blocks ----------------------------------------------------------------------------


def days():
    return view_days("week", TODAY, MONDAY, workweek=False)


def test_a_block_has_its_day_and_minutes():
    [block] = layout([entry(1, date(2026, 9, 22), 9, 90, start_minute=15)], days(), WARSAW, NOW)
    assert (block.day, block.start, block.end, block.column, block.columns) == (1, 555, 645, 0, 1)
    assert (block.running, block.continued, block.continues) == (False, False, False)


def test_overlapping_entries_stand_side_by_side():
    monday = date(2026, 9, 21)
    blocks = layout(
        [
            entry(1, monday, 9, 120),
            entry(2, monday, 10, 60),
            entry(3, monday, 12, 30),
            entry(4, monday, 13, 30),
        ],
        days(),
        WARSAW,
        NOW,
    )
    placed = {block.entry.id: (block.column, block.columns) for block in blocks}
    assert placed == {1: (0, 2), 2: (1, 2), 3: (0, 1), 4: (0, 1)}  # 12:00 no longer overlaps 9–11


def test_three_in_a_chain_use_the_columns_they_need():
    monday = date(2026, 9, 21)
    blocks = layout(
        [entry(1, monday, 9, 180), entry(2, monday, 10, 30), entry(3, monday, 11, 30)], days(), WARSAW, NOW
    )
    placed = {block.entry.id: (block.column, block.columns) for block in blocks}
    assert placed == {1: (0, 2), 2: (1, 2), 3: (1, 2)}  # the second column is free again at 11:00


def test_an_entry_past_midnight_goes_on_into_the_next_day():
    late = entry(1, date(2026, 9, 21), 22, 180)
    first, second = layout([late], days(), WARSAW, NOW)
    assert (first.day, first.start, first.end, first.continues) == (0, 1320, 1440, True)
    assert (second.day, second.start, second.end, second.continued) == (1, 0, 60, True)


def test_the_running_entry_grows_until_now():
    [block] = layout([entry(1, TODAY, 16, 0, running=True)], days(), WARSAW, NOW)
    assert (block.day, block.start, block.end, block.running) == (4, 960, 1080, True)


def test_entries_of_other_days_are_left_out():
    assert layout([entry(1, date(2026, 9, 28), 9, 60)], days(), WARSAW, NOW) == []


def test_day_totals_count_each_entry_on_the_day_it_began():
    entries = [entry(1, date(2026, 9, 21), 22, 180), entry(2, TODAY, 16, 0, running=True)]
    totals = day_totals(entries, days(), WARSAW, NOW)
    assert totals[0] == 3 * 3600 and totals[1] == 0 and totals[4] == 2 * 3600


def test_an_exported_entry_is_kept_with_its_flag():
    [block] = layout([replace(entry(1, TODAY, 9, 60), exported=True)], days(), WARSAW, NOW)
    assert block.entry.exported is True


def test_minutes_on_the_wall_clock_of_a_day():
    from dk_tracker.core.timefmt import wall_clock

    assert wall_clock(TODAY, 555, WARSAW) == datetime(2026, 9, 25, 9, 15, tzinfo=WARSAW)
    assert wall_clock(TODAY, 1440, WARSAW) == datetime(2026, 9, 26, 0, 0, tzinfo=WARSAW)
