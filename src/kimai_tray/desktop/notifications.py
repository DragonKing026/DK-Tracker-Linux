"""Notifications through xdg-desktop-portal (org.freedesktop.portal.Notification, v1 on Plasma 6.7).

Clicks come back as ActionInvoked(id, action, parameter). The parameter carries platform data
(an activation token) rather than our button target, so the entry is identified by the
notification id ("long-timer-<entry id>") — verified on the host and inside Flatpak.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from kimai_tray.core.notification_policy import RenderedNotification, entry_id_from

from .bus import PORTAL, PORTAL_PATH, Bus, Expectation

_INTERFACE = "org.freedesktop.portal.Notification"


@dataclass(frozen=True)
class NotificationAction:
    notification_id: str
    action: str  # "stop" | "keep" | "settings"
    entry_id: int | None


class PortalNotifier:
    def __init__(self, bus: Bus) -> None:
        self._bus = bus

    def show(self, rendered: RenderedNotification) -> None:
        payload: dict[str, Any] = {"title": ("s", rendered.title), "priority": ("s", "normal")}
        if rendered.body:
            payload["body"] = ("s", rendered.body)
        if rendered.buttons:
            payload["buttons"] = (
                "aa{sv}",
                [{"label": ("s", label), "action": ("s", action)} for label, action in rendered.buttons],
            )
        self._bus.call(PORTAL, PORTAL_PATH, _INTERFACE, "AddNotification", "sa{sv}", (rendered.id, payload))

    def withdraw(self, notification_id: str) -> None:
        self._bus.call(PORTAL, PORTAL_PATH, _INTERFACE, "RemoveNotification", "s", (notification_id,))

    def listen(self) -> Expectation:
        """Subscribe to clicks; the UI waits on it in a worker thread (Plan 3)."""
        return self._bus.expect(PORTAL_PATH, _INTERFACE, "ActionInvoked")

    @staticmethod
    def parse(body: tuple[Any, ...]) -> NotificationAction:
        notification_id, action = body[0], body[1]
        return NotificationAction(notification_id, action, entry_id_from(notification_id))
