import pytest

from kimai_tray.desktop.bus import PORTAL, PORTAL_PATH, DBusCallError, PortalError, portal_request

from .fakes import FakeBus

REQUEST = "org.freedesktop.portal.Request"
HANDLE_PREFIX = f"{PORTAL_PATH}/request/1_42/"


def answering(bus, code, results):
    """Handler that answers like a portal: Response on the handle derived from our token."""

    def handler(body):
        token = body[1]["handle_token"][1]
        handle = HANDLE_PREFIX + token
        bus.emit(handle, REQUEST, "Response", (code, results))
        return (handle,)

    return handler


def build(token):
    return ("", {"handle_token": ("s", token), "reason": ("s", "test")})


def test_portal_request_returns_unwrapped_results():
    bus = FakeBus()
    bus.on(PORTAL_PATH, "org.example.Iface", "Do", answering(bus, 0, {"background": ("b", True)}))
    assert portal_request(bus, "org.example.Iface", "Do", "sa{sv}", build) == {"background": True}
    destination, path, interface, member, signature, body = bus.calls[0]
    assert (destination, interface, member, signature) == (PORTAL, "org.example.Iface", "Do", "sa{sv}")
    assert body[1]["handle_token"][1].startswith("kimai_")
    assert bus.closed and bus.closed[0][0].startswith(HANDLE_PREFIX)  # subscription always released


@pytest.mark.parametrize("code", [1, 2])
def test_portal_request_non_zero_response_is_an_error(code):
    bus = FakeBus()
    bus.on(PORTAL_PATH, "org.example.Iface", "Do", answering(bus, code, {}))
    with pytest.raises(PortalError) as caught:
        portal_request(bus, "org.example.Iface", "Do", "sa{sv}", build)
    assert caught.value.response == code


def test_portal_request_timeout_releases_subscription():
    bus = FakeBus()
    bus.on(PORTAL_PATH, "org.example.Iface", "Do", ("/some/handle",))  # never answers
    with pytest.raises(TimeoutError):
        portal_request(bus, "org.example.Iface", "Do", "sa{sv}", build, timeout=0.01)
    assert len(bus.closed) == 1


def test_call_errors_carry_name_and_message():
    error = DBusCallError("org.freedesktop.DBus.Error.AccessDenied", "nope")
    assert (error.name, error.message) == ("org.freedesktop.DBus.Error.AccessDenied", "nope")
    assert "AccessDenied" in str(error)
