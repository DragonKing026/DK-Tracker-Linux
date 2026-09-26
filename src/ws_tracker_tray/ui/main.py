"""Start-up: arguments, logging, one instance, Qt's own translations, waiting for the tray.

`--hidden` is what autostart runs: the app starts in the tray without opening the window.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from PySide6.QtCore import (
    QCoreApplication,
    QElapsedTimer,
    QEventLoop,
    QLibraryInfo,
    QObject,
    QTimer,
    QTranslator,
    Signal,
)
from PySide6.QtNetwork import QLocalServer, QLocalSocket
from PySide6.QtWidgets import QApplication

from ws_tracker_tray.core.settings import Memory, Settings, config_path, load_json, save_json, state_path

APP_ID = "pl.websystems.WsTrackerTray"
TRAY_WAIT_MS = 30_000  # at login the tray host may register after the autostarted app
log = logging.getLogger(__name__)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="ws-tracker-tray", description="Kimai time tracking in the system tray."
    )
    parser.add_argument("--hidden", action="store_true", help="start in the tray without opening the window")
    return parser.parse_args(argv)


def setup_logging(directory: Path, level: int = logging.INFO) -> Path:
    """A small rotating file next to the app state; tokens and headers are never logged."""
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "ws-tracker-tray.log"
    handler = RotatingFileHandler(path, maxBytes=512_000, backupCount=3, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    root = logging.getLogger()
    root.addHandler(handler)
    root.setLevel(level)
    return path


class SingleInstance(QObject):
    """A second start shows the running instance's window and exits (spec, section 5)."""

    showRequested = Signal()

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.server = QLocalServer(self)
        self.server.newConnection.connect(self._on_connection)

    def claim(self) -> bool:
        socket = QLocalSocket()
        socket.connectToServer(self.name)
        if socket.waitForConnected(500):
            socket.write(b"show\n")
            socket.waitForBytesWritten(500)
            socket.disconnectFromServer()
            return False
        QLocalServer.removeServer(self.name)  # left behind by a crash
        if not self.server.listen(self.name):
            # Better two windows than none: the app runs, only without the single-instance guard.
            log.warning("No single instance guard (%s): %s", self.name, self.server.errorString())
        return True

    def release(self) -> None:
        self.server.close()

    def _on_connection(self) -> None:
        # Any connection means "show the window"; its bytes do not matter.
        while (connection := self.server.nextPendingConnection()) is not None:
            connection.disconnected.connect(connection.deleteLater)
            self.showRequested.emit()


class QtTranslations:
    """Texts inside Qt's own widgets (context menus of text fields, "Cancel" …) in our language."""

    def __init__(self) -> None:
        self._translator: QTranslator | None = None

    def switch(self, language: str) -> None:
        if self._translator is not None:
            QCoreApplication.removeTranslator(self._translator)
            self._translator = None
        translator = QTranslator()
        path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
        if language != "en" and translator.load(f"qtbase_{language}", path):
            QCoreApplication.installTranslator(translator)
            self._translator = translator


def wait_for_tray(app: QApplication, limit_ms: int = TRAY_WAIT_MS) -> bool:
    from .tray import Tray

    clock = QElapsedTimer()
    clock.start()
    while not Tray.available() and clock.elapsed() < limit_ms:
        loop = QEventLoop()
        QTimer.singleShot(1000, loop.quit)
        loop.exec()
    return Tray.available()


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    log_path = setup_logging(state_path().parent)
    app = QApplication(sys.argv[:1])
    app.setApplicationName("ws-tracker-tray")
    app.setDesktopFileName(APP_ID)
    app.setQuitOnLastWindowClosed(False)
    from .icons import app_icon

    app.setWindowIcon(app_icon())  # Wayland: sent with xdg-toplevel-icon (KWin 6, Qt >= 6.8)

    instance = SingleInstance(f"ws-tracker-tray-{os.getuid()}")
    if not instance.claim():
        return 0  # the running instance opens its window

    from ws_tracker_tray.core.kimai_client import KimaiClient

    from . import placement
    from .app import Controller
    from .desktop_bridge import Desktop
    from .tray import Tray

    tray_available = Tray.available() or (args.hidden and wait_for_tray(app))
    settings = load_json(Settings, config_path())
    memory = load_json(Memory, state_path())
    controller = Controller(
        settings=settings,
        memory=memory,
        desktop=Desktop(),
        client_factory=lambda url, token: KimaiClient(url, token),
        save_settings=lambda value: save_json(value, config_path()),
        save_memory=lambda value: save_json(value, state_path()),
        tray_available=tray_available,
        window_mode=placement.detect_mode(app.platformName(), tray_available),
    )
    translations = QtTranslations()
    translations.switch(controller.state.t.language)
    controller.languageChanged.connect(translations.switch)
    instance.showRequested.connect(controller.show_popup)
    controller.quitRequested.connect(app.quit)
    app.aboutToQuit.connect(controller.shutdown)
    log.info("WS Tracker started (tray: %s, window: %s, log: %s)", tray_available, controller.mode, log_path)
    controller.start(hidden=args.hidden)
    return app.exec()
