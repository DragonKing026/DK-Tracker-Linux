import pytest

from kimai_tray.desktop.autostart import STATUS_MAX, BackgroundPortal, BackgroundResult
from kimai_tray.desktop.bus import PORTAL_PATH, DBusCallError, PortalError

from .fakes import FakeBus

IFACE = "org.freedesktop.portal.Background"
REQUEST = "org.freedesktop.portal.Request"


def portal(code=0, results=None):
    bus = FakeBus()

    def handler(body):
        handle = f"{PORTAL_PATH}/request/1_42/{body[1]['handle_token'][1]}"
        bus.emit(handle, REQUEST, "Response", (code, results or {}))
        return (handle,)

    bus.on(PORTAL_PATH, IFACE, "RequestBackground", handler)
    return bus


def test_request_autostart_with_commandline():
    bus = portal(results={"background": ("b", True), "autostart": ("b", True)})
    result = BackgroundPortal(bus).request(
        autostart=True, reason="Pomiar czasu w tle", commandline=["kimai-tray", "--hidden"]
    )
    assert result == BackgroundResult(background=True, autostart=True)
    parent_window, options = bus.calls[0][5]
    assert parent_window == ""
    assert options["autostart"] == ("b", True)
    assert options["reason"] == ("s", "Pomiar czasu w tle")
    assert options["commandline"] == ("as", ["kimai-tray", "--hidden"])


def test_request_without_commandline_omits_it():
    bus = portal(results={"background": ("b", True), "autostart": ("b", False)})
    assert BackgroundPortal(bus).request(autostart=False, reason="r") == BackgroundResult(True, False)
    assert "commandline" not in bus.calls[0][5][1]


def test_user_refusal_is_a_portal_error():
    with pytest.raises(PortalError):
        BackgroundPortal(portal(code=1)).request(autostart=True, reason="r")


def test_set_status_in_sandbox():
    bus = FakeBus()
    bus.on(PORTAL_PATH, IFACE, "SetStatus", ())
    assert BackgroundPortal(bus).set_status("Timer: 1:22 — Moduł rezerwacji") is True
    assert bus.calls[0][5] == ({"message": ("s", "Timer: 1:22 — Moduł rezerwacji")},)


def test_set_status_outside_sandbox_is_ignored():
    bus = FakeBus()
    bus.on(
        PORTAL_PATH,
        IFACE,
        "SetStatus",
        DBusCallError(
            "org.freedesktop.portal.Error.NotAllowed", "Only sandboxed applications can set background status"
        ),
    )
    assert BackgroundPortal(bus).set_status("x") is False


def test_status_is_trimmed_to_96_characters():
    bus = FakeBus()
    bus.on(PORTAL_PATH, IFACE, "SetStatus", ())
    BackgroundPortal(bus).set_status("x" * 200)
    sent = bus.calls[0][5][0]["message"][1]
    assert len(sent) == STATUS_MAX
    assert sent.endswith("…")
