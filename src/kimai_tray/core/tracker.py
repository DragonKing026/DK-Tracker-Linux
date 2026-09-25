"""Application logic of Kimai Tray — what the WS Tracker popup did, without any UI.

Every public method returns a new Snapshot, the single source of truth the UI renders.
Actions raise TrackerError when a rule of the app says no and ApiError when Kimai does;
refreshes never raise — a failure is recorded in the Snapshot instead.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass, replace
from datetime import UTC, datetime, tzinfo
from typing import Any

from .billable import default_billable, is_billable_rejected
from .errors import ApiError, ErrorKind, TrackerError
from .grouping import sort_key
from .models import Activity, Entry, Project, User
from .settings import Memory, Settings
from .timefmt import (
    at_wall_clock,
    day_end,
    elapsed_seconds,
    kimai_stamp,
    local_day,
    start_stamp,
    week_start,
    zone,
)
from .validation import check_description

RECENT_SIZE = 20
log = logging.getLogger(__name__)


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
    timezone_missing: bool = False  # Kimai did not report the account zone; the system's is used
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

    def warnings(self) -> list[tuple[str, dict[str, object]]]:
        """Standing warnings for the window and settings, as (i18n key, params)."""
        user = self._snapshot.user
        if user is None:
            return []
        system = self._local_now().tzname() or "?"
        if self._snapshot.timezone_missing:
            return [("warnTimezoneMissing", {"system": system})]
        if self._snapshot.timezone_mismatch:
            return [("warnTimezone", {"kimai": user.timezone, "system": system})]
        return []

    # -- actions ---------------------------------------------------------------

    def start(
        self,
        *,
        project_id: int | None,
        activity_id: int | None,
        description: str,
        billable: bool | None,
    ) -> Snapshot:
        """F-04. `billable` is None unless the user flipped the switch."""
        project, activity = self._require_choice(project_id, activity_id)
        text = description.strip()
        self._check(text)
        tz = self.kimai_tz()
        begin = start_stamp(self._now(), tz)
        wanted = billable if self._snapshot.billable_allowed else None
        notice = None
        try:
            self._start_once(project, activity, text, begin, wanted)
        except ApiError as error:
            if wanted is None or not is_billable_rejected(error):
                raise
            # The choice cannot be honoured, but the entry must not be lost.
            self._lock_billable()
            self._start_once(project, activity, text, begin, None)
            notice = "errBillableDenied"
        self._update_memory(last_project=project, last_activity=activity)
        self.refresh_full()
        return self._set(notice=notice)

    def stop(self, *, end: str | None = None) -> Snapshot:
        """F-05. An end typed as HH:MM closes the entry there instead of now."""
        current = self._require_running()
        if end:
            tz = self.kimai_tz()
            end_at = self._wall_clock(current.begin, end, tz)
            if end_at <= current.begin:
                raise TrackerError("errEndBeforeBegin")
            self._client.update(current.id, {"end": kimai_stamp(end_at, tz)})
        else:
            self._client.stop(current.id)
        return self.refresh_full()

    def resume(self, entry: Entry) -> Snapshot:
        """F-10. Checked first, so a refused resume never stops the running entry."""
        self._require_choice(entry.project_id, entry.activity_id)
        self._check(entry.description.strip())
        current = self._snapshot.current
        if current is not None:
            self._client.stop(current.id)
        # Repeating an entry repeats how it was billed, not the project default.
        try:
            return self.start(
                project_id=entry.project_id,
                activity_id=entry.activity_id,
                description=entry.description,
                billable=entry.billable,
            )
        except Exception:
            # The running entry is already stopped; do not keep showing it as running.
            self.refresh_full()
            raise

    def update_description(self, text: str, *, quiet: bool = False) -> Snapshot | None:
        """F-07. `quiet` is the save-while-typing path: an invalid text is just not saved."""
        current = self._require_running()
        text = text.strip()
        if text == current.description:
            return None
        check = check_description(text, self._settings.min_description)
        if not check.ok:
            if quiet:
                return None
            raise self._description_error(check.reason, check.word)
        updated = self._client.update(current.id, {"description": text})
        return self._merge(updated, notice="savedDescription")

    def update_begin(self, hhmm_value: str) -> Snapshot:
        """F-07. Same day as the original start, never in the future."""
        current = self._require_running()
        tz = self.kimai_tz()
        begin = self._wall_clock(current.begin, hhmm_value, tz)
        if begin > self._now():
            raise TrackerError("errBeginFuture")
        updated = self._client.update(current.id, {"begin": kimai_stamp(begin, tz)})
        return self._merge(updated, notice="savedTime")

    def set_billable(self, entry_id: int, value: bool) -> Snapshot:
        """F-09. The `$` on a running or a recent entry."""
        if not self._snapshot.billable_allowed:
            raise TrackerError("billableLocked")
        try:
            updated = self._client.update(entry_id, {"billable": value})
        except ApiError as error:
            if is_billable_rejected(error):
                self._lock_billable()
                raise TrackerError("errBillableDenied") from error
            raise
        return self._merge(updated, notice="savedBillable")

    def apply_settings(self, settings: Settings, client: Any) -> Snapshot:
        """Saving the settings is the moment to look at the billable permission again."""
        self._settings = settings.normalized()
        self._client = client
        self._update_memory(billable_allowed=True)
        self._snapshot = Snapshot(billable_allowed=True)
        return self.refresh_full()

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
            timezone_missing=not user.timezone,
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
        if not user.timezone:
            return False  # reported separately as timezone_missing
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
        """Remembered state is a convenience: failing to write it (disk full, read-only home)
        must never turn a successful action into an error — the user would retry and book twice."""
        self._memory = replace(self._memory, **changes)
        try:
            self._save_memory(self._memory)
        except OSError as error:
            log.warning("Could not save app state, keeping it in memory only: %s", error)

    def _require_choice(self, project_id: int | None, activity_id: int | None) -> tuple[int, int]:
        if not project_id:
            raise TrackerError("errNoProject")
        if not activity_id:
            raise TrackerError("errNoActivity")
        return project_id, activity_id

    def _require_running(self) -> Entry:
        current = self._snapshot.current
        if current is None:
            raise TrackerError("errNothingRunning")
        return current

    def _check(self, text: str) -> None:
        check = check_description(text, self._settings.min_description)
        if not check.ok:
            raise self._description_error(check.reason, check.word)

    def _description_error(self, reason: str | None, word: str | None) -> TrackerError:
        if reason == "generic":
            return TrackerError("errDescGeneric", word=word)
        return TrackerError("errDescShort", chars=self._settings.min_description)

    @staticmethod
    def _wall_clock(anchor: datetime, hhmm_value: str, tz: tzinfo) -> datetime:
        try:
            return at_wall_clock(anchor, hhmm_value, tz)
        except ValueError:
            raise TrackerError("errInvalidTime") from None

    def _start_once(self, project: int, activity: int, text: str, begin: str, billable: bool | None) -> None:
        try:
            self._client.start(
                project_id=project, activity_id=activity, description=text, begin=begin, billable=billable
            )
        except ApiError as error:
            # A timed-out POST may still have reached Kimai: look before reporting a failure,
            # and never post again — that would book the time twice.
            if error.kind is not ErrorKind.TIMEOUT or not self._started_anyway(project, activity, text):
                raise

    def _started_anyway(self, project: int, activity: int, text: str) -> bool:
        try:
            running = self._client.active()
        except ApiError:
            return False
        return any(
            e.project_id == project and e.activity_id == activity and e.description == text for e in running
        )

    def _lock_billable(self) -> None:
        self._update_memory(billable_allowed=False)
        self._set(billable_allowed=False)

    def _merge(self, updated: Entry, *, notice: str) -> Snapshot:
        """PATCH replies carry related objects as ids; keep the names and colours we had."""

        def merge(entry: Entry) -> Entry:
            if entry.id != updated.id:
                return entry
            return replace(
                entry,
                begin=updated.begin,
                end=updated.end,
                duration=updated.duration,
                description=updated.description,
                billable=updated.billable,
            )

        return self._set(
            running=tuple(merge(e) for e in self._snapshot.running),
            recent=tuple(merge(e) for e in self._snapshot.recent),
            notice=notice,
        )
