"""Plan 7: the calendar — the days shown, the blocks and their columns, snapping (spec 0.10, section 8)."""

from dataclasses import replace
from datetime import UTC, date, datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from dk_tracker.core.calendar import (
    day_totals,
    hhmm_of,
    layout,
    shifted,
    snap,
    span_label,
    titled,
    view_days,
    zoom_floor,
    zoomed,
)
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


def test_a_block_has_its_day_and_seconds():
    [block] = layout([entry(1, date(2026, 9, 22), 9, 90, start_minute=15)], days(), WARSAW, NOW)
    assert (block.day, block.start, block.end, block.column, block.columns) == (1, 555 * 60, 645 * 60, 0, 1)
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
    assert (first.day, first.start, first.end, first.continues) == (0, 1320 * 60, 1440 * 60, True)
    assert (second.day, second.start, second.end, second.continued) == (1, 0, 60 * 60, True)


def test_the_running_entry_grows_until_now():
    [block] = layout([entry(1, TODAY, 16, 0, running=True)], days(), WARSAW, NOW)
    assert (block.day, block.start, block.end, block.running) == (4, 960 * 60, 1080 * 60, True)


def test_seconds_count_when_one_entry_stops_and_the_next_starts_in_the_same_minute():
    monday = date(2026, 9, 21)
    first = make_entry(1, at(monday, 9) + timedelta(seconds=10), at(monday, 10) + timedelta(seconds=40))
    short = make_entry(2, at(monday, 10) + timedelta(seconds=40), at(monday, 10) + timedelta(seconds=55))
    nxt = make_entry(3, at(monday, 10) + timedelta(seconds=55), at(monday, 11))
    blocks = {block.entry.id: block for block in layout([first, short, nxt], days(), WARSAW, NOW)}
    assert (blocks[1].start, blocks[1].end) == (9 * 3600 + 10, 10 * 3600 + 40)
    assert (blocks[2].start, blocks[2].end) == (10 * 3600 + 40, 10 * 3600 + 55)  # within one minute: kept
    assert {(block.column, block.columns) for block in blocks.values()} == {(0, 1)}  # one after another


def test_a_short_entry_and_the_next_one_share_no_columns():
    monday = date(2026, 9, 21)  # 8:45–8:54 and 8:55–10:23 (the user's screenshot)
    short, nxt = entry(1, monday, 8, 9, start_minute=45), entry(2, monday, 8, 88, start_minute=55)
    blocks = layout([short, nxt], days(), WARSAW, NOW)
    assert {(block.column, block.columns) for block in blocks} == {(0, 1)}


def test_a_zero_length_entry_still_shows():
    moment = at(date(2026, 9, 21), 9)
    [block] = layout([make_entry(1, moment, moment)], days(), WARSAW, NOW)
    assert block.start == block.end == 9 * 3600


def test_entries_of_other_days_are_left_out():
    assert layout([entry(1, date(2026, 9, 28), 9, 60)], days(), WARSAW, NOW) == []


def test_day_totals_count_each_entry_on_the_day_it_began():
    entries = [entry(1, date(2026, 9, 21), 22, 180), entry(2, TODAY, 16, 0, running=True)]
    totals = day_totals(entries, days(), WARSAW, NOW)
    assert totals[0] == 3 * 3600 and totals[1] == 0 and totals[4] == 2 * 3600


def test_an_exported_entry_is_kept_with_its_flag():
    [block] = layout([replace(entry(1, TODAY, 9, 60), exported=True)], days(), WARSAW, NOW)
    assert block.entry.exported is True


def test_zoom_by_a_quarter_a_notch_within_bounds():
    assert (zoomed(96, 1), zoomed(96, -1), zoomed(96, 0.5)) == (120, 77, 107)
    assert (zoomed(40, -5), zoomed(300, 5)) == (32, 384)


def test_minutes_on_the_wall_clock_of_a_day():
    from dk_tracker.core.timefmt import wall_clock

    assert wall_clock(TODAY, 555, WARSAW) == datetime(2026, 9, 25, 9, 15, tzinfo=WARSAW)
    assert wall_clock(TODAY, 1440, WARSAW) == datetime(2026, 9, 26, 0, 0, tzinfo=WARSAW)


def test_an_entry_ending_at_midnight_does_not_go_on():
    [block] = layout([entry(1, date(2026, 9, 21), 23, 60)], days(), WARSAW, NOW)
    assert (block.end, block.continues) == (1440 * 60, False)


# -- a line for every title (0090) -------------------------------------------------------------


def test_the_scale_goes_out_only_as_far_as_the_shortest_entry_keeps_its_line():
    monday = date(2026, 9, 21)
    assert zoom_floor(layout([entry(1, monday, 9, 120)], days(), WARSAW, NOW)) == 32  # long ones: no limit
    blocks = layout([entry(1, monday, 9, 120), entry(2, monday, 12, 10)], days(), WARSAW, NOW)
    assert zoom_floor(blocks) == 132  # 10 minutes: 22 px at 132 px an hour


def test_an_entry_too_short_for_a_line_even_at_the_closest_does_not_hold_the_scale():
    monday = date(2026, 9, 21)
    blocks = layout([entry(1, monday, 9, 1), entry(2, monday, 10, 0)], days(), WARSAW, NOW)  # 1 min, 0 min
    assert zoom_floor(blocks) == 32


def test_a_short_entry_gets_its_line_and_the_next_title_starts_below_it():
    monday = date(2026, 9, 21)  # 9:00–9:01, then 9:05–10:00 and 10:00–11:00 at 96 px an hour
    blocks = layout(
        [entry(1, monday, 9, 1), entry(2, monday, 9, 55, start_minute=5), entry(3, monday, 10, 60)],
        days(),
        WARSAW,
        NOW,
    )
    placed = {block.entry.id: block for block in titled(blocks, 96)}
    assert {(block.column, block.columns) for block in placed.values()} == {(0, 1)}  # still one after another
    assert (placed[1].inset, placed[1].height) == (0, 22)  # 1.6 px of time, a line drawn
    assert placed[2].inset == pytest.approx(22 - 8)  # 9:05 is 8 px below 9:00
    assert placed[2].height == pytest.approx(88)  # its own 55 minutes, more than the inset and a line
    assert (placed[3].inset, placed[3].height) == (0, 96)


def test_a_chain_of_short_entries_pushes_each_title_below_the_one_before():
    monday = date(2026, 9, 21)  # three one-minute entries a minute apart, at 60 px an hour
    blocks = layout([entry(i, monday, 9, 1, start_minute=2 * i) for i in range(3)], days(), WARSAW, NOW)
    tops = [(block.start / 3600 * 60 + block.inset) for block in titled(blocks, 60)]
    assert tops == pytest.approx([540, 562, 584])  # each title a line below the one before


def test_entries_side_by_side_do_not_push_each_other():
    monday = date(2026, 9, 21)
    blocks = layout([entry(1, monday, 9, 120), entry(2, monday, 9, 1, start_minute=30)], days(), WARSAW, NOW)
    placed = {block.entry.id: block for block in titled(blocks, 96)}
    assert {block.entry.id: block.column for block in blocks} == {1: 0, 2: 1}
    assert placed[1].inset == 0 and placed[2].inset == 0  # the long one is beside it, not above it
