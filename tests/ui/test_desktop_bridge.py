from kimai_tray.core.notification_policy import RenderedNotification
from kimai_tray.desktop.bus import PORTAL_PATH
from kimai_tray.desktop.notifications import NotificationAction
from kimai_tray.ui.desktop_bridge import ClickListener, Desktop

from ..desktop.fakes import FakeBus

NOTIFY = "org.freedesktop.portal.Notification"


def test_bus_is_opened_once_and_lazily():
    opened = []

    def factory():
        bus = FakeBus()
        bus.on(PORTAL_PATH, NOTIFY, "AddNotification", ())
        opened.append(bus)
        return bus

    desktop = Desktop(factory, register=False)
    assert opened == []
    desktop.notify(RenderedNotification("connection", "Brak połączenia", "", ()))
    desktop.notify(RenderedNotification("connection", "Brak połączenia", "", ()))
    assert len(opened) == 1
    assert opened[0].members() == ["AddNotification", "AddNotification"]


def test_listener_emits_parsed_clicks(qtbot):
    bus = FakeBus()
    bus.emit(PORTAL_PATH, NOTIFY, "ActionInvoked", ("long-timer-7", "stop", []))
    listener = ClickListener(lambda: bus, poll_seconds=0.01)
    with qtbot.waitSignal(listener.clicked, timeout=2000) as signal:
        listener.start()
    assert signal.args == [NotificationAction("long-timer-7", "stop", 7)]
    listener.stop()
    assert listener.wait(2000)


def test_listener_without_a_bus_just_ends(qtbot):
    def broken():
        raise OSError("no session bus")

    listener = ClickListener(broken, poll_seconds=0.01)
    listener.start()
    assert listener.wait(2000)


def test_first_use_registers_the_app_with_the_portal():
    bus = FakeBus()
    bus.on(PORTAL_PATH, "org.freedesktop.host.portal.Registry", "Register", ())
    bus.on(PORTAL_PATH, NOTIFY, "RemoveNotification", ())
    Desktop(lambda: bus).withdraw("long-timer-7")
    assert bus.members() == ["Register", "RemoveNotification"]
