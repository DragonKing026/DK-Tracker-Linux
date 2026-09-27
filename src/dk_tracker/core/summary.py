"""The main window's summaries (Plan 6, spec 0.10 section 6): a period's totals, averages, the
daily norm, the bar chart and the breakdown by project, customer or activity.

Pure functions; `present` makes every text the QML view shows, so the wording is tested here.
"""

from __future__ import annotations

import calendar
import math
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, tzinfo
from typing import Any, Literal

from .entry_list import first_day_of_week
from .grouping import sort_key
from .models import Entry
from .timefmt import elapsed_seconds, local_day, short_duration

Kind = Literal["week", "month", "year", "range"]
Group = Literal["project", "customer", "activity"]
KINDS: tuple[Kind, ...] = ("week", "month", "year", "range")
GROUPS: tuple[Group, ...] = ("project", "customer", "activity")
MAX_RANGE_DAYS = 366  # fetching stops at 5000 entries (10 pages × 500)
DAY_BARS_LIMIT = 62  # more daily bars do not fit the narrowest window
RING_SLICES = 8  # more slices are unreadable; the rest go together
_STEPS_MINUTES = (15, 30) + tuple(
    hours * 60
    for hours in (
        1,
        2,
        3,
        4,
        5,
        6,
        8,
        10,
        12,
        15,
        20,
        25,
        30,
        40,
        50,
        60,
        80,
        100,
        120,
        150,
        200,
        250,
        300,
        400,
        500,
    )
)
_TICKS = 4


@dataclass(frozen=True)
class Span:
    kind: Kind
    first: date
    last: date  # included

    @property
    def days(self) -> int:
        return (self.last - self.first).days + 1


@dataclass(frozen=True)
class Part:
    key: str  # the project's key ("p7") — bars are always split by project
    seconds: int


@dataclass(frozen=True)
class Bucket:
    first: date
    last: date
    seconds: int = 0
    parts: tuple[Part, ...] = ()
    norm: int = 0  # the norm for this bar: a day's, or a day's × days with entries in the month
    days_with: int = 0


@dataclass(frozen=True)
class Share:
    key: str
    name: str
    detail: str  # a project's customer; "" otherwise
    color: str
    seconds: int
    billable: int


@dataclass(frozen=True)
class Summary:
    span: Span
    unit: Literal["day", "month"]
    total: int
    billable: int
    days_with: int
    weeks_with: int
    months_with: int
    weeks_spanned: int
    months_spanned: int
    norm: int  # a day's norm in seconds; 0 = none
    buckets: tuple[Bucket, ...]
    shares: dict[str, tuple[Share, ...]] = field(default_factory=dict)

    @property
    def avg_day(self) -> float:
        """Time ÷ days with entries (spec, section 3), not ÷ days of the period."""
        return self.total / self.days_with if self.days_with else 0

    @property
    def avg_week(self) -> float | None:
        if self.weeks_spanned <= 1:
            return None
        return self.total / self.weeks_with if self.weeks_with else 0

    @property
    def avg_month(self) -> float | None:
        if self.months_spanned <= 1:
            return None
        return self.total / self.months_with if self.months_with else 0


# -- periods -------------------------------------------------------------------------------


def span_for(kind: Kind, day: date, first_weekday: int) -> Span:
    """The week, month or year holding `day`; a range starts as that week."""
    if kind == "month":
        return Span("month", day.replace(day=1), _month_end(day))
    if kind == "year":
        return Span("year", date(day.year, 1, 1), date(day.year, 12, 31))
    first = first_day_of_week(day, first_weekday)
    return Span("week" if kind == "week" else "range", first, first + timedelta(days=6))


def shifted(span: Span, steps: int, first_weekday: int) -> Span:
    """◀ ▶: one period back or on; a range by its own length."""
    if span.kind == "month":
        return span_for("month", _add_months(span.first, steps), first_weekday)
    if span.kind == "year":
        return span_for("year", date(span.first.year + steps, 1, 1), first_weekday)
    length = timedelta(days=(7 if span.kind == "week" else span.days) * steps)
    return Span(span.kind, span.first + length, span.last + length)


def range_span(first: date, last: date) -> Span:
    """Two days typed in any order; at most MAX_RANGE_DAYS from the first."""
    first, last = min(first, last), max(first, last)
    return Span("range", first, min(last, first + timedelta(days=MAX_RANGE_DAYS - 1)))


def span_label(span: Span, today: date, t: Callable[..., str]) -> str:
    if span.kind == "month":
        return f"{_months_long(t)[span.first.month - 1]} {span.first.year}"
    if span.kind == "year":
        return str(span.first.year)
    return _dates(span.first, span.last, t)


# -- counting ------------------------------------------------------------------------------


