"""The main window's summaries (Plan 6, spec 0.10 section 6): a period's totals, averages, the
daily norm, the bar chart and the breakdown by project, customer or activity.

Pure functions; `present` makes every text the QML view shows, so the wording is tested here.
"""

from __future__ import annotations

import calendar
import math
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field, replace
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
TIP_ITEMS = 10  # descriptions a tooltip lists before "+ n more"
MONTH_TIP_ITEMS = 3  # a month's bar: fewer a project, or its tooltip would outgrow the window
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
    items: tuple[tuple[str, int], ...] = ()  # (description, seconds), biggest first — the tooltip


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
    items: tuple[tuple[str, int], ...] = ()  # (description, seconds), biggest first — the tooltip (as Toggl)


@dataclass(frozen=True)
class Summary:
    span: Span
    unit: Literal["day", "month"]
    total: int
    billable: int
    days_with: int
    work_days: int  # Monday–Friday of the period, until today in the current one (no holidays)
    norm: int  # a day's norm in seconds; 0 = none
    buckets: tuple[Bucket, ...]
    shares: dict[str, tuple[Share, ...]] = field(default_factory=dict)

    @property
    def avg_day(self) -> float:
        """The one average, for any period: time ÷ working days (the user after the live test of
        0.10.3) — a Saturday's work raises it instead of lowering it. A period without working days
        (a weekend) falls back to its days with entries."""
        days = self.work_days or self.days_with
        return self.total / days if days else 0


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
    today = local_day(now, tz)
    buckets = tuple(
        _bucket(
            first,
            last,
            [(d, e, s) for d, e, s in counted if first <= d <= last],
            order,
            norm if unit == "day" else norm * _work_days(first, last, today),
            unit,
        )  # fmt: skip
        for first, last in _bucket_spans(span, unit)
    )
    return Summary(
        span=span,
        unit=unit,
        total=sum(seconds for _, _, seconds in counted),
        billable=sum(seconds for _, entry, seconds in counted if entry.billable),
        days_with=len(days),
        work_days=_work_days(span.first, span.last, today),
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
    unpaid = total - summary.billable
    return {
        "empty": total == 0,
        "unit": summary.unit,
        "total": short_duration(total),
        "daysWith": t("sumDaysLine", work=summary.work_days, count=summary.days_with),
        "paid": short_duration(summary.billable),
        "paidPercent": _percent(summary.billable, total, t),
        "paidFraction": summary.billable / total if total else 0.0,
        "unpaid": short_duration(total - summary.billable),
        "unpaidPercent": _percent(total - summary.billable, total, t),
        "avgDay": short_duration(summary.avg_day),
        "norm": short_duration(norm) if norm else "",
        "normDiff": _signed(summary.avg_day - norm) if norm and summary.total else "",
        "normFraction": min(summary.avg_day / norm, 1.0) if norm else 0.0,
        "unpaidLine": t("sumUnpaidLine", time=short_duration(unpaid), percent=_percent(unpaid, total, t)),
        "normText": t("sumNormLine", norm=short_duration(norm), diff=_signed(summary.avg_day - norm))
        if norm and summary.total
        else "",
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
                **_tip([(text or t("sumNoDescription"), seconds) for text, seconds in share.items], t),
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
    items: dict[str, dict[str, int]] = {}
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
        text = " ".join(entry.description.split())  # the same description, however it was spaced
        by_text = items.setdefault(key, {})
        by_text[text] = by_text.get(text, 0) + seconds
    found = {key: replace(share, items=_biggest(items[key])) for key, share in found.items()}
    return tuple(sorted(found.values(), key=lambda share: (-share.seconds, sort_key(share.name))))


def _work_days(first: date, last: date, today: date) -> int:
    """Monday–Friday from `first` to `last`, but not past today (the days to come are not owed yet)."""
    last = min(last, today)
    return sum(1 for i in range((last - first).days + 1) if (first + timedelta(days=i)).weekday() < 5)


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
    texts: dict[str, dict[str, int]] = {}
    for _, entry, seconds in counted:
        key = f"p{entry.project_id}"
        by_project[key] = by_project.get(key, 0) + seconds
        by_text = texts.setdefault(key, {})
        text = " ".join(entry.description.split())
        by_text[text] = by_text.get(text, 0) + seconds
    days_with = len({day for day, _, _ in counted})
    return Bucket(
        first=first,
        last=last,
        seconds=sum(by_project.values()),
        # The biggest project of the whole period at the bottom of every bar, the same order everywhere.
        parts=tuple(
            Part(key, seconds, _biggest(texts[key]))
            for key, seconds in sorted(by_project.items(), key=lambda kv: order[kv[0]])
        ),
        norm=norm,  # a day's, or the month's (a day's × its working days until today)
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
        "normText": t("sumNormTip", time=short_duration(bucket.norm)) if bucket.norm else "",
        "today": bucket.first <= today <= bucket.last,
        "parts": [
            {
                "name": projects[part.key].name or t("sumNoName"),
                "color": projects[part.key].color,
                "seconds": part.seconds,
                "below": sum(lower.seconds for lower in bucket.parts[:index]),  # where the layer starts
                "time": short_duration(part.seconds),
                **_tip(
                    [(text or t("sumNoDescription"), seconds) for text, seconds in part.items],
                    t,
                    MONTH_TIP_ITEMS if summary.unit == "month" else TIP_ITEMS,
                ),
            }
            for index, part in enumerate(bucket.parts)  # bottom up; the tooltip lists them in this order too
        ],
    }


def _slices(shares: tuple[Share, ...], total: int, t: Callable[..., str]) -> list[dict[str, Any]]:
    if not total:
        return []
    shown = [
        {"name": s.name or t("sumNoName"), "color": s.color, "fraction": s.seconds / total, "index": index}
        for index, s in enumerate(shares)
    ]
    if len(shown) > RING_SLICES + 1:  # one leftover slice would only rename it
        rest = sum(item["fraction"] for item in shown[RING_SLICES:])
        others = [(s.name or t("sumNoName"), s.seconds) for s in shares[RING_SLICES:]]
        shown = [
            *shown[:RING_SLICES],
            {
                "name": t("sumOthers"),
                "color": "",
                "fraction": rest,
                "index": -1,
                "time": short_duration(sum(seconds for _, seconds in others)),
                "percent": _percent(rest, 1, t),
                **_tip(others, t),
            },
        ]
    start = 0.0
    for item in shown:  # where each slice begins, as a fraction of the ring
        item["start"], start = start, start + item["fraction"]
    return shown


def _biggest(by_text: dict[str, int]) -> tuple[tuple[str, int], ...]:
    return tuple(sorted(by_text.items(), key=lambda item: (-item[1], sort_key(item[0]))))


def _tip(items: list[tuple[str, int]], t: Callable[..., str], limit: int = TIP_ITEMS) -> dict[str, Any]:
    """What a tooltip lists: the biggest first, and how many more there are."""
    more = len(items) - limit
    return {
        "entries": [{"text": text, "time": short_duration(seconds)} for text, seconds in items[:limit]],
        "more": t("sumMore", count=more) if more > 0 else "",
    }


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
