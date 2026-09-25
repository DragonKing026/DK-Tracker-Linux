from kimai_tray.core.notification_policy import RenderedNotification
from kimai_tray.desktop.bus import PORTAL, PORTAL_PATH
from kimai_tray.desktop.notifications import NotificationAction, PortalNotifier

from .fakes import FakeBus

IFACE = "org.freedesktop.portal.Notification"


def test_show_sends_title_body_and_buttons():
    bus = FakeBus()
    bus.on(PORTAL_PATH, IFACE, "AddNotification", ())
    PortalNotifier(bus).show(
        RenderedNotification(
            "long-timer-7",
            "Timer działa od 8:00",
            "Projekt — opis",
            (("Zatrzymaj", "stop"), ("Działa dalej", "keep")),
        )
    )
    destination, _, _, member, signature, body = bus.calls[0]
    assert (destination, member, signature) == (PORTAL, "AddNotification", "sa{sv}")
    notification_id, payload = body
    assert notification_id == "long-timer-7"
    assert payload["title"] == ("s", "Timer działa od 8:00")
    assert payload["body"] == ("s", "Projekt — opis")
    assert payload["buttons"] == (
        "aa{sv}",
        [
            {"label": ("s", "Zatrzymaj"), "action": ("s", "stop")},
            {"label": ("s", "Działa dalej"), "action": ("s", "keep")},
        ],
    )


def test_show_without_body_or_buttons_omits_them():
    bus = FakeBus()
    bus.on(PORTAL_PATH, IFACE, "AddNotification", ())
    PortalNotifier(bus).show(RenderedNotification("connection", "Połączenie przywrócone", "", ()))
    payload = bus.calls[0][5][1]
    assert set(payload) == {"title", "priority"}


def test_withdraw():
    bus = FakeBus()
    bus.on(PORTAL_PATH, IFACE, "RemoveNotification", ())
    PortalNotifier(bus).withdraw("long-timer-7")
    assert bus.calls[0][3:] == ("RemoveNotification", "s", ("long-timer-7",))


def test_listen_and_parse_a_click():
    bus = FakeBus()
    expectation = PortalNotifier(bus).listen()
    # verified shape: the parameter carries platform data, not our target
    bus.emit(
        PORTAL_PATH,
        IFACE,
        "ActionInvoked",
        ("long-timer-7", "stop", [("a{sv}", {"activation-token": ("s", "kwin-1")})]),
    )
    assert PortalNotifier.parse(expectation.wait(1)) == NotificationAction("long-timer-7", "stop", 7)


def test_parse_action_without_entry():
    assert PortalNotifier.parse(("connection", "settings", [])) == NotificationAction(
        "connection", "settings", None
    )
