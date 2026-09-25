"""What the tray icon and the window say, as plain text — computed here, without Qt,
so every wording and format is tested on its own (F-02, F-08, F-12)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta, tzinfo
from typing import Literal

from .errors import describe
from .models import Entry
from .timefmt import badge_label, clock, elapsed_seconds, hhmm, short_duration, zone
from .tracker import Snapshot

Kind = Literal["unconfigured", "idle", "running", "error"]


@dataclass(frozen=True)
class TrayStatus:
    kind: Kind
    label: str  # drawn inside the icon: "47m", "1:22", "!" or nothing
    tooltip: str


@dataclass(frozen=True)
class RowText:
    description: str
    empty: bool  # "(no description)" is shown dimmed
    meta: str  # "project - activity"
    duration: str  # "1:50"
    span: str  # "15:15-17:05"


def display_zone(snapshot: Snapshot, local_now: datetime) -> tzinfo:
    """Times are shown in the Kimai account's zone — the one they are saved in."""
    user = snapshot.user
    return (zone(user.timezone) if user else None) or local_now.tzinfo or UTC


def tray_status(snapshot: Snapshot, configured: bool, now: datetime, t: Callable[..., str]) -> TrayStatus:
    title = t("appName")
    if not configured:
        return TrayStatus("unconfigured", "", f"{title}\n{t('notConfigured')}")
    if snapshot.error is not None:
        # As in the add-on: a failed poll is shown even while an entry runs.
        return TrayStatus("error", "!", f"{title}\n{describe(snapshot.error, t)}")
    current = snapshot.current
    if current is None:
        lines = [title, t("tooltipIdle")]
        if snapshot.totals is not None:
            lines.append(t("todayTotal", time=short_duration(snapshot.totals.today)))
        return TrayStatus("idle", "", "\n".join(lines))
    seconds = elapsed_seconds(current.begin, now)
    lines = [f"{title} — {clock(seconds)}", _what(current, t)]
    if len(snapshot.running) > 1:
        lines.append(t("tooltipMoreRunning", count=len(snapshot.running) - 1))
    return TrayStatus("running", badge_label(seconds), "\n".join(lines))


def day_label(day: date, today: date, t: Callable[..., str]) -> str:
    if day == today:
        return t("dayToday")
    if day == today - timedelta(days=1):
        return t("dayYesterday")
    weekdays = t("weekdaysShort").split(",")
    months = t("monthsShort").split(",")
    return t("dayOther", weekday=weekdays[day.weekday()], day=day.day, month=months[day.month - 1])


def entry_row(entry: Entry, tz: tzinfo, t: Callable[..., str]) -> RowText:
    text = " ".join(entry.description.split())
    names = [name for name in (entry.project_name, entry.activity_name) if name]
    span = hhmm(entry.begin, tz) + (f"-{hhmm(entry.end, tz)}" if entry.end else "")
    return RowText(
        description=text or t("noDescription"),
        empty=not text,
        meta=" - ".join(names),
        duration=short_duration(entry.duration),
        span=span,
    )


def _what(entry: Entry, t: Callable[..., str]) -> str:
    text = " ".join(entry.description.split()) or t("noDescription")
    return f"{entry.project_name} — {text}" if entry.project_name else text
