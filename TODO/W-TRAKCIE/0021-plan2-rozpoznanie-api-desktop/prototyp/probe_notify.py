"""Probe: xdg-desktop-portal Notification with buttons; wait for ActionInvoked."""
import time
from jeepney import DBusAddress, MatchRule, message_bus, new_method_call
from jeepney.io.blocking import open_dbus_connection

portal = DBusAddress("/org/freedesktop/portal/desktop", bus_name="org.freedesktop.portal.Desktop",
                     interface="org.freedesktop.portal.Notification")
with open_dbus_connection(bus="SESSION") as c:
    props = DBusAddress("/org/freedesktop/portal/desktop", bus_name="org.freedesktop.portal.Desktop",
                        interface="org.freedesktop.DBus.Properties")
    print("version:", c.send_and_get_reply(new_method_call(props, "Get", "ss", ("org.freedesktop.portal.Notification", "version"))).body)
    rule = MatchRule(type="signal", interface="org.freedesktop.portal.Notification", member="ActionInvoked",
                     path="/org/freedesktop/portal/desktop")
    c.send_and_get_reply(message_bus.AddMatch(rule))
    note = {
        "title": ("s", "Kimai Tray — test (poza Flatpakiem)"),
        "body": ("s", "Timer działa od 8:00 — Moduł rezerwacji. Kliknij przycisk (test powiadomień)."),
        "priority": ("s", "normal"),
        "buttons": ("aa{sv}", [
            {"label": ("s", "Zatrzymaj"), "action": ("s", "stop"), "target": ("v", ("i", 123))},
            {"label": ("s", "Działa dalej"), "action": ("s", "keep")},
        ]),
    }
    reply = c.send_and_get_reply(new_method_call(portal, "AddNotification", "sa{sv}", ("long-timer-123", note)))
    print("AddNotification ->", reply.header.message_type.name, reply.body)
    deadline = time.monotonic() + 90
    got = None
    with c.filter(rule) as queue:
        while time.monotonic() < deadline and got is None:
            try:
                got = c.recv_until_filtered(queue, timeout=deadline - time.monotonic())
            except TimeoutError:
                break
    print("ActionInvoked ->", got.body if got else "brak (timeout 90 s)")
    pass  # keep it visible
    print("powiadomienie zostawione")
