"""Property-based tests (Hypothesis) of the pure core: time formats, the wall clock, description checks.

Example tests elsewhere pin known cases; these state rules that hold for every input, so an off-by-one at a
boundary or an unexpected exception type shows up on inputs nobody thought of.
"""

import re
from datetime import UTC, date, datetime, time, timedelta, timezone

from hypothesis import given
from hypothesis import strategies as st

from dk_tracker.core.grouping import sort_key
from dk_tracker.core.timefmt import (
    STAMP,
    WEEKDAYS,
    at_wall_clock,
    badge_label,
    clock,
    elapsed_seconds,
    hhmm,
    kimai_stamp,
    short_duration,
    stop_moment,
    wall_clock,
    week_start,
    weekday_index,
)
from dk_tracker.core.validation import GENERIC, check_description

# Fixed offsets only: a named zone has gaps and overlaps at DST changes, which these rules do not cover.
ZONES = st.integers(min_value=-12 * 60, max_value=14 * 60).map(lambda m: timezone(timedelta(minutes=m)))
MOMENTS = st.datetimes(min_value=datetime(1990, 1, 2), max_value=datetime(2100, 1, 1), timezones=st.just(UTC))
DAYS = st.dates(min_value=date(1990, 1, 2), max_value=date(2100, 1, 1))
SECONDS = st.floats(min_value=-1e7, max_value=1e9, allow_nan=False, allow_infinity=False)
REFERENCE = re.compile(r"https?://|#\d+|\b[A-Z]{2,}-\d+\b")


@given(SECONDS)
def test_clock_splits_the_seconds_into_hours_minutes_seconds(seconds):
    match = re.fullmatch(r"(\d+):([0-5]\d):([0-5]\d)", clock(seconds))
    assert match
    hours, minutes, rest = map(int, match.groups())
    assert hours * 3600 + minutes * 60 + rest == max(0, int(seconds))


@given(st.one_of(st.none(), SECONDS))
def test_short_duration_is_hours_and_minutes_and_never_negative(seconds):
    match = re.fullmatch(r"(\d+):([0-5]\d)", short_duration(seconds))
    assert match
    hours, minutes = map(int, match.groups())
    assert hours * 60 + minutes == max(0, round(seconds or 0)) // 60


@given(SECONDS)
def test_badge_label_switches_to_hours_at_sixty_minutes(seconds):
    label = badge_label(seconds)
    minutes = max(0, int(seconds)) // 60
    if minutes < 60:
        assert label == f"{minutes}m"
    else:
        assert label == f"{minutes // 60}:{minutes % 60:02d}"


@given(st.floats(min_value=0, max_value=1e9, allow_nan=False), st.floats(min_value=0, max_value=1e5))
def test_longer_time_never_shows_a_shorter_clock(seconds, extra):
    def total(text):
        hours, minutes, rest = map(int, text.split(":"))
        return hours * 3600 + minutes * 60 + rest

    assert total(clock(seconds)) <= total(clock(seconds + extra))


@given(MOMENTS, MOMENTS)
def test_elapsed_seconds_is_never_negative(begin, now):
    assert elapsed_seconds(begin, now) >= 0
    if now >= begin:
        assert elapsed_seconds(begin, now) == int((now - begin).total_seconds())


@given(MOMENTS, ZONES)
def test_kimai_stamp_is_the_wall_clock_in_the_zone(moment, tz):
    stamp = kimai_stamp(moment, tz)
    assert datetime.strptime(stamp, STAMP) == moment.astimezone(tz).replace(tzinfo=None, microsecond=0)


@given(MOMENTS)
def test_stop_moment_is_a_full_minute_less_than_a_minute_before_now_minus_a_second(now):
    stop = stop_moment(now)
    assert (stop.second, stop.microsecond) == (0, 0)
    assert timedelta(0) <= (now - timedelta(seconds=1)) - stop < timedelta(minutes=1)


