"""The main window's calendar (Plan 7, spec 0.10 section 8): the days shown, entries as blocks in a
grid of minutes, side by side where they overlap, and snapping to quarter hours.

Pure functions; minutes are counted from the start of a day in the zone the window shows. Blocks keep
the seconds: an entry stopped and the next started within the same minute must neither vanish nor
seem to overlap.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from datetime import date, datetime, timedelta, tzinfo
from typing import Literal

from .entry_list import first_day_of_week
from .models import Entry
from .summary import dates_label
from .timefmt import elapsed_seconds, local_day, wall_clock

Mode = Literal["day", "week"]
DAY_MINUTES = 24 * 60
DAY_SECONDS = DAY_MINUTES * 60
SNAP_MINUTES = 15
# The grid's scale: pixels an hour, changed with Alt + the wheel (each notch a quarter more or less).
HOUR_HEIGHT = 96
HOUR_HEIGHT_MIN, HOUR_HEIGHT_MAX = 32, 384
ZOOM_STEP = 1.25
# A block is at least this tall (pixels): one line, its title. A shorter entry is drawn over the next one,
# whose title starts below it; the scale goes no further out than each entry that can have the line has it.
TITLE_HEIGHT = 22


@dataclass(frozen=True)
class Block:
    entry: Entry
    day: int  # index into the days shown
    start: int  # seconds from the day's midnight
    end: int  # up to 86400
    column: int = 0  # side by side with the entries it overlaps
    columns: int = 1
    running: bool = False
    continued: bool = False  # began the day before (past midnight)
    continues: bool = False  # goes on into the next day
    inset: float = 0  # pixels of its top under a shorter entry drawn over it: its title starts below them
    height: float = 0  # pixels drawn: its length, but at least the inset and a line (`titled`)


def view_days(mode: Mode, anchor: date, first_weekday: int, *, workweek: bool) -> list[date]:
    """A day, or a week from the account's first weekday; five days are Monday to Friday."""
    if mode == "day":
        return [anchor]
    first = first_day_of_week(anchor, first_weekday)
    week = [first + timedelta(days=i) for i in range(7)]
    return sorted(day for day in week if day.weekday() < 5) if workweek else week


def holiday_names(days: list[date], holidays: Mapping[date, str]) -> list[str]:
    """The public holiday of each day shown ("" for an ordinary day)."""
    return [holidays.get(day, "") for day in days]


def shifted(mode: Mode, anchor: date, steps: int) -> date:
    return anchor + timedelta(days=steps if mode == "day" else 7 * steps)


def span_label(days: list[date], today: date, t: Callable[..., str]) -> str:
    if len(days) == 1:
        day = days[0]
        weekdays, months = t("weekdaysShort").split(","), t("monthsShort").split(",")
        label = t("dayOther", weekday=weekdays[day.weekday()], day=day.day, month=months[day.month - 1])
        return f"{label} {day.year}"
    return dates_label(days[0], days[-1], t)


def snap(minutes: float, step: int = SNAP_MINUTES) -> int:
    """To the nearest step (1 = the exact minute, with Alt), within the day."""
    return max(0, min(DAY_MINUTES, round(minutes / step) * step))


def zoomed(hour_height: int, notches: float) -> int:
    """The scale after `notches` of the wheel (up = closer), within its bounds."""
    return max(HOUR_HEIGHT_MIN, min(HOUR_HEIGHT_MAX, round(hour_height * ZOOM_STEP**notches)))


def hhmm_of(minutes: int) -> str:
    """ "HH:MM"; the day's end is "24:00" (midnight of the next day)."""
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def layout(entries: Iterable[Entry], days: list[date], tz: tzinfo, now: datetime) -> list[Block]:
    """Blocks of the entries on the days shown; the running one until now."""
    index = {day: i for i, day in enumerate(days)}
    pieces: list[Block] = []
    for entry in entries:
        begin = entry.begin.astimezone(tz)
        end = (entry.end or now).astimezone(tz)
        day = begin.date()
        while day <= end.date() and day <= days[-1]:
            start = _seconds(begin) if day == begin.date() else 0
            stop = _seconds(end) if day == end.date() else DAY_SECONDS
            if day in index and (stop > start or begin == end):  # a zero-length entry still shows
                pieces.append(
                    Block(entry, index[day], start, stop, running=entry.end is None,
                          continued=day != begin.date(), continues=end > wall_clock(day, DAY_MINUTES, tz))
                )  # fmt: skip
            day += timedelta(days=1)
    placed: list[Block] = []
    for day_index in range(len(days)):
        placed.extend(
            _columns(sorted((b for b in pieces if b.day == day_index), key=lambda b: (b.start, -b.end)))
        )
    return placed


def zoom_floor(blocks: Iterable[Block], line: int = TITLE_HEIGHT) -> int:
    """The furthest scale at which every block has its line; one too short for it even at the closest
    (about 3 minutes) does not hold the scale back."""
    needs = [line * 3600 / length for block in blocks if (length := block.end - block.start) > 0]
    return max([HOUR_HEIGHT_MIN, *(math.ceil(need) for need in needs if need <= HOUR_HEIGHT_MAX)])


def titled(blocks: Iterable[Block], hour_height: float, line: int = TITLE_HEIGHT) -> list[Block]:
    """Each block at least a line tall at this scale; one reaching over a later one (in the same day and
    columns) pushes that one's title below it, and that one grows to keep its line."""
    done: list[Block] = []
    for block in sorted(blocks, key=lambda b: (b.day, b.start, -b.end)):
        top = block.start / 3600 * hour_height
        left, right = block.column / block.columns, (block.column + 1) / block.columns
        above = [
            other.start / 3600 * hour_height + other.height
            for other in done
            if other.day == block.day
            and other.column / other.columns < right
            and left < (other.column + 1) / other.columns
        ]
        inset = max([0.0, *(bottom - top for bottom in above)])
        span = (block.end - block.start) / 3600 * hour_height
        done.append(Block(**{**block.__dict__, "inset": inset, "height": max(span, inset + line)}))
    return done


def day_totals(entries: Iterable[Entry], days: list[date], tz: tzinfo, now: datetime) -> list[int]:
    """Seconds of each day shown; an entry counts on the day it began (as the list and Kimai)."""
    totals = dict.fromkeys(days, 0)
    for entry in entries:
        day = local_day(entry.begin, tz)
        if day in totals:
            totals[day] += entry.duration if entry.end is not None else elapsed_seconds(entry.begin, now)
    return [totals[day] for day in days]


def _seconds(moment: datetime) -> int:
    return moment.hour * 3600 + moment.minute * 60 + moment.second


def _columns(blocks: list[Block]) -> list[Block]:
    """Overlapping blocks side by side: each takes the first free column of its group."""
    placed: list[Block] = []
    group: list[Block] = []
    group_end = -1
    ends: list[int] = []  # when each column of the group is free again
    for block in blocks:
        if block.start >= group_end:  # nothing open overlaps: the group so far is finished
            placed.extend(_width(group, len(ends)))
            group, ends, group_end = [], [], block.end
        column = next((i for i, free in enumerate(ends) if free <= block.start), len(ends))
        if column == len(ends):
            ends.append(block.end)
        else:
            ends[column] = block.end
        group.append(Block(**{**block.__dict__, "column": column}))
        group_end = max(group_end, block.end)
    placed.extend(_width(group, len(ends)))
    return placed


def _width(group: list[Block], columns: int) -> list[Block]:
    return [Block(**{**block.__dict__, "columns": columns}) for block in group]
