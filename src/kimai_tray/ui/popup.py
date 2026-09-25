"""The quick window (F-03): header with totals, the tracker bar, messages and recent entries.

It hides on Esc, on its close button and — as a popup — when it loses focus. A click on the
tray icon cannot close it: Plasma does not deliver that click while the window is open
(prototype 0004).
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime

from PySide6.QtCore import QEvent, QSize, Qt, QTimer, Signal
from PySide6.QtGui import QGuiApplication, QKeyEvent
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from kimai_tray.core.errors import describe
from kimai_tray.core.presentation import display_zone
from kimai_tray.core.timefmt import short_duration
from kimai_tray.core.tracker import live_totals, utc_now

from .form import TrackerForm
from .icons import app_icon, glyph
from .recent import RecentList
from .state import AppState
from .theme import palette_for, stylesheet

WIDTH = 460  # popup.css body width


class QuickWindow(QWidget):
    settingsRequested = Signal()
    openKimaiRequested = Signal()
    shownChanged = Signal(bool)

    def __init__(
        self, state: AppState, now: Callable[[], datetime] = utc_now, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.setObjectName("popup")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFixedWidth(WIDTH)
        self.hide_on_deactivate = True
        self.flash_delay_ms = 2000  # F-07: the green "saved" strip stays 2 s
        self._state = state
        self._now = now
        self._notice_shown: object = None

        header = QFrame(objectName="header")
        self.logo = QLabel()
        self.logo.setPixmap(app_icon().pixmap(18, 18))
        self.brand = QLabel(objectName="brand")
        self.today = QLabel(objectName="totals")
        self.week = QLabel(objectName="totals")
        self.settings_button = self._icon_button("gear")
        self.close_button = self._icon_button("close")
        top = QHBoxLayout(header)
        top.setContentsMargins(14, 8, 8, 8)
        top.setSpacing(8)
        top.addWidget(self.logo)
        top.addWidget(self.brand)
        top.addStretch(1)
        top.addWidget(self.today)
        top.addWidget(self.week)
        top.addWidget(self.settings_button)
        top.addWidget(self.close_button)

        self.unconfigured = QWidget()
        self.not_configured = QLabel(objectName="notConfigured")
        self.not_configured.setWordWrap(True)
        self.open_settings = QPushButton(objectName="primary")
        box = QVBoxLayout(self.unconfigured)
        box.setContentsMargins(14, 20, 14, 20)
        box.setSpacing(12)
        box.addWidget(self.not_configured)
        box.addWidget(self.open_settings)

        self.form = TrackerForm(state.t)
        self.warning = self._message("warning")
        self.error = self._message("error")
        self.saved = self._message("saved")
        self.recent = RecentList()
        self.all_entries = QPushButton(objectName="allEntries")
        self.all_entries.setCursor(Qt.CursorShape.PointingHandCursor)
        self.all_entries.setLayoutDirection(Qt.LayoutDirection.RightToLeft)  # icon after the text

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(header)
        layout.addWidget(self.unconfigured)
        layout.addWidget(self.form)
        for message in (self.warning, self.error, self.saved):
            layout.addWidget(message)
        layout.addWidget(self.recent)
        layout.addWidget(self.all_entries)

        self._flash_timer = QTimer(self, singleShot=True)
        self._flash_timer.timeout.connect(self.saved.hide)
        self.settings_button.clicked.connect(self.settingsRequested.emit)
        self.open_settings.clicked.connect(self.settingsRequested.emit)
        self.all_entries.clicked.connect(self.openKimaiRequested.emit)
        self.close_button.clicked.connect(self.hide)
        self.form.edited.connect(self.clear_error)
        state.changed.connect(self.render)
        QGuiApplication.styleHints().colorSchemeChanged.connect(lambda _scheme: self.apply_theme())
        self.apply_theme()
        self.render()

    # -- drawing -------------------------------------------------------------------

    def apply_theme(self) -> None:
        palette = palette_for(QGuiApplication.styleHints().colorScheme(), self.palette().window().color())
        self.setStyleSheet(stylesheet(palette))
        self.settings_button.setIcon(glyph("gear", palette["muted"], 17))
        self.close_button.setIcon(glyph("close", palette["muted"], 17))
        self.all_entries.setIcon(glyph("external", palette["accent"], 13))

    def render(self) -> None:
        state, t = self._state, self._state.t
        snapshot = state.snapshot
        now = self._now()
        tz = display_zone(snapshot, now.astimezone())
        self._texts(t)
        configured = state.configured
        self.unconfigured.setVisible(not configured)
        for part in (self.form, self.recent, self.all_entries):
            part.setVisible(configured)
        notes = [t(key, **params) for key, params in state.warnings]
        if state.secrets_problem:
            notes.append(t(state.secrets_problem))
        self.warning.setText("\n\n".join(notes))
        self.warning.setVisible(bool(notes))
        if configured:
            self.form.retranslate(t)
            self.form.render(snapshot, tz, now)
            self.recent.render(snapshot, tz, now, t)
            if snapshot.error is not None:
                self.show_error(describe(snapshot.error, t))
            if (
                snapshot.notice
                and snapshot.notice != self._notice_shown
                and not snapshot.notice.startswith("err")
            ):
                self.flash(t(snapshot.notice))
            elif snapshot.notice and snapshot.notice.startswith("err"):
                self.show_error(t(snapshot.notice))
        self._notice_shown = snapshot.notice
        self.tick()
        self.adjustSize()

    def tick(self) -> None:
        """Every second while the window is open: the clock and the live totals."""
        snapshot, t = self._state.snapshot, self._state.t
        now = self._now()
        self.form.tick(now)
        if snapshot.totals is None or not self._state.configured:
            self.today.hide()
            self.week.hide()
            return
        totals = live_totals(snapshot, now, display_zone(snapshot, now.astimezone()))
        self.today.setText(t("todayTotal", time=short_duration(totals.today)))
        self.week.setText(t("weekTotal", time=short_duration(totals.week)))
        self.today.show()
        self.week.show()

    def show_error(self, text: str) -> None:
        self.error.setText(text)
        self.error.setVisible(bool(text))

    def clear_error(self) -> None:
        self.show_error("")

    def flash(self, text: str) -> None:
        self.saved.setText(text)
        self.saved.show()
        self._flash_timer.start(self.flash_delay_ms)

    # -- window behaviour ------------------------------------------------------------

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802 - Qt API
        if event.key() == Qt.Key.Key_Escape:
            self.hide()
            return
        super().keyPressEvent(event)

    def event(self, event: QEvent) -> bool:
        if event.type() == QEvent.Type.WindowDeactivate and self.hide_on_deactivate:
            # A combo box list is a popup of our own: wait a moment and look again.
            QTimer.singleShot(150, self._hide_if_left)
        return super().event(event)

    def showEvent(self, event) -> None:  # noqa: N802 - Qt API
        super().showEvent(event)
        self.shownChanged.emit(True)

    def hideEvent(self, event) -> None:  # noqa: N802 - Qt API
        super().hideEvent(event)
        self.shownChanged.emit(False)

    def _hide_if_left(self) -> None:
        if self.isVisible() and not self.isActiveWindow() and QApplication.activePopupWidget() is None:
            self.hide()

    # -- helpers -----------------------------------------------------------------------

    def _texts(self, t: Callable[..., str]) -> None:
        self.brand.setText(t("appName"))
        self.setWindowTitle(t("appName"))
        self.not_configured.setText(t("notConfigured"))
        self.open_settings.setText(t("openSettings"))
        self.all_entries.setText(t("allEntries"))
        self.settings_button.setToolTip(t("settings"))
        self.close_button.setToolTip(t("winClose"))

    @staticmethod
    def _icon_button(name: str) -> QToolButton:
        button = QToolButton(objectName="iconButton")
        button.setIconSize(QSize(17, 17))
        return button

    @staticmethod
    def _message(name: str) -> QLabel:
        label = QLabel(objectName=name)
        label.setWordWrap(True)
        label.hide()
        return label
