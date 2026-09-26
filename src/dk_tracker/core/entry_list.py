"""The main window's list (Plan 5): weeks, then days, then entries — each with its total.

Plain rows with ready texts, so the QML view only draws and every wording is tested here.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import date, timedelta, tzinfo
from typing import Literal

from .grouping import day_total
from .models import Entry
from .presentation import day_label
from .timefmt import local_day, short_duration

Kind = Literal["week", "day", "entry"]


@dataclass(frozen=True)
class ListRow:
    kind: Kind
    key: str  # stable across refreshes: "week:2026-09-21", "day:2026-09-25", "entry:7"
    label: str  # week and day headers; "" for an entry
    total: str  # "h:mm" — of the week, the day, or the entry
    entry: Entry | None = None


def first_day_of_week(day: date, first_weekday: int) -> date:
    """0 = Monday … 6 = Sunday, as the Kimai account says."""
    return day - timedelta(days=(day.weekday() - first_weekday) % 7)


def build_rows(
    entries: Iterable[Entry], tz: tzinfo, today: date, first_weekday: int, t: Callable[..., str]
) -> list[ListRow]:
    """Entries newest first, as the tracker gives them."""
    weeks: dict[date, dict[date, list[Entry]]] = {}
    for entry in entries:
        day = local_day(entry.begin, tz)
        weeks.setdefault(first_day_of_week(day, first_weekday), {}).setdefault(day, []).append(entry)
    this_week = first_day_of_week(today, first_weekday)
    rows: list[ListRow] = []
    for week, days in weeks.items():
        total = sum(day_total(day_entries) for day_entries in days.values())
        rows.append(ListRow("week", f"week:{week}", _week_label(week, this_week, t), short_duration(total)))
        for day, day_entries in days.items():
            rows.append(
                ListRow("day", f"day:{day}", day_label(day, today, t), short_duration(day_total(day_entries)))
            )
            rows.extend(
                ListRow("entry", f"entry:{entry.id}", "", short_duration(entry.duration), entry)
                for entry in day_entries
            )
    return rows


def _week_label(week: date, this_week: date, t: Callable[..., str]) -> str:
    if week == this_week:
        return t("weekThis")
    if week == this_week - timedelta(days=7):
        return t("weekLast")
    last = week + timedelta(days=6)
    months = t("monthsShort").split(",")

    def short(day: date, with_year: bool) -> str:
        text = f"{day.day} {months[day.month - 1]}"
        return f"{text} {day.year}" if with_year else text

    across_years = week.year != last.year
    with_year = across_years or last.year != this_week.year
    return t("weekRange", first=short(week, across_years), last=short(last, with_year))