@given(DAYS, st.integers(0, 23), st.integers(0, 59), ZONES)
def test_wall_clock_time_survives_a_round_trip(day, hours, minutes, tz):
    moment = at_wall_clock(datetime.combine(day, time(12), tz), f"{hours}:{minutes:02d}", tz)
    assert hhmm(moment, tz) == f"{hours:02d}:{minutes:02d}"
    assert moment.astimezone(tz).date() == day


@given(st.text(max_size=12), ZONES)
def test_at_wall_clock_rejects_with_value_error_only(text, tz):
    day = datetime(2026, 9, 25, 12, tzinfo=tz)
    try:
        moment = at_wall_clock(day, text, tz)
    except ValueError:
        return
    assert 0 <= moment.hour <= 23 and 0 <= moment.minute <= 59
    assert moment.date() == day.date()


@given(st.integers(24, 99), st.integers(0, 99), ZONES)
def test_at_wall_clock_rejects_an_hour_past_23(hours, minutes, tz):
    try:
        at_wall_clock(datetime(2026, 9, 25, 12, tzinfo=tz), f"{hours}:{minutes:02d}", tz)
    except ValueError:
        return
    raise AssertionError("an hour past 23 was accepted")


@given(MOMENTS, ZONES, st.integers(0, 6))
def test_week_start_is_midnight_of_the_first_weekday_within_the_last_seven_days(now, tz, first_weekday):
    start = week_start(now, tz, first_weekday)
    assert start.weekday() == first_weekday
    assert (start.hour, start.minute, start.second) == (0, 0, 0)
    assert timedelta(0) <= now.astimezone(tz) - start < timedelta(days=7)


@given(DAYS, st.integers(0, 3 * 24 * 60), ZONES)
def test_wall_clock_counts_minutes_from_midnight(day, minutes, tz):
    assert wall_clock(day, minutes, tz) - datetime.combine(day, time(), tz) == timedelta(minutes=minutes)


@given(st.one_of(st.none(), st.text(max_size=20)))
def test_weekday_index_is_always_a_weekday_number(name):
    assert 0 <= weekday_index(name) <= 6


@given(st.sampled_from(WEEKDAYS), st.sampled_from(["", " ", "\t"]), st.booleans())
def test_weekday_names_map_to_their_position_in_any_case(name, padding, upper):
    text = padding + (name.upper() if upper else name) + padding
    assert weekday_index(text) == WEEKDAYS.index(name)


@given(st.one_of(st.none(), st.text(max_size=80)), st.integers(-5, 40))
def test_a_description_check_explains_every_refusal(text, min_length):
    result = check_description(text, min_length)
    if result.ok:
        assert result.reason is None and result.word is None
    else:
        assert result.reason in {"short", "generic"}
        assert min_length > 0
        assert (result.word is not None) == (result.reason == "generic")


@given(st.text(max_size=80))
def test_no_length_requirement_accepts_anything(text):
    assert check_description(text, 0).ok is True


@given(st.text(max_size=80), st.integers(1, 40))
def test_an_accepted_description_is_long_enough_or_a_reference(text, min_length):
    result = check_description(text, min_length)
    if len(text.strip()) < min_length and not REFERENCE.search(text.strip()):
        assert not result.ok
    if result.ok:
        assert len(text.strip()) >= min_length or REFERENCE.search(text.strip())


@given(
    st.sampled_from(sorted(GENERIC)),
    st.sampled_from(["", " ", "  "]),
    st.sampled_from(["", ".", "!", ";"]),
    st.booleans(),
    st.integers(1, 40),
)
def test_a_generic_word_is_refused_whatever_its_case_and_punctuation(word, padding, mark, upper, min_length):
    text = padding + (word.upper() if upper else word) + mark + padding
    result = check_description(text, min_length)
    assert (result.ok, result.reason) == (False, "generic")


@given(st.text(alphabet=st.characters(min_codepoint=97, max_codepoint=122), max_size=30))
def test_sort_key_ignores_case_and_accents(word):
    accented = "".join(letter + "́" for letter in word)
    assert sort_key(word) == sort_key(word.upper()) == sort_key(accented)


@given(st.text(max_size=40))
def test_sort_key_accepts_any_text(text):
    assert isinstance(sort_key(text), str)
