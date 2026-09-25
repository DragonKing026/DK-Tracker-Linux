import pytest
from jeepney import HeaderFields, new_error, new_method_return

from kimai_tray.desktop.bus import PORTAL, PORTAL_PATH, DBusCallError, PortalError, SessionBus, portal_request

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


def test_portal_request_timeout_closes_the_request():
    """Otherwise the portal dialog may stay open after we gave up."""
    bus = FakeBus()
    bus.on(PORTAL_PATH, "org.example.Iface", "Do", ("/some/handle",))  # never answers
    bus.on("/some/handle", REQUEST, "Close", ())
    with pytest.raises(TimeoutError):
        portal_request(bus, "org.example.Iface", "Do", "sa{sv}", build, timeout=0.01)
    assert bus.calls[-1][1:4] == ("/some/handle", REQUEST, "Close")


def test_portal_request_timeout_survives_a_failing_close():
    bus = FakeBus()
    bus.on(PORTAL_PATH, "org.example.Iface", "Do", ("/some/handle",))  # no Close handler → UnknownMethod
    with pytest.raises(TimeoutError):
        portal_request(bus, "org.example.Iface", "Do", "sa{sv}", build, timeout=0.01)


class FakeFilter:
    """Mimics jeepney's FilterHandle: a second close raises KeyError."""

    def __init__(self, filters, queue):
        self.filters = filters
        self.queue = queue
        filters.add(id(self))

    def __enter__(self):
        return self.queue

    def __exit__(self, *exc):
        self.filters.remove(id(self))
        return False


class FakeConnection:
    unique_name = ":1.9"

    def __init__(self, fail=()):
        self.fail = set(fail)  # member names answered with an error
        self.sent = []
        self.filters = set()

    def send_and_get_reply(self, message, timeout=None):
        self.sent.append(message.header.fields[HeaderFields.member])
        if message.header.fields[HeaderFields.member] in self.fail:
            return new_error(message, "org.freedesktop.DBus.Error.LimitsExceeded", "s", ("too many",))
        return new_method_return(message)

    def filter(self, rule, queue):
        return FakeFilter(self.filters, queue)


def test_expectation_close_is_idempotent():
    connection = FakeConnection()
    expectation = SessionBus(connection).expect("/p", "org.example.Iface", "Sig")
    expectation.close()
    expectation.close()
    assert connection.filters == set()
    assert connection.sent.count("RemoveMatch") == 1


def test_expect_reports_a_refused_subscription():
    connection = FakeConnection(fail={"AddMatch"})
    with pytest.raises(DBusCallError) as caught:
        SessionBus(connection).expect("/p", "org.example.Iface", "Sig")
    assert caught.value.name == "org.freedesktop.DBus.Error.LimitsExceeded"
    assert connection.filters == set()


def test_call_turns_error_replies_into_dbus_call_errors():
    connection = FakeConnection(fail={"Do"})
    with pytest.raises(DBusCallError) as caught:
        SessionBus(connection).call("org.example", "/p", "org.example.Iface", "Do")
    assert (caught.value.name, caught.value.message) == (
        "org.freedesktop.DBus.Error.LimitsExceeded",
        "too many",
    )
