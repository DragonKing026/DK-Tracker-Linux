from dk_tracker.core.notification_policy import RenderedNotification
from dk_tracker.desktop.bus import PORTAL, PORTAL_PATH
from dk_tracker.desktop.notifications import NotificationAction, PortalNotifier

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
    assert notification_id.startswith("long-timer-7.")
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


def test_every_notification_gets_a_fresh_id_and_replaces_the_previous_one():
    """KDE's portal never shows a notification again under an id it has seen (checked on Plasma 6.7.5)."""
    bus = FakeBus()
    bus.on(PORTAL_PATH, IFACE, "AddNotification", ())
    bus.on(PORTAL_PATH, IFACE, "RemoveNotification", ())
    notifier = PortalNotifier(bus, first_number=1)
    notifier.show(RenderedNotification("action", "Start: a", "", ()))
    notifier.show(RenderedNotification("action", "Stop: a", "", ()))
    sent = [(call[3], call[5][0]) for call in bus.calls]
    assert sent == [
        ("AddNotification", "action.1"),
        ("RemoveNotification", "action.1"),
        ("AddNotification", "action.2"),
    ]


def test_click_on_a_numbered_long_timer_id_still_names_the_entry():
    action = PortalNotifier.parse(("long-timer-7.3", "stop", []))
    assert action == NotificationAction("long-timer-7.3", "stop", 7)


def test_a_previous_notification_already_gone_does_not_stop_the_next():
    bus = FakeBus()
    bus.on(PORTAL_PATH, IFACE, "AddNotification", ())  # no RemoveNotification handler: it fails
    notifier = PortalNotifier(bus, first_number=1)
    notifier.show(RenderedNotification("action", "Start: a", "", ()))
    notifier.show(RenderedNotification("action", "Stop: a", "", ()))
    assert bus.members()[-1] == "AddNotification"


def test_withdraw_by_kind_removes_what_is_on_screen():
    bus = FakeBus()
    bus.on(PORTAL_PATH, IFACE, "AddNotification", ())
    bus.on(PORTAL_PATH, IFACE, "RemoveNotification", ())
    notifier = PortalNotifier(bus, first_number=5)
    notifier.show(RenderedNotification("connection", "Brak połączenia", "", ()))
    notifier.withdraw("connection")
    assert bus.calls[-1][3:] == ("RemoveNotification", "s", ("connection.5",))
