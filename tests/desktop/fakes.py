"""Scriptable stand-in for kimai_tray.desktop.bus.Bus."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from kimai_tray.desktop.bus import DBusCallError

Key = tuple[str, str, str]


class FakeExpectation:
    def __init__(self, bus: FakeBus, key: Key) -> None:
        self.bus = bus
        self.key = key

    def wait(self, timeout: float) -> tuple[Any, ...]:
        queue = self.bus.signals.get(self.key)
        if not queue:
            raise TimeoutError(f"no {self.key[2]} on {self.key[0]}")
        return queue.pop(0)

    def close(self) -> None:
        self.bus.closed.append(self.key)


class FakeBus:
    unique_name = ":1.42"

    def __init__(self) -> None:
        self.handlers: dict[Key, tuple | Callable[[tuple], tuple] | Exception] = {}
        self.calls: list[tuple] = []
        self.signals: dict[Key, list[tuple]] = {}
        self.closed: list[Key] = []

    def on(self, path: str, interface: str, member: str, reply) -> None:
        self.handlers[(path, interface, member)] = reply

    def emit(self, path: str, interface: str, member: str, body: tuple) -> None:
        self.signals.setdefault((path, interface, member), []).append(body)

    def call(self, destination, path, interface, member, signature="", body=(), timeout=25.0):
        self.calls.append((destination, path, interface, member, signature, body))
        reply = self.handlers.get((path, interface, member))
        if reply is None:
            raise DBusCallError("org.freedesktop.DBus.Error.UnknownMethod", f"{interface}.{member} at {path}")
        if isinstance(reply, Exception):
            raise reply
        return reply(body) if callable(reply) else reply

    def expect(self, path: str, interface: str, member: str) -> FakeExpectation:
        return FakeExpectation(self, (path, interface, member))

    def members(self) -> list[str]:
        return [call[3] for call in self.calls]