def summarize(
    entries: Iterable[Entry], span: Span, tz: tzinfo, *, now: datetime, norm: int, first_weekday: int
) -> Summary:
    """Entries of the period (a running one counts until `now`), each on the day it began."""
    unit: Literal["day", "month"] = "day" if span.kind != "year" and span.days <= DAY_BARS_LIMIT else "month"
    counted: list[tuple[date, Entry, int]] = []
    for entry in entries:
        day = local_day(entry.begin, tz)
        if span.first <= day <= span.last:
            seconds = entry.duration if entry.end is not None else elapsed_seconds(entry.begin, now)
            counted.append((day, entry, seconds))

    shares = {group: _shares(counted, group) for group in ("project", "customer", "activity")}
    order = {share.key: index for index, share in enumerate(shares["project"])}
    days = {day for day, _, _ in counted}
    buckets = tuple(
        _bucket(first, last, [(d, e, s) for d, e, s in counted if first <= d <= last], order, norm, unit)
        for first, last in _bucket_spans(span, unit)
    )
    return Summary(
        span=span,
        unit=unit,
        total=sum(seconds for _, _, seconds in counted),
        billable=sum(seconds for _, entry, seconds in counted if entry.billable),
        days_with=len(days),
        weeks_with=len({first_day_of_week(day, first_weekday) for day in days}),
        months_with=len({(day.year, day.month) for day in days}),
        weeks_spanned=len(
            {first_day_of_week(span.first + timedelta(days=i), first_weekday) for i in range(span.days)}
        ),
        months_spanned=(span.last.year - span.first.year) * 12 + span.last.month - span.first.month + 1,
        norm=norm,
        buckets=buckets,
        shares=shares,
    )


def nice_scale(highest: float) -> tuple[int, int]:
    """The chart's top and step in seconds: a round step, at most four of them."""
    if highest <= 0:
        return 3600, 3600
    for minutes in _STEPS_MINUTES:
        step = minutes * 60
        if math.ceil(highest / step) <= _TICKS:
            return math.ceil(highest / step) * step, step
    step = _STEPS_MINUTES[-1] * 60
    return math.ceil(highest / step) * step, step


# -- texts for the view --------------------------------------------------------------------


def present(summary: Summary, t: Callable[..., str], *, group: Group, today: date) -> dict[str, Any]:
    """Everything the summary view draws, as plain values (QML only binds to them)."""
    total, norm = summary.total, summary.norm
    projects = {share.key: share for share in summary.shares["project"]}
    highest = max(
        [bucket.seconds for bucket in summary.buckets] + [bucket.norm for bucket in summary.buckets]
    )
    top, step = nice_scale(highest)
    label_every = 7 if summary.unit == "day" and len(summary.buckets) > 31 else 1
    shares = summary.shares[group]
    return {
        "empty": total == 0,
        "unit": summary.unit,
        "total": short_duration(total),
        "daysWith": t("sumDaysWith", count=summary.days_with),
        "paid": short_duration(summary.billable),
        "paidPercent": _percent(summary.billable, total, t),
        "paidFraction": summary.billable / total if total else 0.0,
        "unpaid": short_duration(total - summary.billable),
        "unpaidPercent": _percent(total - summary.billable, total, t),
        "avgDay": short_duration(summary.avg_day),
        "norm": short_duration(norm) if norm else "",
        "normDiff": _signed(summary.avg_day - norm) if norm and summary.days_with else "",
        "normFraction": min(summary.avg_day / norm, 1.0) if norm else 0.0,
        "avgWeek": short_duration(summary.avg_week) if summary.avg_week is not None else "",
        "avgMonth": short_duration(summary.avg_month) if summary.avg_month is not None else "",
        "normLine": norm if summary.unit == "day" else 0,
        "scaleTop": top,
        "ticks": [{"seconds": s, "label": short_duration(s)} for s in range(0, top + 1, step)],
        "bars": [
            _bar(bucket, index, summary, projects, label_every, today, t)
            for index, bucket in enumerate(summary.buckets)
        ],
        "shares": [
            {
                "key": share.key,
                "name": share.name or t("sumNoName"),
                "detail": share.detail,
                "color": share.color,
                "time": short_duration(share.seconds),
                "percent": _percent(share.seconds, total, t),
                "paid": short_duration(share.billable),
                "fraction": share.seconds / total if total else 0.0,
            }
            for share in shares
        ],
        "slices": _slices(shares, total, t),
    }


# -- internals -----------------------------------------------------------------------------


def _key_name_color(entry: Entry, group: str) -> tuple[str, str, str, str]:
    if group == "customer":
        return f"c{entry.customer_id}", entry.customer_name or "", "", entry.customer_color or ""
    if group == "activity":
        return f"a{entry.activity_id}", entry.activity_name or "", "", entry.activity_color or ""
    return (
        f"p{entry.project_id}",
        entry.project_name or "",
        entry.customer_name or "",
        entry.project_color or "",
    )


