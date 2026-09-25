"""Autostart and background status through xdg-desktop-portal (org.freedesktop.portal.Background v2).

Verified on Plasma 6.7.5: RequestBackground answers through Request.Response; SetStatus
works only for sandboxed apps (outside Flatpak the portal refuses — we ignore that).
"""

from __future__ import annotations

from dataclasses import dataclass

from .bus import PORTAL, PORTAL_PATH, Bus, DBusCallError, portal_request

_INTERFACE = "org.freedesktop.portal.Background"
STATUS_MAX = 96  # the portal's limit for the status message


@dataclass(frozen=True)
class BackgroundResult:
    background: bool
    autostart: bool


class BackgroundPortal:
    def __init__(self, bus: Bus, timeout: float = 120.0) -> None:
        self._bus = bus
        self._timeout = timeout

    def request(
        self, *, autostart: bool, reason: str, commandline: list[str] | None = None
    ) -> BackgroundResult:
        """Ask to keep running in the background and (optionally) to start with the session."""

        def body(token: str) -> tuple:
            options = {"handle_token": ("s", token), "reason": ("s", reason), "autostart": ("b", autostart)}
            if commandline:
                options["commandline"] = ("as", commandline)
            return ("", options)

        results = portal_request(self._bus, _INTERFACE, "RequestBackground", "sa{sv}", body, self._timeout)
        return BackgroundResult(bool(results.get("background", False)), bool(results.get("autostart", False)))

    def set_status(self, message: str) -> bool:
        """Short status shown by the desktop for background apps; False when not allowed."""
        text = message if len(message) <= STATUS_MAX else message[: STATUS_MAX - 1] + "…"
        try:
            self._bus.call(PORTAL, PORTAL_PATH, _INTERFACE, "SetStatus", "a{sv}", ({"message": ("s", text)},))
        except DBusCallError:
            return False  # outside a sandbox: "Only sandboxed applications can set background status"
        return True
