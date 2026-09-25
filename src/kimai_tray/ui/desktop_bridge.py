"""The desktop services of Plan 2, arranged for the UI's threads.

`Desktop` owns one SessionBus and is used only from the desktop worker thread (a jeepney
connection is not thread-safe). Clicks on notifications are heard by `ClickListener` on a
connection of its own: the portal broadcasts ActionInvoked without a destination, so a
second connection receives them (docs/integracje/xdg-portale.md).
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from PySide6.QtCore import QThread, Signal

from kimai_tray.core.notification_policy import RenderedNotification
from kimai_tray.desktop.autostart import BackgroundPortal, BackgroundResult
from kimai_tray.desktop.bus import Bus, SessionBus, register_host_app
from kimai_tray.desktop.notifications import PortalNotifier
from kimai_tray.desktop.secrets import SecretServiceStore, SecretsUnavailable

log = logging.getLogger(__name__)
AUTOSTART_COMMAND = ["kimai-tray", "--hidden"]
APP_ID = "pl.websystems.KimaiTray"


class Desktop:
    def __init__(self, bus_factory: Callable[[], Bus] = SessionBus, *, register: bool = True) -> None:
        self._factory = bus_factory
        self._register = register
        self._bus: Bus | None = None

    def _connection(self) -> Bus:
        if self._bus is None:
            self._bus = self._factory()
            if self._register:
                register_host_app(self._bus, APP_ID)
        return self._bus

    def get_token(self, url: str) -> str | None:
        return SecretServiceStore(self._secrets_bus()).get(url)

    def set_token(self, url: str, token: str) -> None:
        SecretServiceStore(self._secrets_bus()).set(url, token)

    def notify(self, rendered: RenderedNotification) -> None:
        PortalNotifier(self._connection()).show(rendered)

    def withdraw(self, notification_id: str) -> None:
        PortalNotifier(self._connection()).withdraw(notification_id)

    def request_background(self, *, autostart: bool, reason: str) -> BackgroundResult:
        return BackgroundPortal(self._connection()).request(
            autostart=autostart, reason=reason, commandline=AUTOSTART_COMMAND if autostart else None
        )

    def set_status(self, message: str) -> bool:
        return BackgroundPortal(self._connection()).set_status(message)

    def close(self) -> None:
        close = getattr(self._bus, "close", None)
        if close is not None:
            close()
        self._bus = None

    def _secrets_bus(self) -> Bus:
        try:
            return self._connection()
        except (OSError, KeyError, ValueError) as error:  # no session bus at all
            raise SecretsUnavailable(type(error).__name__) from None


class ClickListener(QThread):
    clicked = Signal(object)  # NotificationAction

    def __init__(self, bus_factory: Callable[[], Any] = SessionBus, poll_seconds: float = 0.5) -> None:
        super().__init__()
        self._factory = bus_factory
        self._poll = poll_seconds
        self._stopping = False

    def stop(self) -> None:
        self._stopping = True

    def run(self) -> None:
        try:
            bus = self._factory()
            expectation = PortalNotifier(bus).listen()
        except Exception as error:  # noqa: BLE001 - no clicks is better than no app
            log.warning("Notification clicks will not be heard: %s", error)
            return
        try:
            while not self._stopping:
                try:
                    body = expectation.wait(self._poll)
                except TimeoutError:
                    continue
                self.clicked.emit(PortalNotifier.parse(body))
        finally:
            expectation.close()
            close = getattr(bus, "close", None)
            if close is not None:
                close()
