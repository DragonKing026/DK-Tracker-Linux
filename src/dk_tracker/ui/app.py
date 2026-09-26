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
from datetime import datetime, timedelta
from typing import Any

from PySide6.QtCore import QObject, QSize, QTimer, QUrl, Signal
from PySide6.QtGui import QDesktopServices, QGuiApplication

from dk_tracker.core.entry_list import build_rows, first_day_of_week
from dk_tracker.core.errors import TrackerError, describe
from dk_tracker.core.i18n import Translator, resolve_language, system_locale
from dk_tracker.core.models import Entry
from dk_tracker.core.notification_policy import (
    PolicyState,
    action_confirmation,
    evaluate,
    is_ours,
    render,
)
from dk_tracker.core.presentation import display_zone
from dk_tracker.core.settings import Memory, Settings
from dk_tracker.core.timefmt import local_day, short_duration, weekday_index
from dk_tracker.core.tracker import SEARCH_MIN_CHARS, Snapshot, Tracker, all_entries_url, utc_now
from dk_tracker.desktop.bus import PortalError
from dk_tracker.desktop.notifications import NotificationAction
from dk_tracker.desktop.secrets import SecretsLocked, SecretsUnavailable

from . import placement
from .desktop_bridge import ClickListener
from .main_window.bridge import MainBridge
from .main_window.window import MainWindow
from .popup import QuickWindow
from .settings_dialog import SettingsDialog
from .state import AppState
from .theme import palette_for
from .tray import Tray
from .worker import Worker

