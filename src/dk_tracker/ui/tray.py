"""The tray icon (F-02) and its context menu (F-20).

Left click opens or closes the window. The middle button does nothing on purpose — the user chose
that nothing should start or stop without the window or the menu. The menu is drawn by the
tray host from dbusmenu, so it always appears next to the icon.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from datetime import datetime

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QSystemTrayIcon

from dk_tracker.core.presentation import TrayStatus, tray_status
from dk_tracker.core.tracker import utc_now

from .icons import tray_icon
from .state import AppState

log = logging.getLogger(__name__)


class Tray(QObject):
    openRequested = Signal()
    openMainRequested = Signal()  # Plan 5: the main window
    stopRequested = Signal()
    resumeLastRequested = Signal()
    openKimaiRequested = Signal()
    settingsRequested = Signal()
    quitRequested = Signal()

    def __init__(
        self, state: AppState, now: Callable[[], datetime] = utc_now, parent: QObject | None = None
    ) -> None:
        super().__init__(parent)
        self._state = state
        self._now = now
        self.drawn = 0  # how many times the icon was painted (redraws cost the tray host a D-Bus update)
        self._painted: tuple[str, str] | None = None
        self.status = TrayStatus("unconfigured", "", "")

        self.menu = QMenu()
        self.stop_action = self._action(self.stopRequested)
        self.resume_action = self._action(self.resumeLastRequested)
        self.menu.addSeparator()
        self.open_main_action = self._action(self.openMainRequested)
        self.open_action = self._action(self.openRequested)
        self.open_kimai_action = self._action(self.openKimaiRequested)
        self.settings_action = self._action(self.settingsRequested)
        self.menu.addSeparator()
        self.quit_action = self._action(self.quitRequested)

        self.icon = QSystemTrayIcon(self)
        self.icon.setContextMenu(self.menu)
        self.icon.activated.connect(self._on_activated)
        state.changed.connect(self.render)
        self.render()

    @staticmethod
    def available() -> bool:
        return QSystemTrayIcon.isSystemTrayAvailable()

    def show(self) -> None:
        self.icon.show()

    def render(self) -> None:
        state, t = self._state, self._state.t
        snapshot = state.snapshot
        self.status = tray_status(snapshot, state.configured, self._now(), t)
        if self._painted != (self.status.kind, self.status.label):
            self._painted = (self.status.kind, self.status.label)
            self.icon.setIcon(tray_icon(self.status.kind, self.status.label))
            self.drawn += 1
        self.icon.setToolTip(self.status.tooltip)

        self.stop_action.setText(t("menuStop"))
        self.resume_action.setText(t("menuResumeLast"))
        self.open_main_action.setText(t("menuOpenMain"))
        self.open_action.setText(t("menuOpen"))
        self.open_kimai_action.setText(t("menuOpenKimai"))
        self.settings_action.setText(t("settings"))
        self.quit_action.setText(t("menuQuit"))
        self.stop_action.setEnabled(state.configured and snapshot.current is not None)
        self.resume_action.setEnabled(state.configured and snapshot.current is None and bool(snapshot.recent))
        self.open_kimai_action.setEnabled(state.configured)

    def _action(self, signal: Signal) -> QAction:
        action = QAction(self.menu)
        action.triggered.connect(lambda _checked=False: signal.emit())
        self.menu.addAction(action)
        return action

    def _on_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        log.info("Tray icon activated: %s", reason.name)  # which clicks the tray host delivers
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.openRequested.emit()
