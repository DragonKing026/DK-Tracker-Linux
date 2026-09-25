"""The controller: wires the tray, the window and the settings to the tracker and the desktop.

Threads: the GUI thread only draws. The tracker (HTTP to Kimai) runs on the "kimai" worker,
D-Bus calls (wallet, notifications, autostart) on the "desktop" worker, and notification
clicks arrive from ClickListener. Every result comes back as a Snapshot into AppState.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from dataclasses import replace
from datetime import datetime
from typing import Any

from PySide6.QtCore import QObject, QSize, QTimer, QUrl, Signal
from PySide6.QtGui import QDesktopServices

from kimai_tray.core.errors import TrackerError, describe
from kimai_tray.core.i18n import Translator, resolve_language, system_locale
from kimai_tray.core.models import Entry
from kimai_tray.core.notification_policy import PolicyState, action_confirmation, evaluate, render
from kimai_tray.core.settings import Memory, Settings
from kimai_tray.core.timefmt import short_duration
from kimai_tray.core.tracker import Snapshot, Tracker, all_entries_url, utc_now
from kimai_tray.desktop.bus import PortalError
from kimai_tray.desktop.notifications import NotificationAction
from kimai_tray.desktop.secrets import SecretsLocked, SecretsUnavailable

from . import placement
from .desktop_bridge import ClickListener
from .popup import QuickWindow
from .settings_dialog import SettingsDialog
from .state import AppState
from .tray import Tray
from .worker import Worker

log = logging.getLogger(__name__)
POLL_MS = 60_000  # F-02: GET /api/timesheets/active once a minute
TICK_MS = 1_000  # the clock, only while the window is open
TRAY_MS = 15_000  # tray label and clock-jump check
JUMP_SECONDS = 120  # wall clock moved more than monotonic time: sleep or a clock change
_ENGLISH = Translator("en")


class Controller(QObject):
    languageChanged = Signal(str)
    quitRequested = Signal()

    def __init__(
        self,
        *,
        settings: Settings,
        memory: Memory,
        desktop: Any,
        client_factory: Callable[[str, str], Any],
        save_settings: Callable[[Settings], None],
        save_memory: Callable[[Memory], None],
        now: Callable[[], datetime] = utc_now,
        tray_available: bool,
        window_mode: str,
        listen_for_clicks: bool = True,
    ) -> None:
        super().__init__()
        self._settings = settings.normalized()
        self._memory = memory
        self._desktop = desktop
        self._client_factory = client_factory
        self._save_settings = save_settings
        self._save_memory = save_memory
        self._now = now
        self._tray_available = tray_available
        self._tray_hint = not tray_available and not memory.tray_hint_shown  # spec 7: a one-time hint
        self._tray_hint_saved = False
        self._token: str | None = None
        self._client: Any = None  # the tracker's HTTP client, closed when replaced
        self._tracker: Tracker | None = None
        self._policy = PolicyState()
        self._catalog_loaded = False
        self._last_wall = time.time()
        self._last_mono = time.monotonic()
        self._day = now().astimezone().date()

        self.state = AppState(self._settings, self._translator(self._settings.language))
        self.kimai = Worker("kimai", self)
        self.dbus = Worker("desktop", self)
        self.popup = QuickWindow(self.state, now)
        self.mode = placement.apply(self.popup, window_mode)
        self.popup.set_preferred_size(QSize(memory.popup_width, memory.popup_height))
        self.tray = Tray(self.state, now) if tray_available else None
        self.dialog: SettingsDialog | None = None
        self.listener = ClickListener() if listen_for_clicks else None

        self._poll = QTimer(self, interval=POLL_MS, timeout=self.refresh_active)
        self._tick = QTimer(self, interval=TICK_MS, timeout=self.popup.tick)
        self._tray_timer = QTimer(self, interval=TRAY_MS, timeout=self._on_tray_timer)
        self._connect()

    # -- lifecycle -------------------------------------------------------------------

    def start(self, *, hidden: bool) -> None:
        if self.tray is not None:
            self.tray.show()
        if self.listener is not None:
            self.listener.clicked.connect(self.on_notification)
            self.listener.start()
        self._poll.start()
        self._tray_timer.start()
        self._load_token(self._settings.url)
        if not hidden or self.tray is None:
            self.show_popup()

    def shutdown(self) -> None:
        for timer in (self._poll, self._tick, self._tray_timer):
            timer.stop()
        if self.listener is not None:
            self.listener.stop()
            self.listener.wait(2000)
        self.kimai.shutdown()
        self.dbus.submit(self._desktop.close)
        self.dbus.shutdown(wait=True)
        self.popup.hide()
        if self.tray is not None:
            self.tray.icon.hide()

    def idle(self) -> bool:
        """No job waits for an answer (tests wait for this)."""
        return not self.kimai.busy and not self.dbus.busy

    # -- wiring ------------------------------------------------------------------------

    def _connect(self) -> None:
        form, recent, popup = self.popup.form, self.popup.recent, self.popup
        form.startRequested.connect(lambda payload: self._act(lambda t: t.start(**payload)))
        form.stopRequested.connect(lambda end: self._act(lambda t: t.stop(end=end or None)))
        form.descriptionCommitted.connect(
            lambda text, quiet: self._act(lambda t: t.update_description(text, quiet=quiet) or t.snapshot)
        )
        form.beginCommitted.connect(lambda value: self._act(lambda t: t.update_begin(value)))
        form.billableChanged.connect(self._on_running_billable)
        form.projectChosen.connect(self._load_activities)
        recent.resumeRequested.connect(lambda entry: self._act(lambda t: t.resume(entry)))
        recent.billableRequested.connect(
            lambda entry_id, value: self._act(lambda t: t.set_billable(entry_id, value))
        )
        popup.settingsRequested.connect(self.open_settings)
        popup.openKimaiRequested.connect(self.open_kimai)
        popup.shownChanged.connect(self._on_popup_shown)
        popup.sizeChosen.connect(self._remember_size)
        if self.tray is not None:
            self.tray.openRequested.connect(self.show_popup)
            self.tray.stopRequested.connect(self._menu_stop)
            self.tray.resumeLastRequested.connect(self._menu_resume)
            self.tray.openKimaiRequested.connect(self.open_kimai)
            self.tray.settingsRequested.connect(self.open_settings)
            self.tray.quitRequested.connect(self.quitRequested.emit)

    # -- configuration -------------------------------------------------------------------

    def _load_token(self, url: str) -> None:
        if not url:
            self.state.update(configured=False)
            return
        self.dbus.submit(lambda: self._desktop.get_token(url), self._on_token, self._on_secrets_error)

    def _on_token(self, token: str | None) -> None:
        self._token = token
        self.state.update(secrets_problem=None)
        if not token:
            self.state.update(configured=False)
            return
        self._client = self._client_factory(self._settings.url, token)
        self._tracker = Tracker(
            self._client,
            self._settings,
            self._memory,
            save_memory=self._save_memory,
            now=self._now,
        )
        self.state.update(configured=True)
        if self.popup.isVisible():
            self.refresh_full()
            self._load_catalog()
        else:
            self.refresh_active()

    def _on_secrets_error(self, error: Exception) -> None:
        if isinstance(error, SecretsLocked):
            self.state.update(configured=False, secrets_problem="secretsLocked")
        elif isinstance(error, SecretsUnavailable):
            self.state.update(configured=False, secrets_problem="secretsUnavailable")
        else:
            log.error("Reading the token failed", exc_info=error)
            self.state.update(configured=False, secrets_problem="secretsUnavailable")

    # -- refreshing -------------------------------------------------------------------------

    def refresh_active(self) -> None:
        self._run(lambda t: t.refresh_active(), key="active")

    def refresh_full(self) -> None:
        self._run(lambda t: t.refresh_full(), key="full")

    def _load_catalog(self) -> None:
        if self._catalog_loaded:
            return
        tracker = self._tracker
        if tracker is None:
            return

        def done(result: tuple[Snapshot, list]) -> None:
            self._catalog_loaded = True
            self._apply(result)
            self.popup.form.set_catalog(result[0], tracker.memory.last_project)
            self._load_activities(self.popup.form.project.currentData())

        self.kimai.submit(
            lambda: (tracker.load_catalog(), tracker.warnings()), done, self._on_error, key="catalog"
        )

    def _load_activities(self, project_id: int | None) -> None:
        tracker = self._tracker
        if tracker is None:
            return
        self.kimai.submit(
            lambda: tracker.activities(project_id),
            lambda items: self.popup.form.set_activities(items, tracker.memory.last_activity),
            self._on_error,
            key=f"activities-{project_id}",
        )

    def _run(self, job: Callable[[Tracker], Snapshot], *, key: str | None = None) -> None:
        tracker = self._tracker
        if tracker is None:
            return
        self.kimai.submit(lambda: (job(tracker), tracker.warnings()), self._apply, self._on_error, key=key)

    def _act(
        self, job: Callable[[Tracker], Snapshot], after: Callable[[Snapshot], None] | None = None
    ) -> None:
        """A user action: errors go to the window, the Snapshot as it is then is redrawn."""
        tracker = self._tracker
        if tracker is None:
            return

        def done(result: tuple[Snapshot, list]) -> None:
            self._apply(result)
            if after is not None:
                after(result[0])

        self.popup.clear_error()
        self.kimai.submit(lambda: (job(tracker), tracker.warnings()), done, self._on_error)

    def _apply(self, result: tuple[Snapshot, list]) -> None:
        snapshot, warnings = result
        warnings = list(warnings)
        if self._tray_hint:
            warnings.append(("hintNoTray", {}))
            tracker = self._tracker
            if tracker is not None and not self._tray_hint_saved:
                self._tray_hint_saved = True  # shown this session; the next start stays quiet
                self.kimai.submit(lambda: tracker.remember(tray_hint_shown=True))
        self.state.update(snapshot=snapshot, warnings=warnings)
        notes, self._policy = evaluate(snapshot, self._settings, self._policy, self._now())
        for note in notes:
            self._notify(render(note, self.state.t))

    def _on_error(self, error: Exception) -> None:
        self.popup.show_error(describe(error, self.state.t))
        # In English, whatever the UI language; errors never carry the token (core/errors.py).
        level = logging.INFO if isinstance(error, TrackerError) else logging.WARNING
        log.log(level, "Action failed: %s", describe(error, _ENGLISH))
        if self._tracker is not None:
            # Redraw what is true now (e.g. an optimistic billable switch goes back).
            self.state.update(snapshot=self._tracker.snapshot)

    # -- actions from the tray and notifications --------------------------------------------------

    def _on_running_billable(self, value: bool) -> None:
        current = self.state.snapshot.current
        if current is not None:
            self._act(lambda t: t.set_billable(current.id, value))

    def _menu_stop(self) -> None:
        current = self.state.snapshot.current
        if current is None:
            return
        self._act(lambda t: t.stop(), after=lambda _snapshot: self._confirm("stop", current))

    def _menu_resume(self) -> None:
        snapshot = self.state.snapshot
        if snapshot.current is not None or not snapshot.recent:
            return
        last = snapshot.recent[0]
        self._act(lambda t: t.resume(last), after=lambda s: s.current and self._confirm("start", s.current))

    def _confirm(self, kind: str, entry: Entry) -> None:
        note = action_confirmation(kind, entry, self._settings, self._now())
        if note is not None:
            self._notify(render(note, self.state.t))

    def on_notification(self, action: NotificationAction) -> None:
        # KDE leaves a notification on screen after a button click: take it away ourselves.
        self.dbus.submit(lambda: self._desktop.withdraw(action.notification_id), on_error=lambda _e: None)
        if action.action == "settings":
            self.open_settings()
        elif action.action == "stop":
            current = self.state.snapshot.current
            # Only the entry the reminder was about: it may have been stopped and another started.
            if current is not None and current.id == action.entry_id:
                self._act(lambda t: t.stop())

    def _notify(self, rendered: Any) -> None:
        self.dbus.submit(
            lambda: self._desktop.notify(rendered), on_error=lambda e: log.warning("Notify: %s", e)
        )

    # -- window, settings, links ---------------------------------------------------------------

    def show_popup(self) -> None:
        self.popup.show()
        self.popup.raise_()
        self.popup.activateWindow()
        self.popup.form.description.setFocus()

    def _on_popup_shown(self, shown: bool) -> None:
        if not shown:
            self._tick.stop()
            self._catalog_loaded = False  # projects and activities are read again on the next open
            return
        self._tick.start()
        if self._tracker is not None:
            self.refresh_full()
            self._load_catalog()

    def _remember_size(self, size: QSize) -> None:
        changes = {"popup_width": size.width(), "popup_height": size.height()}
        tracker = self._tracker
        if tracker is not None:
            self.kimai.submit(lambda: tracker.remember(**changes))
        else:
            self._memory = replace(self._memory, **changes)
            self._save_memory(self._memory)

    def open_kimai(self) -> None:
        if self._settings.url:
            locale = self._tracker.memory.kimai_locale if self._tracker else self._memory.kimai_locale
            QDesktopServices.openUrl(QUrl(all_entries_url(self._settings.url, locale)))

    def open_settings(self) -> SettingsDialog:
        if self.dialog is None:
            self.dialog = SettingsDialog(self.state.t)
            self.dialog.saveRequested.connect(self.save_settings)
            self.dialog.testRequested.connect(self._test_connection)
        self.dialog.load(self._settings, has_token=bool(self._token))
        self.dialog.set_secrets_problem(self.state.secrets_problem)
        self.popup.hide()
        self.dialog.show()
        self.dialog.raise_()
        self.dialog.activateWindow()
        return self.dialog

    def _test_connection(self, url: str, token: str) -> None:
        dialog, t = self.dialog, self.state.t
        token = token or self._token or ""

        def probe() -> str:
            client = self._client_factory(url, token)
            try:
                return client.me().display_name
            finally:
                _close(client)

        self.kimai.submit(
            probe,
            lambda name: dialog and dialog.show_status(t("optTestOk", user=name), ok=True),
            lambda error: dialog and dialog.show_status(t("optTestFail", err=describe(error, t)), ok=False),
        )

    def save_settings(self, settings: Settings, token: str | None) -> None:
        if self.dialog is not None:
            self.dialog.set_busy(True)
        url = settings.url

        def store() -> str | None:
            if token:
                self._desktop.set_token(url, token)
                return token
            return self._desktop.get_token(url)

        self.dbus.submit(store, lambda stored: self._settings_saved(settings, stored), self._settings_failed)

    def _settings_saved(self, settings: Settings, token: str | None) -> None:
        dialog, t = self.dialog, self.state.t
        if dialog is not None:
            dialog.set_busy(False)
        if not token:
            if dialog is not None:
                dialog.show_status(t("optTokenRequired"), ok=False)
            return
        previous = self._settings
        self._settings = settings.normalized()
        self._token = token
        self._save_settings(self._settings)
        if previous.language != self._settings.language:
            self.state.update(t=self._translator(self._settings.language))
            self.languageChanged.emit(self.state.t.language)
            if dialog is not None:
                dialog.retranslate(self.state.t)
        self.state.update(settings=self._settings, secrets_problem=None)
        if previous.autostart != self._settings.autostart:
            self._request_autostart(self._settings.autostart)
        if self._tracker is None:
            self._on_token(token)
        else:
            old, settings_now = self._client, self._settings
            self._client = client = self._client_factory(settings_now.url, token)
            self._catalog_loaded = False

            def switch(tracker: Tracker) -> Snapshot:
                snapshot = tracker.apply_settings(settings_now, client)
                if old is not client:
                    _close(old)
                return snapshot

            self._act(switch)
        self.state.update(configured=True)
        if dialog is not None:
            dialog.show_status(t("optSaved"), ok=True)

    def _settings_failed(self, error: Exception) -> None:
        if self.dialog is None:
            return
        self.dialog.set_busy(False)
        key = "secretsLocked" if isinstance(error, SecretsLocked) else "secretsUnavailable"
        self.dialog.show_status(self.state.t(key), ok=False)

    def _request_autostart(self, enabled: bool) -> None:
        reason = self.state.t("optAutostartReason")

        def denied(error: Exception) -> None:
            if isinstance(error, PortalError | TimeoutError):
                self._settings = replace(self._settings, autostart=False)
                self._save_settings(self._settings)
                if self.dialog is not None:
                    self.dialog.autostart.setChecked(False)
                    self.dialog.show_status(self.state.t("optAutostartDenied"), ok=False)
            else:
                log.warning("Autostart request failed: %s", error)

        self.dbus.submit(
            lambda: self._desktop.request_background(autostart=enabled, reason=reason), on_error=denied
        )

    # -- time ---------------------------------------------------------------------------

    def _on_tray_timer(self) -> None:
        if self.tray is not None:
            self.tray.render()
        wall, mono = time.time(), time.monotonic()
        jumped = abs((wall - self._last_wall) - (mono - self._last_mono)) > JUMP_SECONDS
        self._last_wall, self._last_mono = wall, mono
        today = self._now().astimezone().date()
        if jumped or today != self._day:
            self._day = today
            self.refresh_full()  # after sleep or midnight the totals and the day names change
        current = self.state.snapshot.current
        if current is not None:
            seconds = max(0, int((self._now() - current.begin).total_seconds()))
            message = self.state.t(
                "statusRunning", time=short_duration(seconds), project=current.project_name or ""
            )
            self.dbus.submit(lambda: self._desktop.set_status(message), on_error=lambda _e: None)

    @staticmethod
    def _translator(language: str) -> Translator:
        return Translator(resolve_language(language, system_locale()))


def _close(client: Any) -> None:
    close = getattr(client, "close", None)
    if close is not None:
        close()
