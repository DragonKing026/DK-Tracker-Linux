"""Probe: Secret Service round trip with jeepney (plain session), test item removed afterwards."""
from jeepney import DBusAddress, new_method_call, MatchRule, message_bus
from jeepney.io.blocking import open_dbus_connection

BUS = "org.freedesktop.secrets"
svc = DBusAddress("/org/freedesktop/secrets", bus_name=BUS, interface="org.freedesktop.Secret.Service")
ATTRS = {"application": "pl.websystems.KimaiTray.TEST", "url": "https://kimai.test"}

with open_dbus_connection(bus="SESSION") as c:
    call = lambda addr, m, sig, body: c.send_and_get_reply(new_method_call(addr, m, sig, body)).body
    _, session = call(svc, "OpenSession", "sv", ("plain", ("s", "")))
    (collection,) = call(svc, "ReadAlias", "s", ("default",))
    print("session", session, "collection", collection)
    coll = DBusAddress(collection, bus_name=BUS, interface="org.freedesktop.Secret.Collection")
    props = {
        "org.freedesktop.Secret.Item.Label": ("s", "Kimai Tray TEST — https://kimai.test"),
        "org.freedesktop.Secret.Item.Attributes": ("a{ss}", ATTRS),
    }
    secret = (session, b"", b"test-token-123", "text/plain")
    item, prompt = call(coll, "CreateItem", "a{sv}(oayays)b", (props, secret, True))
    print("CreateItem ->", item, "prompt:", prompt)
    unlocked, locked = call(svc, "SearchItems", "a{ss}", (ATTRS,))
    print("SearchItems -> unlocked", unlocked, "locked", locked)
    secrets = call(svc, "GetSecrets", "aoo", (unlocked, session))[0]
    print("GetSecrets ->", {k: bytes(v[2]) for k, v in secrets.items()})
    for path in unlocked:
        it = DBusAddress(path, bus_name=BUS, interface="org.freedesktop.Secret.Item")
        print("Delete ->", call(it, "Delete", "", ()))
    print("after delete:", call(svc, "SearchItems", "a{ss}", (ATTRS,)))
    # locked state of the collection
    p = DBusAddress(collection, bus_name=BUS, interface="org.freedesktop.DBus.Properties")
    print("Collection Locked =", call(p, "Get", "ss", ("org.freedesktop.Secret.Collection", "Locked")))
