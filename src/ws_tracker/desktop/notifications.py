"""Notifications through xdg-desktop-portal (org.freedesktop.portal.Notification, v1 on Plasma 6.7).

Clicks come back as ActionInvoked(id, action, parameter). The parameter carries platform data
(an activation token) rather than our button target, so the entry is identified by the
notification id ("long-timer-<entry id>") — verified on the host and inside Flatpak.
"""

from __future__ import annotations

import itertools
import time
from dataclasses import dataclass
from typing import Any

from ws_tracker.core.notification_policy import RenderedNotification, entry_id_from

from .bus import PORTAL, PORTAL_PATH, Bus, DBusCallError, Expectation

_INTERFACE = "org.freedesktop.portal.Notification"


@dataclass(frozen=True)
class NotificationAction:
    notification_id: str
    action: str  # "stop" | "keep" | "settings"
    entry_id: int | None


class PortalNotifier:
    """Sends notifications; one instance per connection, because it remembers what it showed.

    KDE's portal (Plasma 6.7.5) treats an id it has seen as an update of that notification and
    shows nothing once the old one is gone — so every notification gets a fresh id
    ("action.1790374275"), and the previous one of the same kind is withdrawn first.
    """

    def __init__(self, bus: Bus, first_number: int | None = None) -> None:
        self._bus = bus
        # Seconds since the epoch: numbers keep growing across restarts of the app.
        self._numbers = itertools.count(int(time.time()) if first_number is None else first_number)
        self._shown: dict[str, str] = {}  # kind ("action", "long-timer-7") -> id on screen

    def show(self, rendered: RenderedNotification) -> None:
        payload: dict[str, Any] = {"title": ("s", rendered.title), "priority": ("s", "normal")}
        if rendered.body:
            payload["body"] = ("s", rendered.body)
        if rendered.buttons:
            payload["buttons"] = (
                "aa{sv}",
                [{"label": ("s", label), "action": ("s", action)} for label, action in rendered.buttons],
            )
        previous = self._shown.get(rendered.id)
        if previous is not None:
            try:
                self.withdraw(previous)
            except DBusCallError:
                pass  # already gone; the new one is shown anyway
        notification_id = f"{rendered.id}.{next(self._numbers)}"
        self._bus.call(
            PORTAL, PORTAL_PATH, _INTERFACE, "AddNotification", "sa{sv}", (notification_id, payload)
        )
        self._shown[rendered.id] = notification_id

    def withdraw(self, notification_id: str) -> None:
        """By the id the portal knows, or by kind ("connection") for the one shown last."""
        shown = self._shown.pop(notification_id, None)
        if shown is None:
            kind = notification_id.rsplit(".", 1)[0]
            if self._shown.get(kind) == notification_id:
                del self._shown[kind]
        target = shown or notification_id
        self._bus.call(PORTAL, PORTAL_PATH, _INTERFACE, "RemoveNotification", "s", (target,))

    def listen(self) -> Expectation:
        """Subscribe to clicks; the UI waits on it in a worker thread (Plan 3).

        The portal broadcasts ActionInvoked without a destination, so the listener may use
        its own SessionBus (one connection per thread) and still hear clicks on notifications
        sent through another connection.
        """
        return self._bus.expect(PORTAL_PATH, _INTERFACE, "ActionInvoked")

    @staticmethod
    def parse(body: tuple[Any, ...]) -> NotificationAction:
        notification_id, action = body[0], body[1]
        kind = notification_id.rsplit(".", 1)[0]  # "long-timer-7.1790374275" -> "long-timer-7"
        return NotificationAction(notification_id, action, entry_id_from(kind))
