"""Time in the Kimai account's zone and the formats the UI shows.

Kimai reads a submitted wall-clock time in the *account's* timezone and attaches that
zone without converting (verified on 2.67.0), so every time we send is computed there.
"""

from __future__ import annotations

import re
from datetime import date, datetime, timedelta, tzinfo
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

STAMP = "%Y-%m-%dT%H:%M:%S"
WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
_HHMM = re.compile(r"(\d{1,2}):(\d{2})")


def zone(name: str | None) -> ZoneInfo | None:
    """The named zone, or None when the name is empty or unknown to this system's tzdata."""
    if not name:
        return None
    try:
        return ZoneInfo(name)
    except (ZoneInfoNotFoundError, ValueError):
        return None


def kimai_stamp(moment: datetime, tz: tzinfo) -> str:
    return moment.astimezone(tz).strftime(STAMP)


def start_stamp(now: datetime, tz: tzinfo) -> str:
    """Kimai may refuse a start in the future, so "now" is sent one second early."""
    return kimai_stamp(now - timedelta(seconds=1), tz)


def elapsed_seconds(begin: datetime, now: datetime) -> int:
    return max(0, int((now - begin).total_seconds()))


def short_duration(seconds: float | None) -> str:
    total = max(0, round(seconds or 0))
    return f"{total // 3600}:{total // 60 % 60:02d}"


def clock(seconds: float) -> str:
    total = max(0, int(seconds))
    return f"{total // 3600}:{total // 60 % 60:02d}:{total % 60:02d}"


def badge_label(seconds: float) -> str:
    minutes = max(0, int(seconds)) // 60
    return f"{minutes}m" if minutes < 60 else f"{minutes // 60}:{minutes % 60:02d}"


def local_day(moment: datetime, tz: tzinfo) -> date:
    return moment.astimezone(tz).date()


def weekday_index(name: str | None) -> int:
    """Kimai's `first_weekday` preference as a weekday number (Monday 0); Monday if unknown."""
    name = (name or "").strip().lower()
    return WEEKDAYS.index(name) if name in WEEKDAYS else 0


def week_start(now: datetime, tz: tzinfo, first_weekday: int = 0) -> datetime:
    """00:00 of the first day of the current week in `tz` (Monday unless the account says otherwise)."""
    today = local_day(now, tz)
    start = today - timedelta(days=(today.weekday() - first_weekday) % 7)
    return datetime(start.year, start.month, start.day, tzinfo=tz)


def day_end(now: datetime, tz: tzinfo) -> datetime:
    today = local_day(now, tz)
    return datetime(today.year, today.month, today.day, 23, 59, 59, tzinfo=tz)


def days_back(moment: datetime, now: datetime, tz: tzinfo) -> int:
    return (local_day(now, tz) - local_day(moment, tz)).days


def at_wall_clock(day: datetime, hhmm_value: str, tz: tzinfo) -> datetime:
    """The calendar day of `day` in `tz`, at the given "HH:MM"."""
    match = _HHMM.fullmatch(hhmm_value.strip())
    if not match:
        raise ValueError(f"not a HH:MM time: {hhmm_value!r}")
    hours, minutes = int(match.group(1)), int(match.group(2))
    if hours > 23 or minutes > 59:
        raise ValueError(f"not a HH:MM time: {hhmm_value!r}")
    local = local_day(day, tz)
    return datetime(local.year, local.month, local.day, hours, minutes, tzinfo=tz)


def hhmm(moment: datetime, tz: tzinfo) -> str:
    return moment.astimezone(tz).strftime("%H:%M")