log = logging.getLogger(__name__)
POLL_MS = 60_000  # F-02: GET /api/timesheets/active once a minute
TICK_MS = 1_000  # the clock, only while the window is open
TRAY_MS = 15_000  # tray label and clock-jump check
REOPEN_GUARD_SECONDS = 0.4
SHUTDOWN_SECONDS = 5.0
JUMP_SECONDS = 120  # wall clock moved more than monotonic time: sleep or a clock change
EMPTY_WEEKS_LIMIT = 8  # the main list stops loading older weeks after this many empty ones in a row
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
        self._opening = 0  # counts window openings; a catalog answer counts only for its own opening
        self._status_sent: str | None = None  # last background status sent: "running" | "idle"
        self._last_wall = time.time()
        self._last_mono = time.monotonic()
        self._day = now().astimezone().date()

        self.state = AppState(self._settings, self._translator(self._settings.language))
        self.kimai = Worker("kimai", self)
        self.dbus = Worker("desktop", self)
        self.popup = QuickWindow(self.state, now)
        self.mode = placement.apply(self.popup, window_mode)
        self.popup.set_preferred_size(QSize(memory.popup_width, memory.popup_height))
        self._tray_available = tray_available
        self.tray = Tray(self.state, now) if tray_available and self._settings.show_tray else None
        # Without a tray the window is the whole app: closing it must not leave a hidden process.
        self.popup.quit_on_close = self.tray is None
        self.dialog: SettingsDialog | None = None
        self.listener = ClickListener() if listen_for_clicks else None
        # Plan 5: the main window, made on first use (QML takes a moment to load).
        self.main_bridge = MainBridge(self)
        self.main_window: MainWindow | None = None
        self._weeks = 1  # weeks the main list shows, this one included
        self._listed = 0  # entries in the main list after the last load
        self._growing = False  # the last load asked for one more week
        self._empty_weeks = 0
        self._main_term = ""  # the main list's search; "" = the weeks

        self._poll = QTimer(self, interval=POLL_MS, timeout=self._on_poll)
        self._tick = QTimer(self, interval=TICK_MS, timeout=self._on_tick)
        self._tray_timer = QTimer(self, interval=TRAY_MS, timeout=self._on_tray_timer)
        self._connect()

    # -- lifecycle -------------------------------------------------------------------

    def start(self, *, hidden: bool) -> None:
        if self.tray is not None:
            self.tray.show()
        if self._tray_hint:
            self.state.update(warnings=[("hintNoTray", {})])  # before any configuration, too
        if self.listener is not None:
            self.listener.clicked.connect(self.on_notification)
            self.listener.start()
        self._poll.start()
        self._tray_timer.start()
        self._load_token(self._settings.url)
        if not hidden or self.tray is None:
            self.show_main_window()

    def shutdown(self) -> None:
        for timer in (self._poll, self._tick, self._tray_timer):
            timer.stop()
        if self.listener is not None:
            self.listener.stop()
            self.listener.wait(2000)
        self.main_bridge.flush_deletes()  # a delete still in its undo time reaches Kimai
        self.popup.hide()  # first: leaving the description field saves what was typed
        if self.main_window is not None:
            self.main_window.dispose()
            self.main_window = None
        if self.tray is not None:
            self.tray.icon.hide()
        # Queued actions still reach Kimai; a hung request does not hold the exit for long.
        if not self.kimai.finish(timeout=SHUTDOWN_SECONDS):
            log.warning("Kimai did not answer the last actions before quitting")
        self.dbus.submit(self._desktop.close)
        self.dbus.finish(timeout=SHUTDOWN_SECONDS)

    @property
    def catalog_loaded(self) -> bool:
        return self._catalog_loaded

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
        form.workChanged.connect(self._change_work)
        recent.resumeRequested.connect(lambda entry: self._act(lambda t: t.resume(entry)))
        recent.billableRequested.connect(
            lambda entry_id, value: self._act(
                lambda t: t.set_billable(entry_id, value), after=lambda _snapshot: self._search_again()
            )
        )
        recent.searchRequested.connect(self._search)
        popup.settingsRequested.connect(self.open_settings)
        popup.openKimaiRequested.connect(self.show_main_window)  # Plan 5: the main window, not the browser
        popup.shownChanged.connect(self._on_popup_shown)
        popup.sizeChosen.connect(self._remember_size)
        popup.closeRequested.connect(self.quitRequested.emit)
        if self.tray is not None:
            self._connect_tray(self.tray)
        self.state.changed.connect(self._render_main)
        main = self.main_bridge
        main.startRequested.connect(lambda payload: self._act_main(lambda t: t.start(**payload)))
        main.stopRequested.connect(lambda: self._act_main(lambda t: t.stop()))
        main.addRequested.connect(lambda payload: self._act_main(lambda t: t.add_entry(**payload)))
        main.editRequested.connect(self._edit_entry)
        main.deleteRequested.connect(self._delete_entry)
        main.resumeRequested.connect(self._resume_entry)
        main.runningEdited.connect(self._edit_running)
        main.loadMoreRequested.connect(self._load_more)
        main.searchRequested.connect(self._main_search)
        main.activitiesRequested.connect(self._main_activities)
        main.rowActivitiesRequested.connect(
            lambda project_id: self._main_activities(project_id, deliver=self.main_bridge.set_row_activities)
        )
        main.settingsRequested.connect(self.open_settings)

    def _connect_tray(self, tray: Tray) -> None:
        tray.openRequested.connect(self.toggle_popup)
        tray.openMainRequested.connect(self.show_main_window)
        tray.stopRequested.connect(self._menu_stop)
        tray.resumeLastRequested.connect(self._menu_resume)
        tray.openKimaiRequested.connect(self.open_kimai)
        tray.settingsRequested.connect(self.open_settings)
        tray.quitRequested.connect(self.quitRequested.emit)

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
        if self._main_visible():  # opened at start, before the wallet answered
            self._main_catalog()
            self._reload_entries()

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

        opening = self._opening

        def done(result: tuple[Snapshot, list]) -> None:
            if opening == self._opening and self.popup.isVisible():
                self._catalog_loaded = True
            self._apply(result)
            self.popup.form.set_catalog(result[0], tracker.default_work()[0])
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
            lambda items: self._apply_activities(project_id, items),
            self._on_error,
            key=f"activities-{project_id}",
        )

    def _apply_activities(self, project_id: int | None, items: list) -> None:
        # Answers can arrive for a project the user has already left: only the chosen one counts.
        if project_id != self.popup.form.project.currentData() or self._tracker is None:
            return
        self.popup.form.set_activities(items, self._tracker.default_work()[1])

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

    def _change_work(self, project_id: int, activity_id: int) -> None:
        """F-34. A refusal puts the pickers back to what Kimai still has."""
        tracker = self._tracker
        if tracker is None:
            return

        def refused(error: Exception) -> None:
            self.popup.form.reset_work()
            self._on_error(error)

        self.popup.clear_error()
        self.kimai.submit(
            lambda: (tracker.change_work(project_id, activity_id), tracker.warnings()), self._apply, refused
        )

    def _search(self, term: str) -> None:
        """F-33. Answers for an older term are dropped by the list itself."""
        tracker = self._tracker
        if tracker is None:
            return
        self.popup.clear_error()
        self.kimai.submit(
            lambda: tracker.search(term),
            lambda entries: self.popup.show_search_results(term, entries),
            self._on_error,
        )

    def _search_again(self) -> None:
        # A `$` on a result changes that entry; the results are Kimai's answer, so ask again.
        recent = self.popup.recent
        if recent.searching:
            self._search(recent.term)

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
        if not is_ours(action.notification_id):
            return  # another app's notification: the portal tells every listener
        # KDE leaves a notification on screen after a button click: take it away ourselves.
        self.dbus.submit(lambda: self._desktop.withdraw(action.notification_id), on_error=lambda _e: None)
        if action.action == "open":
            self.show_main_window()
        elif action.action == "settings":
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

    def toggle_popup(self) -> None:
        """Tray click: close an open window, open a closed one — unless that very click just
        closed it by taking the focus (the panel gets the press before the icon's Activate)."""
        if self.popup.isVisible():
            self.popup.hide()
        elif time.monotonic() - self.popup.hidden_by_focus_loss_at > REOPEN_GUARD_SECONDS:
            self.show_popup()

    def show_popup(self) -> None:
        self.popup.show()
        self.popup.raise_()
        self.popup.activateWindow()
        self.popup.form.description.setFocus()

    def _on_popup_shown(self, shown: bool) -> None:
        if not shown:
            if not self._main_visible():
                self._tick.stop()
            self._catalog_loaded = False  # projects and activities are read again on the next open
            self._opening += 1
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
        # A wallet that was locked or unreachable at start may hold the token: an empty field
        # then means "take it from the wallet" (saving looks it up) rather than "type it again".
        in_wallet = bool(self._token) or (self.state.secrets_problem is not None and bool(self._settings.url))
        self.dialog.load(self._settings, has_token=in_wallet)
        self.dialog.set_secrets_problem(self.state.secrets_problem)
        self.popup.hide()
        self.dialog.show()
        self.dialog.raise_()
        self.dialog.activateWindow()
        return self.dialog

    def _test_connection(self, url: str, token: str) -> None:
        dialog, t = self.dialog, self.state.t
        if not token:
            # The stored token belongs to the saved address only — never send it anywhere else.
            if url.strip().rstrip("/") != self._settings.url or not self._token:
                if dialog is not None:
                    dialog.show_status(t("optTokenRequired"), ok=False)
                return
            token = self._token

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
        if previous.show_tray != self._settings.show_tray:
            self._set_tray(self._settings.show_tray)
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

    # -- the main window (Plan 5) ---------------------------------------------------------

    def show_main_window(self) -> None:
        if self.main_window is None:
            self.main_window = MainWindow(self.main_bridge, parent=self.main_bridge)  # the engine goes first
            self.main_window.closed.connect(self._on_main_closed)
            self._main_theme()
            QGuiApplication.styleHints().colorSchemeChanged.connect(lambda _scheme: self._main_theme())
        memory = self._tracker.memory if self._tracker is not None else self._memory
        self.popup.hide()
        self._render_main()
        self.main_window.show(QSize(memory.main_width, memory.main_height))
        self._tick.start()
        if self._tracker is not None:
            self._main_catalog()
            self._reload_entries()

    def _main_visible(self) -> bool:
        return self.main_window is not None and self.main_window.isVisible()

    def _main_theme(self) -> None:
        hints, window = QGuiApplication.styleHints(), QGuiApplication.palette().window().color()
        self.main_bridge.set_palette(palette_for(hints.colorScheme(), window))

    def _render_main(self) -> None:
        if self.main_window is None:
            return
        snapshot, now = self.state.snapshot, self._now()
        tz = display_zone(snapshot, now.astimezone())
        self.main_bridge.render(snapshot, configured=self.state.configured, t=self.state.t, now=now, tz=tz)

    def _on_main_closed(self) -> None:
        size = self.main_window.size() if self.main_window is not None else QSize()
        self._remember(main_width=size.width(), main_height=size.height())
        if self.tray is None:
            self.quitRequested.emit()  # no tray: the main window is the whole app
        elif not self.popup.isVisible():
            self._tick.stop()

    def _set_tray(self, shown: bool) -> None:
        if shown and self.tray is None and self._tray_available:
            self.tray = Tray(self.state, self._now)
            self._connect_tray(self.tray)
            self.tray.show()
        elif not shown and self.tray is not None:
            self.tray.icon.hide()
            self.tray.deleteLater()
            self.tray = None
            self.popup.hide()
            self.show_main_window()  # otherwise nothing of the app would be left on screen
        self.popup.quit_on_close = self.tray is None

    def _main_catalog(self) -> None:
        tracker = self._tracker
        if tracker is None:
            return

        def done(result: tuple[Snapshot, list]) -> None:
            self._apply(result)
            self.main_bridge.set_projects(list(result[0].projects))

        self.kimai.submit(
            lambda: (tracker.load_catalog(), tracker.warnings()), done, self._main_failed, key="main-catalog"
        )

    def _main_activities(self, project_id: int, deliver: Callable[[list], None] | None = None) -> None:
        tracker = self._tracker
        if tracker is None or not project_id:
            return
        deliver = deliver or self.main_bridge.set_activities
        self.kimai.submit(
            lambda: tracker.activities(project_id), deliver, self._main_failed,
            key=f"main-activities-{deliver.__name__}-{project_id}",
        )  # fmt: skip

    def _reload_entries(self) -> None:
        tracker = self._tracker
        if tracker is None or not self._main_visible():
            return
        if self._main_term:
            self._main_search(self._main_term)
            return
        snapshot, now = self.state.snapshot, self._now()
        tz = display_zone(snapshot, now.astimezone())
        first_weekday = weekday_index(snapshot.user.first_weekday) if snapshot.user else 0
        today = local_day(now, tz)
        first = first_day_of_week(today, first_weekday) - timedelta(days=7 * (self._weeks - 1))
        t = self.state.t

        def done(entries: tuple) -> None:
            grew, growing = len(entries) > self._listed, self._growing
            if growing:
                self._empty_weeks = 0 if grew else self._empty_weeks + 1
                self._growing = False
            self._listed = len(entries)
            self.main_bridge.set_loading(False)
            self.main_bridge.set_entries(build_rows(entries, tz, today, first_weekday, t), tz)
            if (growing and not grew) or (self._weeks == 1 and not entries):
                # An empty week adds no rows, so the list cannot ask for more: keep going
                # until an entry turns up or EMPTY_WEEKS_LIMIT empty weeks in a row.
                self._load_more()

        self.main_bridge.set_loading(True)
        self.kimai.submit(lambda: tracker.entries(first, today), done, self._main_failed, key="main-entries")

    def _load_more(self) -> None:
        if self._main_term or self._empty_weeks >= EMPTY_WEEKS_LIMIT or self.kimai_pending("main-entries"):
            return
        self._weeks += 1
        self._growing = True
        self._reload_entries()

    def kimai_pending(self, key: str) -> bool:
        return self.kimai.pending(key)

    def _main_search(self, term: str) -> None:
        term = " ".join(term.split())
        tracker = self._tracker
        if len(term) < SEARCH_MIN_CHARS or tracker is None:
            if self._main_term:
                self._main_term = ""
                self._reload_entries()
            return
        self._main_term = term
        snapshot, now = self.state.snapshot, self._now()
        tz = display_zone(snapshot, now.astimezone())
        first_weekday = weekday_index(snapshot.user.first_weekday) if snapshot.user else 0
        today, t = local_day(now, tz), self.state.t

        def done(found: tuple) -> None:
            if term == self._main_term:  # typing went on: an older answer is dropped
                self.main_bridge.set_entries(build_rows(found, tz, today, first_weekday, t), tz)

        self.kimai.submit(lambda: tracker.search(term), done, self._main_failed)

    def _act_main(
        self,
        job: Callable[[Tracker], Snapshot],
        *,
        entry_id: int | None = None,
        on_error: Callable[[], None] | None = None,
    ) -> None:
        """An action from the main window: its error goes to the window (or under the row)."""
        tracker = self._tracker
        if tracker is None:
            return
        self.main_bridge.show_error("")

        def done(result: tuple[Snapshot, list]) -> None:
            self._apply(result)
            self._reload_entries()

        def failed(error: Exception) -> None:
            text = describe(error, self.state.t)
            if entry_id is not None:
                self.main_bridge.show_row_error(entry_id, text)
            else:
                self.main_bridge.show_error(text)
            if on_error is not None:
                on_error()
            level = logging.INFO if isinstance(error, TrackerError) else logging.WARNING
            log.log(level, "Main window action failed: %s", describe(error, _ENGLISH))
            self.state.update(snapshot=tracker.snapshot)
            self._reload_entries()  # the row shows again what Kimai has

        self.kimai.submit(lambda: (job(tracker), tracker.warnings()), done, failed)

    def _main_failed(self, error: Exception) -> None:
        """A background load (list, projects, activities); the next one that works clears it."""
        self.main_bridge.set_loading(False)
        self.main_bridge.show_load_error(describe(error, self.state.t))

    def _edit_entry(self, entry_id: int, changes: dict) -> None:
        entry = self.main_bridge.entries.entry(entry_id)
        if entry is not None:
            self._act_main(lambda t: t.edit_entry(entry, **changes), entry_id=entry_id)

    def _delete_entry(self, entry_id: int) -> None:
        entry = self.main_bridge.deleted_entry(entry_id) or self.main_bridge.entries.entry(entry_id)
        if entry is not None:
            # The row is hidden: an error goes to the bar, and the row comes back (spec, section 9).
            self._act_main(
                lambda t: t.delete_entry(entry),
                on_error=lambda: self.main_bridge.entries.show_entry(entry_id),
            )

    def _resume_entry(self, entry_id: int) -> None:
        entry = self.main_bridge.entries.entry(entry_id)
        if entry is not None:
            self._act_main(lambda t: t.resume(entry))

    def _edit_running(self, changes: dict) -> None:
        current = self.state.snapshot.current
        if "description" in changes:
            text = changes["description"]
            self._act_main(lambda t: t.update_description(text) or t.snapshot)
        elif "project_id" in changes:
            self._act_main(lambda t: t.change_work(changes["project_id"], changes["activity_id"]))
        elif "begin" in changes:
            self._act_main(lambda t: t.update_begin(changes["begin"]))
        elif "billable" in changes and current is not None:
            self._act_main(lambda t: t.set_billable(current.id, changes["billable"]))

    def _remember(self, **changes: Any) -> None:
        tracker = self._tracker
        if tracker is not None:
            self.kimai.submit(lambda: tracker.remember(**changes))
        else:
            self._memory = replace(self._memory, **changes)
            self._save_memory(self._memory)

    def _on_poll(self) -> None:
        self.refresh_active()
        if self._main_visible():
            self._reload_entries()  # changes made elsewhere (the browser) show up within a minute

    def _on_tick(self) -> None:
        if self.popup.isVisible():
            self.popup.tick()
        if self._main_visible():
            self._render_main()

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
        elif self._status_sent not in (None, "idle"):
            message = self.state.t("tooltipIdle")  # once after a stop, so no old time stays shown
        else:
            return
        self._status_sent = "running" if current is not None else "idle"
        self.dbus.submit(lambda: self._desktop.set_status(message), on_error=lambda _e: None)

    @staticmethod
    def _translator(language: str) -> Translator:
        return Translator(resolve_language(language, system_locale()))


def _close(client: Any) -> None:
    close = getattr(client, "close", None)
    if close is not None:
        close()
