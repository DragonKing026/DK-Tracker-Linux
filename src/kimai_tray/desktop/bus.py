"""A small D-Bus layer over jeepney: method calls, awaited signals and the portal
Request/Response pattern. Services depend on the `Bus` protocol, so tests use a fake.

Facts behind this module: TODO/…/0021-plan2-rozpoznanie-api-desktop/notatki/rozpoznanie.md.
"""

from __future__ import annotations

import secrets
from collections import deque
from collections.abc import Callable
from typing import Any, Protocol

from jeepney import DBusAddress, HeaderFields, MatchRule, MessageType, message_bus, new_method_call
from jeepney.io.blocking import open_dbus_connection

PORTAL = "org.freedesktop.portal.Desktop"
PORTAL_PATH = "/org/freedesktop/portal/desktop"
_REQUEST = "org.freedesktop.portal.Request"


class DBusCallError(Exception):
    """The other side answered with a D-Bus error."""

    def __init__(self, name: str, message: str = "") -> None:
        super().__init__(f"{name}: {message}" if message else name)
        self.name = name
        self.message = message


class PortalError(Exception):
    """A portal request ended without success (1 = cancelled by the user, 2 = other)."""

    def __init__(self, response: int) -> None:
        super().__init__(f"portal response {response}")
        self.response = response


class Expectation(Protocol):
    def wait(self, timeout: float) -> tuple[Any, ...]: ...

    def close(self) -> None: ...


class Bus(Protocol):
    unique_name: str

    def call(
        self,
        destination: str,
        path: str,
        interface: str,
        member: str,
        signature: str = "",
        body: tuple = (),
        timeout: float = 25.0,
    ) -> tuple[Any, ...]: ...

    def expect(self, path: str, interface: str, member: str) -> Expectation: ...


class _JeepneyExpectation:
    def __init__(self, connection: Any, rule: MatchRule) -> None:
        self._connection = connection
        self._rule = rule
        # Several signals may arrive between two waits (e.g. notification clicks).
        self._filter = connection.filter(rule, queue=deque(maxlen=64))
        self._queue = self._filter.__enter__()

    def wait(self, timeout: float) -> tuple[Any, ...]:
        return self._connection.recv_until_filtered(self._queue, timeout=timeout).body

    def close(self) -> None:
        self._filter.__exit__(None, None, None)
        try:
            self._connection.send_and_get_reply(message_bus.RemoveMatch(self._rule), timeout=5)
        except Exception:  # noqa: BLE001 - the connection may already be closing
            pass


class SessionBus:
    """One blocking session-bus connection. Not thread-safe: use one per thread."""

    def __init__(self) -> None:
        self._connection = open_dbus_connection(bus="SESSION")
        self.unique_name: str = self._connection.unique_name

    def close(self) -> None:
        self._connection.close()

    def call(
        self,
        destination: str,
        path: str,
        interface: str,
        member: str,
        signature: str = "",
        body: tuple = (),
        timeout: float = 25.0,
    ) -> tuple[Any, ...]:
        address = DBusAddress(path, bus_name=destination, interface=interface)
        reply = self._connection.send_and_get_reply(
            new_method_call(address, member, signature or None, body), timeout=timeout
        )
        if reply.header.message_type is MessageType.error:
            name = reply.header.fields.get(HeaderFields.error_name, "org.freedesktop.DBus.Error.Failed")
            text = reply.body[0] if reply.body and isinstance(reply.body[0], str) else ""
            raise DBusCallError(name, text)
        return reply.body

    def expect(self, path: str, interface: str, member: str) -> Expectation:
        rule = MatchRule(type="signal", path=path, interface=interface, member=member)
        self._connection.send_and_get_reply(message_bus.AddMatch(rule), timeout=5)
        return _JeepneyExpectation(self._connection, rule)


def portal_request(
    bus: Bus,
    interface: str,
    member: str,
    signature: str,
    build_body: Callable[[str], tuple],
    timeout: float = 120.0,
) -> dict[str, Any]:
    """Call a portal method that answers later with Request.Response.

    The Response arrives on a path derived from our unique name and a token we choose,
    so we subscribe to it *before* calling — otherwise a fast backend could answer first.
    """
    token = "kimai_" + secrets.token_hex(6)
    sender = bus.unique_name.lstrip(":").replace(".", "_")
    expectation = bus.expect(f"{PORTAL_PATH}/request/{sender}/{token}", _REQUEST, "Response")
    try:
        bus.call(PORTAL, PORTAL_PATH, interface, member, signature, build_body(token))
        code, results = expectation.wait(timeout)
    finally:
        expectation.close()
    if code != 0:
        raise PortalError(code)
    return {key: variant[1] for key, variant in results.items()}  # jeepney variants are (signature, value)
