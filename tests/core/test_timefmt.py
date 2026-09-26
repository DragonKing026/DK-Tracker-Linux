from datetime import UTC, date, datetime
from zoneinfo import ZoneInfo

import pytest

from ws_tracker.core.timefmt import (
    at_wall_clock,
    badge_label,
    clock,
    day_end,
    days_back,
    elapsed_seconds,
    hhmm,
    kimai_stamp,
    local_day,
    short_duration,
    start_stamp,
    week_start,
    weekday_index,
    zone,
)

WAW = ZoneInfo("Europe/Warsaw")
UTC_ZONE = ZoneInfo("UTC")
NOW = datetime(2026, 9, 25, 16, 4, 3, tzinfo=UTC)  # Friday, 18:04:03 in Warsaw


def test_zone_known_and_unknown():
    assert zone("Europe/Warsaw") == WAW
    assert zone("Mars/Olympus") is None
    assert zone("") is None
    assert zone(None) is None
    assert zone("../etc/passwd") is None


def test_start_stamp_is_one_second_back_in_given_zone():
    assert start_stamp(NOW, WAW) == "2026-09-25T18:04:02"
    assert start_stamp(NOW, UTC_ZONE) == "2026-09-25T16:04:02"


def test_kimai_stamp_converts_to_zone():
    assert kimai_stamp(datetime(2026, 9, 25, 22, 30, tzinfo=UTC), WAW) == "2026-09-26T00:30:00"


def test_durations():
    assert short_duration(0) == "0:00"
    assert short_duration(None) == "0:00"
    assert short_duration(-5) == "0:00"
    assert short_duration(3599) == "0:59"
    assert short_duration(10 * 3600 + 5 * 60) == "10:05"
    assert clock(3723) == "1:02:03"
    assert badge_label(59) == "0m"
    assert badge_label(47 * 60) == "47m"
    assert badge_label(3600) == "1:00"
    assert badge_label(82 * 60 + 30) == "1:22"


def test_elapsed_never_negative():
    assert elapsed_seconds(NOW, NOW.replace(second=0)) == 0
    assert elapsed_seconds(NOW.replace(second=0), NOW) == 3


def test_week_start_and_day_end():
    assert week_start(NOW, WAW) == datetime(2026, 9, 21, 0, 0, tzinfo=WAW)
    assert day_end(NOW, WAW) == datetime(2026, 9, 25, 23, 59, 59, tzinfo=WAW)


def test_week_start_on_monday_and_sunday():
    monday = datetime(2026, 9, 21, 0, 30, tzinfo=WAW)
    sunday = datetime(2026, 9, 27, 23, 0, tzinfo=WAW)
    assert week_start(monday, WAW) == datetime(2026, 9, 21, 0, 0, tzinfo=WAW)
    assert week_start(sunday, WAW) == datetime(2026, 9, 21, 0, 0, tzinfo=WAW)


def test_week_start_across_dst_change():
    sunday_after_dst_end = datetime(2026, 10, 25, 12, 0, tzinfo=UTC)  # 13:00 CET
    start = week_start(sunday_after_dst_end, WAW)
    assert start == datetime(2026, 10, 19, 0, 0, tzinfo=WAW)
    assert start.utcoffset().total_seconds() == 2 * 3600  # Monday was still CEST
    assert day_end(sunday_after_dst_end, WAW).utcoffset().total_seconds() == 3600


def test_days_back_depends_on_zone():
    just_after_midnight_in_warsaw = datetime(2026, 9, 24, 22, 30, tzinfo=UTC)
    assert days_back(just_after_midnight_in_warsaw, NOW, WAW) == 0
    assert days_back(just_after_midnight_in_warsaw, NOW, UTC_ZONE) == 1
    assert local_day(just_after_midnight_in_warsaw, WAW) == date(2026, 9, 25)


def test_at_wall_clock_uses_day_of_anchor_in_zone():
    anchor = datetime(2026, 9, 25, 6, 0, tzinfo=UTC)
    assert at_wall_clock(anchor, "07:15", WAW) == datetime(2026, 9, 25, 7, 15, tzinfo=WAW)
    assert at_wall_clock(anchor, "7:05", WAW) == datetime(2026, 9, 25, 7, 5, tzinfo=WAW)


@pytest.mark.parametrize("value", ["25:00", "7", "ab:cd", "07:60", "", "12:5", "-1:00"])
def test_at_wall_clock_rejects_invalid_time(value):
    with pytest.raises(ValueError):
        at_wall_clock(NOW, value, WAW)


def test_hhmm():
    assert hhmm(datetime(2026, 9, 25, 16, 4, tzinfo=UTC), WAW) == "18:04"


def test_weekday_index():
    assert (weekday_index("monday"), weekday_index("Sunday"), weekday_index("saturday")) == (0, 6, 5)
    assert (weekday_index(None), weekday_index(""), weekday_index("someday")) == (0, 0, 0)


def test_week_start_on_sunday_weeks():
    assert week_start(NOW, WAW, first_weekday=6) == datetime(
        2026, 9, 20, 0, 0, tzinfo=WAW
    )  # Friday -> last Sunday
    sunday = datetime(2026, 9, 27, 10, 0, tzinfo=WAW)
    assert week_start(sunday, WAW, first_weekday=6) == datetime(2026, 9, 27, 0, 0, tzinfo=WAW)
