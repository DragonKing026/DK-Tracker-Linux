"""Application logic of Kimai Tray — what the WS Tracker popup did, without any UI.

Every public method returns a new Snapshot, the single source of truth the UI renders.
Actions raise TrackerError when a rule of the app says no and ApiError when Kimai does;
refreshes never raise — a failure is recorded in the Snapshot instead.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, replace
from datetime import UTC, datetime, tzinfo
from typing import Any

from .billable import default_billable
from .errors import ApiError
from .grouping import sort_key
from .models import Activity, Entry, Project, User
from .settings import Memory, Settings
from .timefmt import day_end, elapsed_seconds, kimai_stamp, local_day, week_start, zone

RECENT_SIZE = 20


@dataclass(frozen=True)
class Totals:
    today: int = 0
    week: int = 0


@dataclass(frozen=True)
class Snapshot:
    user: User | None = None
    running: tuple[Entry, ...] = ()
    recent: tuple[Entry, ...] = ()
    totals: Totals | None = None
    projects: tuple[Project, ...] = ()
    non_billable_customers: frozenset[int] = frozenset()
    error: ApiError | None = None
    failures: int = 0
    billable_allowed: bool = True
    timezone_mismatch: bool = False
    notice: str | None = None  # i18n key of a one-off message ("savedDescription", ...)

    @property
    def current(self) -> Entry | None:
        return self.running[0] if self.running else None


def utc_now() -> datetime:
    return datetime.now(UTC)


def _system_now() -> datetime:
    return datetime.now().astimezone()


def live_totals(snapshot: Snapshot, now: datetime) -> Totals:
    """Totals count closed entries only; the running ones are added by the clock."""
    base = snapshot.totals or Totals()
    live = sum(elapsed_seconds(entry.begin, now) for entry in snapshot.running)
    return Totals(today=base.today + live, week=base.week + live)


def all_entries_url(kimai_url: str, locale: str) -> str:
    """Kimai has no locale-free route: /timesheet/ is a 404, /{locale}/timesheet/ is not."""
    return f"{kimai_url.rstrip('/')}/{locale}/timesheet/"


class Tracker:
    def __init__(
        self,
        client: Any,
        settings: Settings,
        memory: Memory,
        *,
        save_memory: Callable[[Memory], None] = lambda memory: None,
        now: Callable[[], datetime] = utc_now,
        local_now: Callable[[], datetime] = _system_now,
    ) -> None:
        self._client = client
        self._settings = settings.normalized()
        self._memory = memory
        self._save_memory = save_memory
        self._now = now
        self._local_now = local_now
        self._snapshot = Snapshot(billable_allowed=memory.billable_allowed)

    @property
    def snapshot(self) -> Snapshot:
        return self._snapshot

    @property
    def memory(self) -> Memory:
        return self._memory

    @property
    def settings(self) -> Settings:
        return self._settings

    # -- refresh ---------------------------------------------------------------

    def refresh_active(self) -> Snapshot:
        """The cheap one-minute poll behind the tray icon."""
        try:
            user = self._snapshot.user or self._client.me()
            running = self._running(self._client.active())
        except ApiError as error:
            return self._failed(error)
        return self._succeeded(user=user, running=running)

    def refresh_full(self) -> Snapshot:
        """Everything the window shows: running entry, recent entries and totals."""
        try:
            user = self._client.me()
            running = self._running(self._client.active())
            recent = tuple(entry for entry in self._client.latest(RECENT_SIZE) if not entry.running)
        except ApiError as error:
            return self._failed(error)
        self._remember_locale(user, recent)
        return self._succeeded(user=user, running=running, recent=recent, totals=self._totals(user))

    def load_catalog(self) -> Snapshot:
        """Projects plus the customers that make them non-billable (their failure is tolerated)."""
        projects = self._client.projects()
        try:
            customers = self._client.customers()
        except ApiError:
            customers = []
        non_billable = frozenset(customer.id for customer in customers if not customer.billable)
        return self._set(projects=tuple(projects), non_billable_customers=non_billable)

    def activities(self, project_id: int | None) -> list[Activity]:
        return sorted(self._client.activities(project_id), key=lambda activity: sort_key(activity.name))

    def default_billable(self, project_id: int | None, activity: Activity | None) -> bool:
        project = next((p for p in self._snapshot.projects if p.id == project_id), None)
        return default_billable(project, activity, self._snapshot.non_billable_customers)

    def kimai_tz(self) -> tzinfo:
        """The zone Kimai reads submitted times in; the system's if Kimai's is unknown here."""
        user = self._snapshot.user
        if user is None:
            user = self._client.me()
            self._set(user=user)
        return self._zone_for(user)

    # -- internals ---------------------------------------------------------------

    def _set(self, **changes: Any) -> Snapshot:
        self._snapshot = replace(self._snapshot, **changes)
        return self._snapshot

    def _succeeded(self, *, user: User, **changes: Any) -> Snapshot:
        return self._set(
            user=user,
            error=None,
            failures=0,
            notice=None,
            timezone_mismatch=self._mismatch(user),
            **changes,
        )

    def _failed(self, error: ApiError) -> Snapshot:
        return self._set(error=error, failures=self._snapshot.failures + 1, notice=None)

    @staticmethod
    def _running(entries: list[Entry]) -> tuple[Entry, ...]:
        return tuple(sorted((e for e in entries if e.running), key=lambda e: e.begin, reverse=True))

    def _zone_for(self, user: User) -> tzinfo:
        return zone(user.timezone) or self._local_now().tzinfo or UTC

    def _mismatch(self, user: User) -> bool:
        kimai = zone(user.timezone)
        if kimai is None:
            return True
        local = self._local_now()
        return local.utcoffset() != local.astimezone(kimai).utcoffset()

    def _totals(self, user: User) -> Totals | None:
        tz = self._zone_for(user)
        now = self._now()
        try:
            entries = self._client.range(
                kimai_stamp(week_start(now, tz), tz), kimai_stamp(day_end(now, tz), tz)
            )
        except ApiError:
            return None  # the header just hides the totals, as in the add-on
        finished = [entry for entry in entries if not entry.running]
        today = local_day(now, tz)
        return Totals(
            today=sum(e.duration for e in finished if local_day(e.begin, tz) == today),
            week=sum(e.duration for e in finished),
        )

    def _remember_locale(self, user: User, recent: tuple[Entry, ...]) -> None:
        language = next((e.user_language for e in recent if e.user_language), None) or user.language
        if language and language != self._memory.kimai_locale:
            self._update_memory(kimai_locale=language)

    def _update_memory(self, **changes: Any) -> None:
        self._memory = replace(self._memory, **changes)
        self._save_memory(self._memory)
