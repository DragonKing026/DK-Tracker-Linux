"""Throwaway spike for task 0004: tray icon + frameless quick window on Wayland/X11.

Logs (JSON lines, stdout) everything the questions of 0004 need: tray availability,
platform, activation reasons, window geometry after show, and the timing between
"window hid on focus loss" and "tray icon activated" (the click-on-icon collision).

    python3 tray_demo.py [--mode tool|popup|normal] [--guard-ms 0] [--width 460 --height 560]

Not product code: nothing here is imported by the app.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

from PySide6.QtCore import QEvent, QPoint, Qt, QTimer
from PySide6.QtGui import QAction, QColor, QGuiApplication, QIcon, QPainter, QPixmap
from PySide6.QtWidgets import (
    QApplication, QLabel, QLineEdit, QMenu, QPushButton, QSystemTrayIcon, QVBoxLayout, QWidget,
)

START = time.monotonic()


def log(event: str, **data: object) -> None:
    print(json.dumps({"t": round(time.monotonic() - START, 3), "event": event, **data}), flush=True)


def dot_icon(color: str) -> QIcon:
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QColor(color))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(4, 4, 56, 56)
    painter.end()
    return QIcon(pixmap)


class QuickWindow(QWidget):
    def __init__(self, mode: str, size: tuple[int, int]) -> None:
        flags = {
            "tool": Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint,
            "popup": Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint,
            "normal": Qt.WindowType.Window,
        }[mode]
        super().__init__(None, flags)
        self.setWindowTitle("Kimai Tray — prototyp")
        self.resize(*size)
        self.last_hidden_at: float | None = None
        layout = QVBoxLayout(self)
        self.label = QLabel("Prototyp okna szybkiej obsługi\n(tryb: %s)" % mode)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        self.description = QLineEdit()
        self.description.setPlaceholderText("Co robisz? (sprawdź, czy da się pisać)")
        self.description.textEdited.connect(lambda text: log("input.typed", length=len(text)))
        layout.addWidget(self.description)
        close = QPushButton("Zamknij okno")
        close.clicked.connect(self.hide)
        layout.addWidget(close)
        self.setStyleSheet("QWidget { background: #ffffff; color: #111827; } QLabel { font-size: 16px; }"
                           " QLineEdit { border: 1px solid #9ca3af; padding: 6px; font-size: 14px; }")

    def event(self, event: QEvent) -> bool:
        if event.type() == QEvent.Type.WindowDeactivate and self.isVisible():
            log("window.deactivated_hide")
            self.last_hidden_at = time.monotonic()
            self.hide()
        return super().event(event)

    def showEvent(self, event) -> None:  # noqa: N802 - Qt API
        super().showEvent(event)
        QTimer.singleShot(300, self.report_geometry)

    def report_geometry(self) -> None:
        handle = self.windowHandle()
        log(
            "window.geometry",
            geometry=[self.x(), self.y(), self.width(), self.height()],
            frame=[self.frameGeometry().x(), self.frameGeometry().y()],
            screen=self.screen().name() if self.screen() else None,
            screen_geometry=list(self.screen().geometry().getRect()) if self.screen() else None,
            active=self.isActiveWindow(),
            handle_position=[handle.x(), handle.y()] if handle else None,
        )


def anchor_bottom_right(window: QWidget) -> None:
    """Configure LayerShellQt::Window for the widget's QWindow via ctypes (no Python bindings exist)."""
    import ctypes

    import shiboken6
    from PySide6.QtCore import QMargins, QObject

    window.winId()  # create the QWindow before it is shown
    lib = ctypes.CDLL("libLayerShellQtInterface.so.6")
    get = lib["_ZN12LayerShellQt6Window3getEP7QWindow"]
    get.restype = ctypes.c_void_p
    get.argtypes = [ctypes.c_void_p]
    pointer = get(shiboken6.getCppPointer(window.windowHandle())[0])
    layer_window = shiboken6.wrapInstance(pointer, QObject)
    results = {
        "anchors": layer_window.setProperty("anchors", 2 | 8),  # AnchorBottom | AnchorRight
        "layer": layer_window.setProperty("layer", 2),  # LayerTop
        "keyboardInteractivity": layer_window.setProperty("keyboardInteractivity", 2),  # OnDemand
        "margins": layer_window.setProperty("margins", QMargins(0, 0, 12, 12)),
        "scope": layer_window.setProperty("scope", "kimai-tray-popup"),
    }
    read_back = {}
    for key in results:
        try:
            read_back[key] = str(layer_window.property(key))
        except RuntimeError as error:  # PySide has no converter for QFlags<LayerShellQt::Window::Anchor>
            read_back[key] = f"<unreadable: {error}>"
    log("layer.configured", set_ok=results, read_back=read_back)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="tool", choices=["tool", "popup", "normal"])
    parser.add_argument("--guard-ms", type=int, default=0, help="ignore a click this soon after hide-on-focus-loss")
    parser.add_argument("--width", type=int, default=460)
    parser.add_argument("--height", type=int, default=560)
    parser.add_argument("--layer", action="store_true", help="KDE only: anchor the window with layer-shell-qt")
    parser.add_argument("--start-running", action="store_true", help="simulate a running timer from the start")
    args = parser.parse_args()
    if args.layer:
        # Must be set before QApplication; the plugin then serves every window of the process.
        os.environ["QT_WAYLAND_SHELL_INTEGRATION"] = "layer-shell"

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setApplicationName("kimai-tray-prototyp")
    app.setDesktopFileName("kimai-tray-prototyp")
    log(
        "start",
        pid=os.getpid(),
        platform=QGuiApplication.platformName(),
        tray_available=QSystemTrayIcon.isSystemTrayAvailable(),
        messages_supported=QSystemTrayIcon.supportsMessages(),
        mode=args.mode,
        guard_ms=args.guard_ms,
        env={k: os.environ.get(k) for k in ("XDG_CURRENT_DESKTOP", "XDG_SESSION_TYPE", "QT_WAYLAND_SHELL_INTEGRATION",
                                           "LAYERSHELLQT_ANCHORS", "LAYERSHELLQT_LAYER", "FLATPAK_ID")},
    )

    window = QuickWindow(args.mode, (args.width, args.height))
    if args.layer:
        anchor_bottom_right(window)
    tray = QSystemTrayIcon(dot_icon("#6b7280"))
    tray.setToolTip("Kimai Tray — prototyp")

    menu = QMenu()
    toggle_action = QAction("Pokaż / schowaj okno")
    running_action = QAction("Symuluj start timera")
    quit_action = QAction("Zakończ prototyp")
    menu.addAction(toggle_action)
    menu.addAction(running_action)
    menu.addSeparator()
    menu.addAction(quit_action)
    tray.setContextMenu(menu)

    started_at: list[float] = []

    def toggle(source: str) -> None:
        since_hide = None if window.last_hidden_at is None else round((time.monotonic() - window.last_hidden_at) * 1000)
        if window.isVisible():
            log("toggle.hide", source=source)
            window.hide()
            return
        if since_hide is not None and since_hide < args.guard_ms:
            log("toggle.ignored_by_guard", source=source, ms_since_hide=since_hide)
            return
        log("toggle.show", source=source, ms_since_hide=since_hide, tray_geometry=list(tray.geometry().getRect()))
        window.show()
        window.raise_()
        window.activateWindow()
        window.description.setFocus()

    def on_activated(reason: QSystemTrayIcon.ActivationReason) -> None:
        log("tray.activated", reason=reason.name, tray_geometry=list(tray.geometry().getRect()))
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            toggle("tray-left-click")

    def simulate_start() -> None:
        started_at[:] = [time.monotonic()]
        tray.setIcon(dot_icon("#16a34a"))
        log("timer.started")

    def tick() -> None:
        if not started_at:
            return
        seconds = int(time.monotonic() - started_at[0])
        tray.setToolTip(f"Kimai Tray — {seconds // 3600}:{seconds // 60 % 60:02d}:{seconds % 60:02d} — Moduł rezerwacji")

    tray.activated.connect(on_activated)
    toggle_action.triggered.connect(lambda: toggle("menu"))
    running_action.triggered.connect(simulate_start)
    quit_action.triggered.connect(app.quit)
    timer = QTimer()
    timer.timeout.connect(tick)
    timer.start(1000)

    if args.start_running:
        simulate_start()
    tray.show()
    QTimer.singleShot(500, lambda: log("tray.shown", visible=tray.isVisible(), geometry=list(tray.geometry().getRect())))
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
