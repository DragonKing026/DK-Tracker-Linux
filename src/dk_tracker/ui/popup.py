"""The quick window (F-03): header with totals, the tracker bar, messages and recent entries.

It hides on Esc, on its close button and — as a popup — when it loses focus; a tray click
toggles it (app.py guards against the click that itself took the focus away). Without a tray,
closing it quits the app. The user can resize it with the corner grip; the size is remembered.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from datetime import datetime

from PySide6.QtCore import QEvent, QPoint, QPointF, QRect, QSize, Qt, QTimer, Signal
from PySide6.QtGui import QGuiApplication, QKeyEvent, QMouseEvent, QPainter, QPen, QRegion
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from dk_tracker.core.errors import describe
from dk_tracker.core.presentation import display_zone
from dk_tracker.core.timefmt import short_duration
from dk_tracker.core.tracker import live_totals, utc_now

from .form import TrackerForm
from .icons import glyph, mark
from .recent import RecentList
from .state import AppState
from .theme import palette_for, stylesheet, write_assets

WIDTH, HEIGHT = 460, 600  # popup.css: 460 px wide, at most 600 px tall (the default size here)
MIN_WIDTH, MIN_HEIGHT = 400, 420
SCREEN_MARGIN = 12  # as the layer-shell margins from the screen edge


LOGO_SIZE = 24  # 18 px made the letters unreadable (0065)


class ResizeGrip(QWidget):
    """Top-left corner handle. The window is anchored bottom-right, so it grows up and left.

    A layer surface cannot be resized by the compositor, so the drag resizes the widget; a
    frameless toplevel asks the compositor to do it (startSystemResize).
    """

    SIZE = 14

    def __init__(self, window: QuickWindow) -> None:
        super().__init__(window)
        self._window = window
        self._start: tuple[QPoint, QSize] | None = None
        self.setFixedSize(self.SIZE, self.SIZE)
        self.setCursor(Qt.CursorShape.SizeFDiagCursor)

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802 - Qt API
        handle = self._window.windowHandle()
        edges = Qt.Edge.TopEdge | Qt.Edge.LeftEdge
        if self._window.placement_mode != "layer" and handle is not None and handle.startSystemResize(edges):
            return
        if self._window.placement_mode == "layer":
            self._start = (self.mapTo(self._window, event.position().toPoint()), self._window.panel_size())
        else:
            self._start = (event.globalPosition().toPoint(), self._window.size())

    def mouseMoveEvent(self, event: QMouseEvent) -> None:  # noqa: N802 - Qt API
        if self._start is None:
            return
        origin, size = self._start
        if self._window.placement_mode == "layer":
            # The layer surface never changes size (0066): only the panel inside it does, so the
            # pointer, in canvas coordinates, is exact however fast it moves.
            moved = origin - self.mapTo(self._window, event.position().toPoint())
            self._window.set_preferred_size(QSize(size.width() + moved.x(), size.height() + moved.y()))
            return
        moved = origin - event.globalPosition().toPoint()
        self._window.set_preferred_size(QSize(size.width() + moved.x(), size.height() + moved.y()))

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802 - Qt API
        if self._start is not None:
            self._start = None
            self._window.report_size()

    def paintEvent(self, event) -> None:  # noqa: N802 - Qt API
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(self.palette().placeholderText().color(), 1.4))
        for offset in (4, 8, 12):
            painter.drawLine(QPointF(offset, 2), QPointF(2, offset))
        painter.end()


class QuickWindow(QWidget):
    settingsRequested = Signal()
    openKimaiRequested = Signal()
    shownChanged = Signal(bool)
    closeRequested = Signal()  # ✕, Esc or the window frame while quit_on_close (no tray to come back from)
    sizeChosen = Signal(QSize)  # after the user resized the window with the grip

    def __init__(
        self, state: AppState, now: Callable[[], datetime] = utc_now, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.setObjectName("popup")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setMinimumSize(MIN_WIDTH, MIN_HEIGHT)
        self.resize(WIDTH, HEIGHT)
        self._preferred = QSize(WIDTH, HEIGHT)  # the user's size; used while there are lists to show
        self._canvas = False  # layer mode: a transparent surface holding the panel bottom-right (0066)
        self._panel = QSize(WIDTH, HEIGHT)  # the visible window inside the canvas
        self._compact: bool | None = None
        self._error_from_refresh = False  # the red strip came from a failed refresh, not from an action
        self.quit_on_close = False
        self.size_report_ms = 600  # a resize by the compositor is reported once it settles
        self._reported = QSize()
        self._size_timer = QTimer(self, singleShot=True)
        self._size_timer.timeout.connect(self.report_size)
        self.hide_on_deactivate = True
        self.placement_mode = "frameless"
        self.hidden_by_focus_loss_at = 0.0  # monotonic time; a tray click right after must not reopen
        self.flash_delay_ms = 2000  # F-07: the green "saved" strip stays 2 s
        self._state = state
        self._now = now
        self._notice_shown: object = None

        self.backdrop = QFrame(self, objectName="backdrop")  # the panel's background on the canvas
        self.backdrop.hide()
        self.header = header = QFrame(objectName="header")
        header.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)  # never stretches
        self.logo = QLabel()  # the WS mark, drawn in the theme's colours by apply_theme
        self.brand = QLabel(objectName="brand")
        self.today = QLabel(objectName="totals")
        self.week = QLabel(objectName="totals")
        self.settings_button = self._icon_button("gear")
        self.close_button = self._icon_button("close")
        self.grip = ResizeGrip(self)
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
        layout.addWidget(self.recent, 1)  # the list takes whatever height the user gives the window
        layout.addWidget(self.all_entries)

        self._flash_timer = QTimer(self, singleShot=True)
        self._flash_timer.timeout.connect(self.saved.hide)
        self.settings_button.clicked.connect(self.settingsRequested.emit)
        self.open_settings.clicked.connect(self.settingsRequested.emit)
        self.all_entries.clicked.connect(self.openKimaiRequested.emit)
        self.close_button.clicked.connect(self.dismiss)
        self.form.edited.connect(self.clear_error)
        state.changed.connect(self.render)
        QGuiApplication.styleHints().colorSchemeChanged.connect(lambda _scheme: self.apply_theme())
        self.apply_theme()
        self.render()

    # -- drawing -------------------------------------------------------------------

    def apply_theme(self) -> None:
        palette = palette_for(
            QGuiApplication.styleHints().colorScheme(),
            self.palette().window().color(),
            self._state.settings.theme,
        )
        css = stylesheet(palette, write_assets(palette))
        if self._canvas:  # only the panel is painted; the rest of the surface stays see-through
            css += f"#popup {{ background: transparent; }} QFrame#backdrop {{ background: {palette['bg']}; }}"
        self.setStyleSheet(css)
        self.logo.setPixmap(mark(palette["fg"], LOGO_SIZE))
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
        self._fit(compact=not configured)
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
                self._error_from_refresh = True
            elif self._error_from_refresh:
                self.clear_error()  # Kimai answers again; an action's own error is left alone
            # A notice belongs to the Snapshot an action produced: shown once for that Snapshot,
            # again only for a new one (a second save carries the same text in a new Snapshot).
            if snapshot.notice and snapshot is not self._notice_shown:
                if snapshot.notice.startswith("err"):
                    self.show_error(t(snapshot.notice, **dict(snapshot.notice_params)))
                else:
                    self.flash(t(snapshot.notice))
        self._notice_shown = snapshot
        self.tick()

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

    def set_preferred_size(self, size: QSize) -> None:
        screen = self.screen() or QGuiApplication.primaryScreen()
        if screen is not None:  # a size remembered on a bigger monitor must still fit this one
            area = screen.availableGeometry()
            size = size.boundedTo(QSize(area.width() - 2 * SCREEN_MARGIN, area.height() - 2 * SCREEN_MARGIN))
        self._preferred = size.expandedTo(QSize(MIN_WIDTH, MIN_HEIGHT))
        if self._compact:
            self._set_panel(QSize(self._preferred.width(), self.panel_size().height()))
        else:
            self._set_panel(self._preferred)

    def _fit(self, *, compact: bool) -> None:
        """Without lists (not configured) the window is as low as its content, as in the add-on."""
        if compact == self._compact:
            return
        self._compact = compact
        if compact:
            if not self._canvas:
                self.setMinimumHeight(0)
            self.layout().activate()
            height = self.layout().sizeHint().height() - self.layout().contentsMargins().top()
            self._set_panel(QSize(self._preferred.width(), height))
        else:
            if not self._canvas:
                self.setMinimumHeight(MIN_HEIGHT)
            self._set_panel(self._preferred)

    # -- the canvas (layer mode, 0066) ----------------------------------------------

    def set_placement(self, mode: str) -> None:
        """Layer mode keeps a transparent surface as big as allowed and moves only the panel inside
        it: a layer surface that changes size while the pointer drags it makes the pointer's
        position refer to a size the compositor has not shown yet, and the corner jumped."""
        self.placement_mode = mode
        self._canvas = mode == "layer"
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, self._canvas)
        self.backdrop.setVisible(self._canvas)
        if self._canvas:
            self.setMinimumSize(0, 0)
        else:
            self.clearMask()
            self.layout().setContentsMargins(0, 0, 0, 0)
            self.setMinimumSize(MIN_WIDTH, MIN_HEIGHT if not self._compact else 0)
        self.apply_theme()
        # The window may already be low (made while unconfigured): size the panel for that again.
        compact, self._compact = self._compact, None
        if compact is None:
            self._set_panel(self._preferred)
        else:
            self._fit(compact=compact)

    def panel_size(self) -> QSize:
        return QSize(self._panel) if self._canvas else self.size()

    def panel_rect(self) -> QRect:
        if not self._canvas:
            return self.rect()
        return QRect(
            self.width() - self._panel.width(),
            self.height() - self._panel.height(),
            self._panel.width(),
            self._panel.height(),
        )

    def _canvas_size(self) -> QSize:
        screen = self.screen() or QGuiApplication.primaryScreen()
        if screen is None:
            return self._panel
        area = screen.availableGeometry()
        return QSize(area.width() - 2 * SCREEN_MARGIN, area.height() - 2 * SCREEN_MARGIN)

    def _set_panel(self, size: QSize) -> None:
        if not self._canvas:
            self.resize(size)
            return
        self._panel = QSize(size)
        canvas = self._canvas_size()
        if self.size() != canvas:
            self.resize(canvas)  # once; the resize event places the panel
        else:
            self._place_panel()
        if self.isVisible() and not self._compact:
            self._size_timer.start(self.size_report_ms)

    def _place_panel(self) -> None:
        rect = self.panel_rect()
        self.layout().setContentsMargins(rect.left(), rect.top(), 0, 0)
        self.backdrop.setGeometry(rect)
        self.backdrop.lower()
        self.setMask(QRegion(rect))  # input region: beside the panel, clicks reach the desktop
        self.grip.move(rect.topLeft() + QPoint(1, 1))
        self.grip.raise_()

    def dismiss(self) -> None:
        """Close as the user asked: hide to the tray, or — with no tray to come back from — quit."""
        if self.quit_on_close:
            self.closeRequested.emit()
        else:
            self.hide()

    def closeEvent(self, event) -> None:  # noqa: N802 - Qt API
        super().closeEvent(event)
        if self.quit_on_close:
            self.closeRequested.emit()

    def report_size(self) -> None:
        size = self.panel_size()
        if not self._compact and self.isVisible() and size != self._reported:
            self._reported = size
            self.sizeChosen.emit(size)

    def resizeEvent(self, event) -> None:  # noqa: N802 - Qt API
        super().resizeEvent(event)
        if self._canvas:
            self._place_panel()
            return
        if self.isVisible() and not self._compact:
            self._size_timer.start(self.size_report_ms)
        self.grip.move(1, 1)
        self.grip.raise_()

    def show_search_results(self, term: str, entries: tuple) -> None:
        """F-33: results for `term`, drawn in the same zone as the recent list."""
        now = self._now()
        self.recent.show_results(term, entries, display_zone(self._state.snapshot, now.astimezone()), now)

    def show_error(self, text: str) -> None:
        self._error_from_refresh = False
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
            self.dismiss()
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
            self.hide_after_focus_loss()

    def hide_after_focus_loss(self) -> None:
        self.hidden_by_focus_loss_at = time.monotonic()
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
