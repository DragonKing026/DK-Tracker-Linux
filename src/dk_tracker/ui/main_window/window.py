"""The main window's QML engine: `app` in the context, icons from our glyphs, the Basic style
(our palette, the same look on KDE and GNOME), and what closing means (Plan 5, spec section 7)."""

from __future__ import annotations

import logging
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QEvent, QObject, QSize, QUrl, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickImageProvider
from PySide6.QtQuickControls2 import QQuickStyle

from ..icons import glyph, mark
from .bridge import MainBridge

QML_DIR = Path(__file__).with_name("qml")
WHEEL_LOG_LIMIT = 5  # the first wheel events of a run go to the log: what the desktop sends (0079)

log = logging.getLogger(__name__)


class _Icons(QQuickImageProvider):
    """image://glyph/<name>/<rrggbb> and image://icons/mark/<rrggbb> — the icons the popup uses too."""

    def __init__(self, bridge: MainBridge) -> None:
        super().__init__(QQuickImageProvider.ImageType.Pixmap)
        self._bridge = bridge

    def requestPixmap(self, id: str, size: QSize, requested: QSize) -> QPixmap:  # noqa: A002, N802
        side = max(requested.width(), requested.height(), 16)
        name, _, color = id.partition("/")
        if name == "mark":  # the colour is in the address: a theme change must not reuse a cached one
            return mark(f"#{color}" if color else self._bridge.palette.get("fg", "#eceef2"), side)
        return glyph(name, f"#{color or 'eceef2'}", side).pixmap(side, side)


class MainWindow(QObject):
    """Created on first use; closing hides it (the controller then decides whether to quit)."""

    closed = Signal()

    def __init__(self, bridge: MainBridge, parent: QObject | None = None) -> None:
        super().__init__(parent)
        # Always Basic: on KDE the platform theme picks org.kde.desktop first, which ignores the
        # window's palette — white fields with dark text on our dark window (live test 0.10.0).
        if QQuickStyle.name() != "Basic":
            QQuickStyle.setStyle("Basic")
        self.bridge = bridge
        self.engine = QQmlApplicationEngine(self)
        self.engine.addImageProvider("glyph", _Icons(bridge))
        self.engine.addImageProvider("icons", _Icons(bridge))
        self.engine.rootContext().setContextProperty("app", bridge)
        self.engine.load(QUrl.fromLocalFile(str(QML_DIR / "Main.qml")))
        roots = self.engine.rootObjects()
        if not roots:
            raise RuntimeError("the main window's QML did not load (see the log)")
        self.window = roots[0]
        self._wheels_logged = 0
        self.window.installEventFilter(self)
        bridge.windowClosed.connect(self.closed.emit)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:  # noqa: N802
        """Only looks: the calendar zooms with the wheel, and a real mouse on KDE sent it nothing once."""
        if event.type() == QEvent.Type.Wheel and self._wheels_logged < WHEEL_LOG_LIMIT:
            self._wheels_logged += 1
            device = event.pointingDevice()
            log.info(
                "Wheel: angle %s, pixels %s, phase %s, device %s (%s)",
                event.angleDelta().toTuple(), event.pixelDelta().toTuple(), event.phase().name,
                device.name() if device else "?", device.type().name if device else "?",
            )  # fmt: skip
        return False

    def show(self, size: QSize | None = None) -> None:
        # An open window is only raised: QWindow.show() is showNormal() on a desktop, so it
        # un-maximized the window when "Settings" was clicked (live test of 0.10.0).
        if not self.window.isVisible():
            if size is not None:
                self.window.resize(size)
            self.window.show()
        self.window.raise_()
        self.window.requestActivate()

    def hide(self) -> None:
        self.window.hide()

    def isVisible(self) -> bool:  # noqa: N802 - as QWidget, for the controller
        return bool(self.window.isVisible())

    def size(self) -> QSize:
        return self.window.size()

    def dispose(self) -> None:
        """At exit: the QML goes before `app` does, or its bindings would read a deleted object."""
        self.window.hide()
        self.window.deleteLater()
        self.engine.deleteLater()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)

    def child(self, name: str) -> QObject | None:
        """A QML object by its objectName (tests, and the controller's focus handling)."""
        return self.window.findChild(QObject, name)