def _shares(counted: list[tuple[date, Entry, int]], group: str) -> tuple[Share, ...]:
    found: dict[str, Share] = {}
    for _, entry, seconds in counted:
        key, name, detail, color = _key_name_color(entry, group)
        old = found.get(key) or Share(key, name, detail, color, 0, 0)
        found[key] = Share(
            key,
            old.name,
            old.detail,
            old.color,
            old.seconds + seconds,
            old.billable + (seconds if entry.billable else 0),
        )
    return tuple(sorted(found.values(), key=lambda share: (-share.seconds, sort_key(share.name))))


def _bucket_spans(span: Span, unit: str) -> list[tuple[date, date]]:
    if unit == "day":
        return [(day, day) for day in (span.first + timedelta(days=i) for i in range(span.days))]
    spans, first = [], span.first
    while first <= span.last:
        last = min(_month_end(first), span.last)
        spans.append((first, last))
        first = last + timedelta(days=1)
    return spans


def _bucket(
    first: date,
    last: date,
    counted: list[tuple[date, Entry, int]],
    order: dict[str, int],
    norm: int,
    unit: str,
) -> Bucket:
    by_project: dict[str, int] = {}
    for _, entry, seconds in counted:
        key = f"p{entry.project_id}"
        by_project[key] = by_project.get(key, 0) + seconds
    days_with = len({day for day, _, _ in counted})
    return Bucket(
        first=first,
        last=last,
        seconds=sum(by_project.values()),
        # The biggest project of the whole period at the bottom of every bar, the same order everywhere.
        parts=tuple(
            Part(key, seconds) for key, seconds in sorted(by_project.items(), key=lambda kv: order[kv[0]])
        ),
        norm=norm if unit == "day" else norm * days_with,
        days_with=days_with,
    )


def _bar(
    bucket: Bucket,
    index: int,
    summary: Summary,
    projects: dict[str, Share],
    label_every: int,
    today: date,
    t: Callable[..., str],
) -> dict[str, Any]:
    months = t("monthsShort").split(",")
    day = bucket.first
    if summary.unit == "month":
        label = months[day.month - 1]
        title = f"{_months_long(t)[day.month - 1]} {day.year}"
    else:
        weekdays = t("weekdaysShort").split(",")
        label = (
            t("sumBarDay", weekday=weekdays[day.weekday()], day=day.day)
            if summary.span.kind == "week"
            else str(day.day)
        )
        title = t("dayOther", weekday=weekdays[day.weekday()], day=day.day, month=months[day.month - 1])
        if day.year != today.year:
            title = f"{title} {day.year}"
    return {
        "label": label if index % label_every == 0 else "",
        "title": title,
        "total": short_duration(bucket.seconds),
        "seconds": bucket.seconds,
        "norm": bucket.norm,
        "today": bucket.first <= today <= bucket.last,
        "parts": [
            {
                "name": projects[part.key].name or t("sumNoName"),
                "color": projects[part.key].color,
                "seconds": part.seconds,
                "time": short_duration(part.seconds),
            }
            for part in bucket.parts  # bottom up; the tooltip lists them in the same order
        ],
    }


def _slices(shares: tuple[Share, ...], total: int, t: Callable[..., str]) -> list[dict[str, Any]]:
    if not total:
        return []
    shown = [
        {"name": s.name or t("sumNoName"), "color": s.color, "fraction": s.seconds / total} for s in shares
    ]
    if len(shown) <= RING_SLICES + 1:  # one leftover slice would only rename it
        return shown
    rest = sum(item["fraction"] for item in shown[RING_SLICES:])
    return [*shown[:RING_SLICES], {"name": t("sumOthers"), "color": "", "fraction": rest}]


def _percent(part: float, whole: float, t: Callable[..., str]) -> str:
    return t("sumPercent", value=round(100 * part / whole) if whole else 0)


def _signed(seconds: float) -> str:
    return ("−" if seconds < 0 else "+") + short_duration(abs(seconds))


def _dates(first: date, last: date, t: Callable[..., str]) -> str:
    months = t("monthsShort").split(",")
    if first.year != last.year:
        head = f"{first.day} {months[first.month - 1]} {first.year}"
    elif first.month != last.month:
        head = f"{first.day} {months[first.month - 1]}"
    else:
        head = str(first.day)
    return t("weekRange", first=head, last=f"{last.day} {months[last.month - 1]} {last.year}")


def _months_long(t: Callable[..., str]) -> list[str]:
    return t("monthsLong").split(",")


def _month_end(day: date) -> date:
    return day.replace(day=calendar.monthrange(day.year, day.month)[1])


def _add_months(day: date, months: int) -> date:
    index = day.year * 12 + day.month - 1 + months
    return date(index // 12, index % 12 + 1, 1)
