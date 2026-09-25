"""Probe: xdg-desktop-portal Background (autostart=false) — Request/Response pattern."""
import secrets, time
from jeepney import DBusAddress, MatchRule, message_bus, new_method_call
from jeepney.io.blocking import open_dbus_connection

D = "org.freedesktop.portal.Desktop"
bg = DBusAddress("/org/freedesktop/portal/desktop", bus_name=D, interface="org.freedesktop.portal.Background")
props = DBusAddress("/org/freedesktop/portal/desktop", bus_name=D, interface="org.freedesktop.DBus.Properties")
with open_dbus_connection(bus="SESSION") as c:
    print("Background version:", c.send_and_get_reply(new_method_call(props, "Get", "ss", ("org.freedesktop.portal.Background", "version"))).body)
    sender = c.unique_name[1:].replace(".", "_")
    token = "kimai_" + secrets.token_hex(4)
    handle = f"/org/freedesktop/portal/desktop/request/{sender}/{token}"
    rule = MatchRule(type="signal", interface="org.freedesktop.portal.Request", member="Response", path=handle)
    c.send_and_get_reply(message_bus.AddMatch(rule))
    opts = {"handle_token": ("s", token), "reason": ("s", "Kimai Tray — test portalu (bez autostartu)"),
            "autostart": ("b", False)}
    with c.filter(rule) as q:
        reply = c.send_and_get_reply(new_method_call(bg, "RequestBackground", "sa{sv}", ("", opts)))
        print("RequestBackground ->", reply.header.message_type.name, reply.body)
        try:
            resp = c.recv_until_filtered(q, timeout=30)
            print("Response ->", resp.body)
        except TimeoutError:
            print("Response -> brak (30 s)")
    r = c.send_and_get_reply(new_method_call(bg, "SetStatus", "a{sv}", ({"message": ("s", "Timer: 1:22 — Moduł rezerwacji")},)))
    print("SetStatus ->", r.header.message_type.name, r.body)
