"""Which notifications to show (F-21: N-01, N-02, N-02b, N-03) — decided here, sent by desktop/.

A pure function of the snapshot, the settings and a small state, so it is tested without D-Bus.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from .errors import ErrorKind
from .models import Entry
from .settings import Settings
from .timefmt import elapsed_seconds, short_duration
from .tracker import Snapshot

LONG_TIMER = "long-timer"  # notification ids: a new one replaces the old one with the same id
CONNECTION = "connection"
ACTION = "action"
FAILURES_BEFORE_ALERT = 3  # ~3 minutes of failed one-minute polls


@dataclass(frozen=True)
class Notification:
    id: str
    title_key: str
    body_key: str | None = None
    params: dict[str, object] = field(default_factory=dict)
    actions: tuple[str, ...] = ()  # "stop" | "keep" | "settings"


@dataclass(frozen=True)
class PolicyState:
    next_threshold: dict[int, int] = field(default_factory=dict)  # entry id -> seconds
    connection_alerted: bool = False


def evaluate(
    snapshot: Snapshot, settings: Settings, state: PolicyState, now: datetime
) -> tuple[list[Notification], PolicyState]:
    notifications: list[Notification] = []

    # N-01: the long timer, repeated every further hour while it keeps running.
    thresholds: dict[int, int] = {}
    if settings.long_timer_hours > 0:
        first = int(settings.long_timer_hours * 3600)
        for entry in snapshot.running:
            threshold = state.next_threshold.get(entry.id, first)
            elapsed = elapsed_seconds(entry.begin, now)
            if elapsed >= threshold:
                notifications.append(
                    Notification(
                        LONG_TIMER,
                        "notifLongTimerTitle",
                        "notifLongTimerBody",
                        {
                            "time": short_duration(elapsed),
                            "project": entry.project_name or "",
                            "description": entry.description,
                        },
                        ("stop", "keep"),
                    )
                )
                while threshold <= elapsed:
                    threshold += 3600
            thresholds[entry.id] = threshold

    # N-02 / N-02b: one alert per outage, one note when it is over.
    alerted = state.connection_alerted
    error = snapshot.error
    if not settings.notify_connection:
        alerted = False
    elif not alerted and error is not None:
        auth = error.kind is ErrorKind.AUTH
        if auth or snapshot.failures >= FAILURES_BEFORE_ALERT:
            notifications.append(
                Notification(
                    CONNECTION,
                    "notifAuthFailed" if auth else "notifConnectionLost",
                    actions=("settings",) if auth else (),
                )
            )
            alerted = True
    elif alerted and error is None:
        notifications.append(Notification(CONNECTION, "notifConnectionRestored"))
        alerted = False

    return notifications, PolicyState(thresholds, alerted)


def action_confirmation(kind: str, entry: Entry, settings: Settings, now: datetime) -> Notification | None:
    """N-03: the context menu shows no result of its own, so a start or stop is confirmed."""
    if not settings.notify_menu_actions:
        return None
    project = entry.project_name or ""
    if kind == "start":
        return Notification(
            ACTION, "notifStarted", params={"description": entry.description, "project": project}
        )
    seconds = entry.duration or elapsed_seconds(entry.begin, now)
    return Notification(ACTION, "notifStopped", params={"time": short_duration(seconds), "project": project})
