---
noteId: "2e15896562da4d04ac0375d0fffce4c6"
tytul: "Plan 2: Integracje desktopowe (desktop)"
tags: [plan, implementacja, desktop, dbus]
status: wykonany
utworzono: 2026-09-25 20:47
zaktualizowano: 2026-09-25 21:48
---

# Plan 2: Integracje desktopowe (desktop) — plan implementacji

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Zbudować warstwę `kimai_tray.desktop` — token w magazynie sekretów systemu (KWallet / GNOME Keyring), powiadomienia z przyciskami przez portal i autostart przez portal — na `jeepney`, bez Qt.

**Architecture:** Mały moduł `desktop/bus.py` (wywołania D-Bus z rozpoznaniem błędów, oczekiwanie na sygnały, wzorzec Request/Response portali) i trzy usługi na nim: `secrets.py`, `notifications.py`, `autostart.py`. Tekst powiadomień renderuje czysta funkcja w rdzeniu (`core/notification_policy.render`). Testy jednostkowe na fałszywej szynie (`FakeBus`), testy `desktop` na prawdziwej sesji.

**Tech Stack:** Python ≥ 3.13, jeepney 0.9 (czysty Python), pytest.

**Spec:** [docs/specyfikacja/2026-09-25-kimai-tray-1.0.md](../specyfikacja/2026-09-25-kimai-tray-1.0.md) (sekcje 7–9), decyzje [ADR-0004](../decyzje/0004-architektura-rdzen-python-ui-qt.md), fakty: [rozpoznanie API](../../TODO/ZROBIONE/0021-plan2-rozpoznanie-api-desktop/notatki/rozpoznanie.md).

## Global Constraints

- Pracujemy bezpośrednio na `main` (jeden autor), małe commity po polsku z linią `Co-Authored-By`.
- `src/kimai_tray/desktop/` nie importuje `PySide6` (pilnuje `tests/test_architektura.py`); `core/` nie importuje `jeepney`.
- Nowa zależność runtime: `jeepney>=0.9,<1`.
- Token nigdy w wyjątkach, logach ani plikach; atrybuty sekretu: `application=pl.websystems.KimaiTray`, `url=<adres bez końcowego />`.
- Sekrety: sesja `plain`, kolekcja alias `default`; brak usługi / odmowa dostępu → `SecretsUnavailable`; odrzucony prompt → `SecretsLocked`.
- Powiadomienia: portal `org.freedesktop.portal.Notification` (wersja 1 na Plasmie 6.7.5); numer wpisu z identyfikatora `long-timer-<id>`, nie z parametru przycisku (portal dokleja tam `activation-token`).
- Autostart: portal `org.freedesktop.portal.Background` (wersja 2); `SetStatus` poza piaskownicą zwraca błąd — ignorujemy (`False`), komunikat ≤ 96 znaków.
- Połączenie `SessionBus` nie jest bezpieczne wątkowo — jedno na wątek (Plan 3 tworzy osobne dla workerów).
- Przed commitem: `.venv/bin/ruff format . && .venv/bin/ruff check . && .venv/bin/pytest`.

## Review Focus

1. **Brak usługi sekretów / odmowa z piaskownicy** (Flatpak bez `--talk-name=org.freedesktop.secrets`) — czytelne `SecretsUnavailable`, nie surowy błąd D-Bus. Test: zadanie 2 (`test_missing_service_is_unavailable`).
2. **Zablokowany portfel i odrzucony prompt** — `SecretsLocked`, bez zawieszenia i bez tokenu w komunikacie. Test: zadanie 2 (`test_dismissed_unlock_prompt_is_locked`).
3. **Wiele wpisów o tych samych atrybutach** (po ręcznej edycji w KWallet) — odczyt bierze pierwszy, usunięcie kasuje wszystkie. Test: zadanie 2 (`test_delete_removes_every_match`).
4. **Bardzo długi status w tle** (> 96 znaków) — przycięty z wielokropkiem, nie odrzucony przez portal. Test: zadanie 4 (`test_status_is_trimmed_to_96_characters`).
5. **Kliknięcie w powiadomienie bez numeru wpisu / nieznana akcja** — `entry_id=None`, bez wyjątku. Test: zadanie 3 (`test_parse_action_without_entry`).

## Struktura plików

```
pyproject.toml                                  zadanie 1 (jeepney)
src/kimai_tray/desktop/__init__.py              zadanie 1
src/kimai_tray/desktop/bus.py                   zadanie 1   SessionBus, DBusCallError, portal_request
tests/desktop/__init__.py, fakes.py             zadanie 1   FakeBus
tests/desktop/test_bus.py                       zadanie 1
src/kimai_tray/desktop/secrets.py               zadanie 2   SecretServiceStore
tests/desktop/test_secrets.py                   zadanie 2
src/kimai_tray/core/notification_policy.py      zadanie 3   render(), entry_id_from()
src/kimai_tray/desktop/notifications.py         zadanie 3   PortalNotifier
tests/core/test_notification_render.py, tests/desktop/test_notifications.py   zadanie 3
src/kimai_tray/desktop/autostart.py             zadanie 4   BackgroundPortal
tests/desktop/test_autostart.py                 zadanie 4
tests/desktop/test_na_zywo.py                   zadanie 5   testy `desktop` na prawdziwej sesji
```

---

### Task 1: Szyna D-Bus (`desktop/bus.py`)

**Files:**
- Modify: `pyproject.toml` (zależność `jeepney`)
- Create: `src/kimai_tray/desktop/__init__.py`, `src/kimai_tray/desktop/bus.py`
- Create: `tests/desktop/__init__.py`, `tests/desktop/fakes.py`, `tests/desktop/test_bus.py`

**Interfaces:**
- Consumes: `jeepney`.
- Produces:
  - `class DBusCallError(Exception)` — pola `name: str`, `message: str`
  - `class PortalError(Exception)` — pole `response: int` (1 = anulowane przez użytkownika, 2 = inny błąd)
  - `Bus` (Protocol): `unique_name: str`; `call(destination, path, interface, member, signature="", body=(), timeout=25.0) -> tuple`; `expect(path, interface, member) -> Expectation`
  - `Expectation` (Protocol): `wait(timeout: float) -> tuple` (rzuca `TimeoutError`), `close() -> None`
  - `class SessionBus` (implementacja `Bus` na jeepney) + `close()`
  - `PORTAL = "org.freedesktop.portal.Desktop"`, `PORTAL_PATH = "/org/freedesktop/portal/desktop"`
  - `portal_request(bus, interface, member, signature, build_body: Callable[[str], tuple], timeout=120.0) -> dict[str, Any]`
  - `tests/desktop/fakes.py`: `FakeBus` (`on(path, interface, member, reply)`, `emit(path, interface, member, body)`, `calls`, `closed`)

- [ ] **Step 1: Dodaj zależność** — w `pyproject.toml` zmień `dependencies = ["httpx>=0.28,<1"]` na:

```toml
dependencies = ["httpx>=0.28,<1", "jeepney>=0.9,<1"]
```

Run: `.venv/bin/pip install -e ".[dev]"` → instaluje `jeepney`.

- [ ] **Step 2: Utwórz pusty `tests/desktop/__init__.py`, a potem fałszywą szynę `tests/desktop/fakes.py`:**

```python
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
```

- [ ] **Step 3: Napisz testy (padające) `tests/desktop/test_bus.py`**

```python
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
```

- [ ] **Step 4: Uruchom — mają paść**

Run: `.venv/bin/pytest tests/desktop/test_bus.py -q`
Expected: błąd importu — `No module named 'kimai_tray.desktop'`.

- [ ] **Step 5: Zaimplementuj `src/kimai_tray/desktop/__init__.py` i `src/kimai_tray/desktop/bus.py`**

`src/kimai_tray/desktop/__init__.py`:

```python
"""Desktop integrations over D-Bus (jeepney): secrets, notifications, autostart. No Qt here."""
```

`src/kimai_tray/desktop/bus.py`:

```python
"""A small D-Bus layer over jeepney: method calls, awaited signals and the portal
Request/Response pattern. Services depend on the `Bus` protocol, so tests use a fake.

Facts behind this module: TODO/…/0021-plan2-rozpoznanie-api-desktop/notatki/rozpoznanie.md.
"""

from __future__ import annotations

import secrets
from collections import deque
from collections.abc import Callable
from typing import Any, Protocol

from jeepney import DBusAddress, HeaderFields, MatchRule, MessageType, message_bus, new_method_call
from jeepney.io.blocking import open_dbus_connection

PORTAL = "org.freedesktop.portal.Desktop"
PORTAL_PATH = "/org/freedesktop/portal/desktop"
_REQUEST = "org.freedesktop.portal.Request"


class DBusCallError(Exception):
    """The other side answered with a D-Bus error."""

    def __init__(self, name: str, message: str = "") -> None:
        super().__init__(f"{name}: {message}" if message else name)
        self.name = name
        self.message = message


class PortalError(Exception):
    """A portal request ended without success (1 = cancelled by the user, 2 = other)."""

    def __init__(self, response: int) -> None:
        super().__init__(f"portal response {response}")
        self.response = response


class Expectation(Protocol):
    def wait(self, timeout: float) -> tuple[Any, ...]: ...

    def close(self) -> None: ...


class Bus(Protocol):
    unique_name: str

    def call(
        self,
        destination: str,
        path: str,
        interface: str,
        member: str,
        signature: str = "",
        body: tuple = (),
        timeout: float = 25.0,
    ) -> tuple[Any, ...]: ...

    def expect(self, path: str, interface: str, member: str) -> Expectation: ...


class _JeepneyExpectation:
    def __init__(self, connection: Any, rule: MatchRule) -> None:
        self._connection = connection
        self._rule = rule
        # Several signals may arrive between two waits (e.g. notification clicks).
        self._filter = connection.filter(rule, queue=deque(maxlen=64))
        self._queue = self._filter.__enter__()

    def wait(self, timeout: float) -> tuple[Any, ...]:
        return self._connection.recv_until_filtered(self._queue, timeout=timeout).body

    def close(self) -> None:
        self._filter.__exit__(None, None, None)
        try:
            self._connection.send_and_get_reply(message_bus.RemoveMatch(self._rule), timeout=5)
        except Exception:  # noqa: BLE001 - the connection may already be closing
            pass


class SessionBus:
    """One blocking session-bus connection. Not thread-safe: use one per thread."""

    def __init__(self) -> None:
        self._connection = open_dbus_connection(bus="SESSION")
        self.unique_name: str = self._connection.unique_name

    def close(self) -> None:
        self._connection.close()

    def call(
        self,
        destination: str,
        path: str,
        interface: str,
        member: str,
        signature: str = "",
        body: tuple = (),
        timeout: float = 25.0,
    ) -> tuple[Any, ...]:
        address = DBusAddress(path, bus_name=destination, interface=interface)
        reply = self._connection.send_and_get_reply(
            new_method_call(address, member, signature or None, body), timeout=timeout
        )
        if reply.header.message_type is MessageType.error:
            name = reply.header.fields.get(HeaderFields.error_name, "org.freedesktop.DBus.Error.Failed")
            text = reply.body[0] if reply.body and isinstance(reply.body[0], str) else ""
            raise DBusCallError(name, text)
        return reply.body

    def expect(self, path: str, interface: str, member: str) -> Expectation:
        rule = MatchRule(type="signal", path=path, interface=interface, member=member)
        self._connection.send_and_get_reply(message_bus.AddMatch(rule), timeout=5)
        return _JeepneyExpectation(self._connection, rule)


def portal_request(
    bus: Bus,
    interface: str,
    member: str,
    signature: str,
    build_body: Callable[[str], tuple],
    timeout: float = 120.0,
) -> dict[str, Any]:
    """Call a portal method that answers later with Request.Response.

    The Response arrives on a path derived from our unique name and a token we choose,
    so we subscribe to it *before* calling — otherwise a fast backend could answer first.
    """
    token = "kimai_" + secrets.token_hex(6)
    sender = bus.unique_name.lstrip(":").replace(".", "_")
    expectation = bus.expect(f"{PORTAL_PATH}/request/{sender}/{token}", _REQUEST, "Response")
    try:
        bus.call(PORTAL, PORTAL_PATH, interface, member, signature, build_body(token))
        code, results = expectation.wait(timeout)
    finally:
        expectation.close()
    if code != 0:
        raise PortalError(code)
    return {key: variant[1] for key, variant in results.items()}  # jeepney variants are (signature, value)
```

- [ ] **Step 6: Uruchom — mają przejść**

Run: `.venv/bin/pytest tests/desktop/test_bus.py -q && .venv/bin/pytest -q`
Expected: 5 PASS w `test_bus.py`; całość zielona (test architektury obejmuje teraz `desktop/`).

- [ ] **Step 7: Commit**

```bash
.venv/bin/ruff format . && .venv/bin/ruff check .
git add pyproject.toml src/kimai_tray/desktop tests/desktop
git commit -m "feat(desktop): szyna D-Bus na jeepney i wzorzec Request/Response portali"
```

---

### Task 2: Token w magazynie sekretów (`desktop/secrets.py`)

**Files:**
- Create: `src/kimai_tray/desktop/secrets.py`
- Test: `tests/desktop/test_secrets.py`
- Modify: `docs/integracje/jeepney.md`, `docs/integracje/secret-service.md` (sekcje „Gdzie w kodzie”)

**Interfaces:**
- Consumes: `Bus`, `DBusCallError` (zadanie 1).
- Produces: `APP_ID = "pl.websystems.KimaiTray"`; `class SecretsUnavailable(Exception)`, `class SecretsLocked(Exception)`; `class SecretServiceStore(bus: Bus, application: str = APP_ID, prompt_timeout: float = 300.0)` z metodami `get(url: str) -> str | None`, `set(url: str, token: str) -> None`, `delete(url: str) -> None`.

- [ ] **Step 1: Napisz testy (padające) `tests/desktop/test_secrets.py`**

```python
import pytest

from kimai_tray.desktop.bus import DBusCallError
from kimai_tray.desktop.secrets import SecretServiceStore, SecretsLocked, SecretsUnavailable

from .fakes import FakeBus

ROOT = "/org/freedesktop/secrets"
SVC = "org.freedesktop.Secret.Service"
COLL = "org.freedesktop.Secret.Collection"
ITEM = "org.freedesktop.Secret.Item"
PROMPT = "org.freedesktop.Secret.Prompt"
PROPS = "org.freedesktop.DBus.Properties"
COLLECTION = "/org/freedesktop/secrets/collection/kdewallet"
SESSION = "/org/freedesktop/secrets/session/1"


def wallet(*, items=("/item/1",), locked_items=(), locked_collection=False, secret=b"kimai-token"):
    bus = FakeBus()
    bus.on(ROOT, SVC, "OpenSession", (("s", ""), SESSION))
    bus.on(ROOT, SVC, "ReadAlias", (COLLECTION,))
    bus.on(COLLECTION, PROPS, "Get", (("b", locked_collection),))
    bus.on(ROOT, SVC, "SearchItems", (list(items), list(locked_items)))
    bus.on(ROOT, SVC, "GetSecrets", lambda body: ({path: (SESSION, b"", secret, "text/plain") for path in body[0]},))
    bus.on(COLLECTION, COLL, "CreateItem", (f"{COLLECTION}/9", "/"))
    for path in (*items, *locked_items):
        bus.on(path, ITEM, "Delete", ("/",))
    return bus


def test_set_creates_an_item_with_label_attributes_and_secret():
    bus = wallet()
    SecretServiceStore(bus).set("https://kimai.firma.pl/", "  kimai-token  ")
    create = next(call for call in bus.calls if call[3] == "CreateItem")
    properties, secret, replace = create[5]
    assert properties["org.freedesktop.Secret.Item.Label"] == ("s", "Kimai Tray — https://kimai.firma.pl")
    assert properties["org.freedesktop.Secret.Item.Attributes"] == (
        "a{ss}",
        {"application": "pl.websystems.KimaiTray", "url": "https://kimai.firma.pl"},
    )
    assert secret == (SESSION, b"", b"kimai-token", "text/plain")
    assert replace is True
    assert create[4] == "a{sv}(oayays)b"


def test_get_returns_the_token_or_none():
    assert SecretServiceStore(wallet()).get("https://kimai.firma.pl") == "kimai-token"
    assert SecretServiceStore(wallet(items=())).get("https://kimai.firma.pl") is None


def test_session_is_opened_once():
    bus = wallet()
    store = SecretServiceStore(bus)
    store.get("https://a.test")
    store.get("https://a.test")
    assert bus.members().count("OpenSession") == 1


def test_delete_removes_every_match():
    bus = wallet(items=("/item/1", "/item/2"))
    SecretServiceStore(bus).delete("https://kimai.firma.pl")
    assert [call[1] for call in bus.calls if call[3] == "Delete"] == ["/item/1", "/item/2"]


def test_locked_item_is_unlocked_through_the_prompt():
    bus = wallet(items=(), locked_items=("/item/7",))
    bus.on(ROOT, SVC, "Unlock", ([], "/prompt/1"))
    bus.on("/prompt/1", PROMPT, "Prompt", ())
    bus.emit("/prompt/1", PROMPT, "Completed", (False, ("ao", ["/item/7"])))
    assert SecretServiceStore(bus).get("https://kimai.firma.pl") == "kimai-token"
    assert "Prompt" in bus.members()


def test_dismissed_unlock_prompt_is_locked():
    bus = wallet(items=(), locked_items=("/item/7",))
    bus.on(ROOT, SVC, "Unlock", ([], "/prompt/1"))
    bus.on("/prompt/1", PROMPT, "Prompt", ())
    bus.emit("/prompt/1", PROMPT, "Completed", (True, ("s", "")))
    with pytest.raises(SecretsLocked) as caught:
        SecretServiceStore(bus).get("https://kimai.firma.pl")
    assert "kimai-token" not in str(caught.value)


def test_locked_collection_is_unlocked_before_writing():
    bus = wallet(locked_collection=True)
    bus.on(ROOT, SVC, "Unlock", ([COLLECTION], "/"))
    SecretServiceStore(bus).set("https://kimai.firma.pl", "t")
    assert bus.members().index("Unlock") < bus.members().index("CreateItem")


@pytest.mark.parametrize(
    "name",
    ["org.freedesktop.DBus.Error.ServiceUnknown", "org.freedesktop.DBus.Error.AccessDenied",
     "org.freedesktop.DBus.Error.NameHasNoOwner"],
)
def test_missing_service_is_unavailable(name):
    bus = FakeBus()
    bus.on(ROOT, SVC, "SearchItems", DBusCallError(name, "sandbox"))
    bus.on(ROOT, SVC, "OpenSession", DBusCallError(name, "sandbox"))
    with pytest.raises(SecretsUnavailable):
        SecretServiceStore(bus).get("https://kimai.firma.pl")


def test_no_default_collection_is_unavailable():
    bus = wallet()
    bus.on(ROOT, SVC, "ReadAlias", ("/",))
    with pytest.raises(SecretsUnavailable):
        SecretServiceStore(bus).set("https://kimai.firma.pl", "t")


def test_token_never_appears_in_errors():
    bus = wallet()
    bus.on(COLLECTION, COLL, "CreateItem", DBusCallError("org.freedesktop.DBus.Error.AccessDenied", "denied"))
    with pytest.raises(SecretsUnavailable) as caught:
        SecretServiceStore(bus).set("https://kimai.firma.pl", "super-secret-token")
    assert "super-secret-token" not in str(caught.value)
```

- [ ] **Step 2: Uruchom — mają paść**

Run: `.venv/bin/pytest tests/desktop/test_secrets.py -q`
Expected: błąd importu — `No module named 'kimai_tray.desktop.secrets'`.

- [ ] **Step 3: Zaimplementuj `src/kimai_tray/desktop/secrets.py`**

```python
"""The Kimai API token in the system secret store (KWallet / GNOME Keyring) via Secret Service.

Plain session, `default` collection, items found by attributes — verified on Plasma 6.7.5
(ksecretd), also from inside Flatpak with --talk-name=org.freedesktop.secrets. See ADR-0004.
The token is never logged, stored elsewhere or put into exception messages.
"""

from __future__ import annotations

from typing import Any

from .bus import Bus, DBusCallError

APP_ID = "pl.websystems.KimaiTray"
_SERVICE = "org.freedesktop.secrets"
_ROOT = "/org/freedesktop/secrets"
_SVC = "org.freedesktop.Secret.Service"
_COLL = "org.freedesktop.Secret.Collection"
_ITEM = "org.freedesktop.Secret.Item"
_PROMPT = "org.freedesktop.Secret.Prompt"
_PROPS = "org.freedesktop.DBus.Properties"
_NO_PROMPT = "/"
_UNAVAILABLE = {
    "org.freedesktop.DBus.Error.ServiceUnknown",
    "org.freedesktop.DBus.Error.NameHasNoOwner",
    "org.freedesktop.DBus.Error.AccessDenied",
    "org.freedesktop.DBus.Error.NoReply",
}


class SecretsUnavailable(Exception):
    """No secret service on the session bus, or the sandbox may not talk to it."""


class SecretsLocked(Exception):
    """The wallet stayed locked: the user dismissed the unlock prompt."""


class SecretServiceStore:
    def __init__(self, bus: Bus, application: str = APP_ID, prompt_timeout: float = 300.0) -> None:
        self._bus = bus
        self._application = application
        self._prompt_timeout = prompt_timeout
        self._session_path: str | None = None

    # -- public -----------------------------------------------------------------

    def get(self, url: str) -> str | None:
        items = self._find(url)
        if not items:
            return None
        (secrets,) = self._call(_ROOT, _SVC, "GetSecrets", "aoo", (items[:1], self._session()))
        value = secrets[items[0]][2]
        return bytes(value).decode("utf-8")

    def set(self, url: str, token: str) -> None:
        collection = self._collection()
        address = _normalize(url)
        properties = {
            "org.freedesktop.Secret.Item.Label": ("s", f"Kimai Tray — {address}"),
            "org.freedesktop.Secret.Item.Attributes": ("a{ss}", self._attributes(url)),
        }
        secret = (self._session(), b"", token.strip().encode("utf-8"), "text/plain")
        _, prompt = self._call(collection, _COLL, "CreateItem", "a{sv}(oayays)b", (properties, secret, True))
        self._run_prompt(prompt)

    def delete(self, url: str) -> None:
        for item in self._find(url):
            (prompt,) = self._call(item, _ITEM, "Delete")
            self._run_prompt(prompt)

    # -- internals ----------------------------------------------------------------

    def _attributes(self, url: str) -> dict[str, str]:
        return {"application": self._application, "url": _normalize(url)}

    def _session(self) -> str:
        if self._session_path is None:
            _, self._session_path = self._call(_ROOT, _SVC, "OpenSession", "sv", ("plain", ("s", "")))
        return self._session_path

    def _collection(self) -> str:
        (path,) = self._call(_ROOT, _SVC, "ReadAlias", "s", ("default",))
        if path == _NO_PROMPT:
            raise SecretsUnavailable("no default collection")
        ((_, locked),) = self._call(path, _PROPS, "Get", "ss", (_COLL, "Locked"))
        if locked:
            self._unlock([path])
        return path

    def _find(self, url: str) -> list[str]:
        unlocked, locked = self._call(_ROOT, _SVC, "SearchItems", "a{ss}", (self._attributes(url),))
        found = list(unlocked)
        if locked:
            found += self._unlock(list(locked))
        return found

    def _unlock(self, paths: list[str]) -> list[str]:
        unlocked, prompt = self._call(_ROOT, _SVC, "Unlock", "ao", (paths,))
        if prompt != _NO_PROMPT:
            self._run_prompt(prompt)
            return paths
        return list(unlocked)

    def _run_prompt(self, prompt: str) -> None:
        if prompt == _NO_PROMPT:
            return
        expectation = self._bus.expect(prompt, _PROMPT, "Completed")
        try:
            self._call(prompt, _PROMPT, "Prompt", "s", ("",))
            dismissed, _ = expectation.wait(self._prompt_timeout)
        except TimeoutError:
            raise SecretsLocked("unlock prompt not answered") from None
        finally:
            expectation.close()
        if dismissed:
            raise SecretsLocked("unlock prompt dismissed")

    def _call(self, path: str, interface: str, member: str, signature: str = "", body: tuple = ()) -> Any:
        try:
            return self._bus.call(_SERVICE, path, interface, member, signature, body)
        except DBusCallError as error:
            if error.name in _UNAVAILABLE:
                raise SecretsUnavailable(error.name) from None
            if error.name.endswith(".IsLocked"):
                raise SecretsLocked(error.name) from None
            raise


def _normalize(url: str) -> str:
    return url.strip().rstrip("/")
```

- [ ] **Step 4: Uruchom — mają przejść**

Run: `.venv/bin/pytest tests/desktop/test_secrets.py -q && .venv/bin/pytest -q`
Expected: 12 PASS w `test_secrets.py`; całość zielona.

- [ ] **Step 5: Dokumentacja** — w `docs/integracje/jeepney.md` i `docs/integracje/secret-service.md` dopisz przed „## Dokumentacja”:

```markdown
## Gdzie w kodzie

- [src/kimai_tray/desktop/secrets.py](../../src/kimai_tray/desktop/secrets.py) — `SecretServiceStore` (get/set/delete, odblokowanie przez prompt).
- [src/kimai_tray/desktop/bus.py](../../src/kimai_tray/desktop/bus.py) — szyna D-Bus na jeepney.
- Testy: [tests/desktop/test_secrets.py](../../tests/desktop/test_secrets.py) (FakeBus).
```

Run: `python3 .claude/skills/sprawdz-linki/linki.py sprawdz`

- [ ] **Step 6: Commit**

```bash
.venv/bin/ruff format . && .venv/bin/ruff check . && .venv/bin/pytest
git add src/kimai_tray/desktop/secrets.py tests/desktop/test_secrets.py docs/integracje/jeepney.md docs/integracje/secret-service.md
git commit -m "feat(desktop): token w magazynie sekretów przez Secret Service"
```

---

### Task 3: Powiadomienia — tekst w rdzeniu, wysyłka przez portal

**Files:**
- Modify: `src/kimai_tray/core/notification_policy.py` (dopisz `RenderedNotification`, `render`, `entry_id_from`)
- Create: `src/kimai_tray/desktop/notifications.py`
- Test: `tests/core/test_notification_render.py`, `tests/desktop/test_notifications.py`

**Interfaces:**
- Consumes: `Notification`, `LONG_TIMER` (Plan 1); `Bus`, `PORTAL`, `PORTAL_PATH`.
- Produces:
  - core: `@dataclass(frozen=True) RenderedNotification(id: str, title: str, body: str, buttons: tuple[tuple[str, str], ...])`; `render(notification: Notification, t: Callable[..., str]) -> RenderedNotification`; `entry_id_from(notification_id: str) -> int | None`; `ACTION_LABELS: dict[str, str]`
  - desktop: `@dataclass(frozen=True) NotificationAction(notification_id: str, action: str, entry_id: int | None)`; `class PortalNotifier(bus)` z `show(rendered) -> None`, `withdraw(notification_id) -> None`, `listen() -> Expectation`, `staticmethod parse(body: tuple) -> NotificationAction`

- [ ] **Step 1: Napisz testy (padające)**

`tests/core/test_notification_render.py`:

```python
from kimai_tray.core.i18n import Translator
from kimai_tray.core.notification_policy import Notification, entry_id_from, render


def test_render_long_timer_in_polish():
    note = Notification("long-timer-7", "notifLongTimerTitle", "notifLongTimerBody",
                        {"time": "8:00", "project": "Moduł rezerwacji", "description": "Formularz"},
                        ("stop", "keep"), entry_id=7)
    rendered = render(note, Translator("pl"))
    assert rendered.id == "long-timer-7"
    assert rendered.title == "Timer działa od 8:00"
    assert rendered.body == "Moduł rezerwacji — Formularz"
    assert rendered.buttons == (("Zatrzymaj", "stop"), ("Działa dalej", "keep"))


def test_render_without_body_and_buttons_in_english():
    rendered = render(Notification("connection", "notifConnectionRestored"), Translator("en"))
    assert (rendered.title, rendered.body, rendered.buttons) == ("Connection to Kimai restored", "", ())


def test_entry_id_from_notification_id():
    assert entry_id_from("long-timer-123") == 123
    assert entry_id_from("connection") is None
    assert entry_id_from("long-timer-abc") is None

```

`tests/desktop/test_notifications.py`:

```python
from kimai_tray.core.notification_policy import RenderedNotification
from kimai_tray.desktop.bus import PORTAL, PORTAL_PATH
from kimai_tray.desktop.notifications import NotificationAction, PortalNotifier

from .fakes import FakeBus

IFACE = "org.freedesktop.portal.Notification"


def test_show_sends_title_body_and_buttons():
    bus = FakeBus()
    bus.on(PORTAL_PATH, IFACE, "AddNotification", ())
    PortalNotifier(bus).show(RenderedNotification("long-timer-7", "Timer działa od 8:00", "Projekt — opis",
                                                  (("Zatrzymaj", "stop"), ("Działa dalej", "keep"))))
    destination, _, _, member, signature, body = bus.calls[0]
    assert (destination, member, signature) == (PORTAL, "AddNotification", "sa{sv}")
    notification_id, payload = body
    assert notification_id == "long-timer-7"
    assert payload["title"] == ("s", "Timer działa od 8:00")
    assert payload["body"] == ("s", "Projekt — opis")
    assert payload["buttons"] == ("aa{sv}", [{"label": ("s", "Zatrzymaj"), "action": ("s", "stop")},
                                             {"label": ("s", "Działa dalej"), "action": ("s", "keep")}])


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
    bus.emit(PORTAL_PATH, IFACE, "ActionInvoked", ("long-timer-7", "stop", [("a{sv}", {"activation-token": ("s", "kwin-1")})]))
    assert PortalNotifier.parse(expectation.wait(1)) == NotificationAction("long-timer-7", "stop", 7)


def test_parse_action_without_entry():
    assert PortalNotifier.parse(("connection", "settings", [])) == NotificationAction("connection", "settings", None)
```

- [ ] **Step 2: Uruchom — mają paść**

Run: `.venv/bin/pytest tests/core/test_notification_render.py tests/desktop/test_notifications.py -q`
Expected: błąd importu (`render`, `kimai_tray.desktop.notifications`).

- [ ] **Step 3: Dopisz do `src/kimai_tray/core/notification_policy.py`** (na końcu pliku; import `Callable` dodaj do importów)

```python
ACTION_LABELS = {"stop": "actionStop", "keep": "actionKeepRunning", "settings": "actionSettings"}


@dataclass(frozen=True)
class RenderedNotification:
    id: str
    title: str
    body: str
    buttons: tuple[tuple[str, str], ...]  # (label, action)


def render(notification: Notification, t: Callable[..., str]) -> RenderedNotification:
    """User-facing text of a notification in the current language."""
    return RenderedNotification(
        notification.id,
        t(notification.title_key, **notification.params),
        t(notification.body_key, **notification.params) if notification.body_key else "",
        tuple((t(ACTION_LABELS[action]), action) for action in notification.actions),
    )


def entry_id_from(notification_id: str) -> int | None:
    """The portal returns our id with a click; long-timer ids carry the entry number."""
    prefix = f"{LONG_TIMER}-"
    if notification_id.startswith(prefix) and notification_id[len(prefix):].isdigit():
        return int(notification_id[len(prefix):])
    return None
```

Import na górze pliku: `from collections.abc import Callable`.

- [ ] **Step 4: Utwórz `src/kimai_tray/desktop/notifications.py`**

```python
"""Notifications through xdg-desktop-portal (org.freedesktop.portal.Notification, v1 on Plasma 6.7).

Clicks come back as ActionInvoked(id, action, parameter). The parameter carries platform data
(an activation token) rather than our button target, so the entry is identified by the
notification id ("long-timer-<entry id>") — verified on the host and inside Flatpak.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from kimai_tray.core.notification_policy import RenderedNotification, entry_id_from

from .bus import PORTAL, PORTAL_PATH, Bus, Expectation

_INTERFACE = "org.freedesktop.portal.Notification"


@dataclass(frozen=True)
class NotificationAction:
    notification_id: str
    action: str  # "stop" | "keep" | "settings"
    entry_id: int | None


class PortalNotifier:
    def __init__(self, bus: Bus) -> None:
        self._bus = bus

    def show(self, rendered: RenderedNotification) -> None:
        payload: dict[str, Any] = {"title": ("s", rendered.title), "priority": ("s", "normal")}
        if rendered.body:
            payload["body"] = ("s", rendered.body)
        if rendered.buttons:
            payload["buttons"] = (
                "aa{sv}",
                [{"label": ("s", label), "action": ("s", action)} for label, action in rendered.buttons],
            )
        self._bus.call(PORTAL, PORTAL_PATH, _INTERFACE, "AddNotification", "sa{sv}", (rendered.id, payload))

    def withdraw(self, notification_id: str) -> None:
        self._bus.call(PORTAL, PORTAL_PATH, _INTERFACE, "RemoveNotification", "s", (notification_id,))

    def listen(self) -> Expectation:
        """Subscribe to clicks; the UI waits on it in a worker thread (Plan 3)."""
        return self._bus.expect(PORTAL_PATH, _INTERFACE, "ActionInvoked")

    @staticmethod
    def parse(body: tuple[Any, ...]) -> NotificationAction:
        notification_id, action = body[0], body[1]
        return NotificationAction(notification_id, action, entry_id_from(notification_id))
```

- [ ] **Step 5: Uruchom — mają przejść**

Run: `.venv/bin/pytest tests/core/test_notification_render.py tests/desktop/test_notifications.py -q && .venv/bin/pytest -q`
Expected: 8 PASS; całość zielona (także test kluczy i18n — `actionStop` itd. istnieją od Planu 1).

- [ ] **Step 6: Commit**

```bash
.venv/bin/ruff format . && .venv/bin/ruff check . && .venv/bin/pytest
git add src/kimai_tray/core/notification_policy.py src/kimai_tray/desktop/notifications.py tests/core/test_notification_render.py tests/desktop/test_notifications.py
git commit -m "feat(desktop): powiadomienia przez portal z przyciskami; tekst renderowany w rdzeniu"
```

---

### Task 4: Autostart i status w tle (`desktop/autostart.py`)

**Files:**
- Create: `src/kimai_tray/desktop/autostart.py`
- Test: `tests/desktop/test_autostart.py`
- Modify: `docs/integracje/xdg-portale.md` („Gdzie w kodzie”)

**Interfaces:**
- Consumes: `Bus`, `portal_request`, `PORTAL`, `PORTAL_PATH`, `DBusCallError`, `PortalError`.
- Produces: `STATUS_MAX = 96`; `@dataclass(frozen=True) BackgroundResult(background: bool, autostart: bool)`; `class BackgroundPortal(bus, timeout=120.0)` z `request(*, autostart: bool, reason: str, commandline: list[str] | None = None) -> BackgroundResult` (rzuca `PortalError`, `TimeoutError`) i `set_status(message: str) -> bool`.

- [ ] **Step 1: Napisz testy (padające) `tests/desktop/test_autostart.py`**

```python
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
    result = BackgroundPortal(bus).request(autostart=True, reason="Pomiar czasu w tle",
                                           commandline=["kimai-tray", "--hidden"])
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
    bus.on(PORTAL_PATH, IFACE, "SetStatus",
           DBusCallError("org.freedesktop.portal.Error.NotAllowed", "Only sandboxed applications can set background status"))
    assert BackgroundPortal(bus).set_status("x") is False


def test_status_is_trimmed_to_96_characters():
    bus = FakeBus()
    bus.on(PORTAL_PATH, IFACE, "SetStatus", ())
    BackgroundPortal(bus).set_status("x" * 200)
    sent = bus.calls[0][5][0]["message"][1]
    assert len(sent) == STATUS_MAX
    assert sent.endswith("…")
```

- [ ] **Step 2: Uruchom — mają paść**

Run: `.venv/bin/pytest tests/desktop/test_autostart.py -q`
Expected: błąd importu — `No module named 'kimai_tray.desktop.autostart'`.

- [ ] **Step 3: Zaimplementuj `src/kimai_tray/desktop/autostart.py`**

```python
"""Autostart and background status through xdg-desktop-portal (org.freedesktop.portal.Background v2).

Verified on Plasma 6.7.5: RequestBackground answers through Request.Response; SetStatus
works only for sandboxed apps (outside Flatpak the portal refuses — we ignore that).
"""

from __future__ import annotations

from dataclasses import dataclass

from .bus import PORTAL, PORTAL_PATH, Bus, DBusCallError, portal_request

_INTERFACE = "org.freedesktop.portal.Background"
STATUS_MAX = 96  # the portal's limit for the status message


@dataclass(frozen=True)
class BackgroundResult:
    background: bool
    autostart: bool


class BackgroundPortal:
    def __init__(self, bus: Bus, timeout: float = 120.0) -> None:
        self._bus = bus
        self._timeout = timeout

    def request(self, *, autostart: bool, reason: str, commandline: list[str] | None = None) -> BackgroundResult:
        """Ask to keep running in the background and (optionally) to start with the session."""

        def body(token: str) -> tuple:
            options = {"handle_token": ("s", token), "reason": ("s", reason), "autostart": ("b", autostart)}
            if commandline:
                options["commandline"] = ("as", commandline)
            return ("", options)

        results = portal_request(self._bus, _INTERFACE, "RequestBackground", "sa{sv}", body, self._timeout)
        return BackgroundResult(bool(results.get("background", False)), bool(results.get("autostart", False)))

    def set_status(self, message: str) -> bool:
        """Short status shown by the desktop for background apps; False when not allowed."""
        text = message if len(message) <= STATUS_MAX else message[: STATUS_MAX - 1] + "…"
        try:
            self._bus.call(PORTAL, PORTAL_PATH, _INTERFACE, "SetStatus", "a{sv}", ({"message": ("s", text)},))
        except DBusCallError:
            return False  # outside a sandbox: "Only sandboxed applications can set background status"
        return True
```

- [ ] **Step 4: Uruchom — mają przejść**

Run: `.venv/bin/pytest tests/desktop/test_autostart.py -q && .venv/bin/pytest -q`
Expected: 6 PASS; całość zielona.

- [ ] **Step 5: Dokumentacja** — w `docs/integracje/xdg-portale.md` dopisz przed „## Dokumentacja”:

```markdown
## Gdzie w kodzie

- [src/kimai_tray/desktop/notifications.py](../../src/kimai_tray/desktop/notifications.py) — `PortalNotifier` (AddNotification, RemoveNotification, ActionInvoked).
- [src/kimai_tray/desktop/autostart.py](../../src/kimai_tray/desktop/autostart.py) — `BackgroundPortal` (RequestBackground, SetStatus).
- [src/kimai_tray/desktop/bus.py](../../src/kimai_tray/desktop/bus.py) — `portal_request` (Request/Response).
```

Run: `python3 .claude/skills/sprawdz-linki/linki.py sprawdz`

- [ ] **Step 6: Commit**

```bash
.venv/bin/ruff format . && .venv/bin/ruff check . && .venv/bin/pytest
git add src/kimai_tray/desktop/autostart.py tests/desktop/test_autostart.py docs/integracje/xdg-portale.md
git commit -m "feat(desktop): autostart i status w tle przez portal Background"
```

---

### Task 5: Testy na prawdziwej sesji i komendy

**Files:**
- Create: `tests/desktop/test_na_zywo.py`
- Modify: `AGENTS.md` (sekcja „Komendy”)

**Interfaces:**
- Consumes: `SessionBus`, `SecretServiceStore`, `PortalNotifier`, `BackgroundPortal`, `render`, `Translator`.
- Produces: testy `@pytest.mark.desktop` (domyślnie pomijane).

- [ ] **Step 1: Napisz testy `tests/desktop/test_na_zywo.py`**

```python
"""Real session-bus tests (marker `desktop`): `.venv/bin/pytest -m desktop`.

They touch the user's desktop: a test item in the wallet (removed at the end), a notification
(withdrawn) and a background request with autostart=False (no autostart entry is created).
"""

import os

import pytest

from kimai_tray.core.i18n import Translator
from kimai_tray.core.notification_policy import Notification, render
from kimai_tray.desktop.autostart import BackgroundPortal
from kimai_tray.desktop.bus import SessionBus
from kimai_tray.desktop.notifications import PortalNotifier
from kimai_tray.desktop.secrets import SecretServiceStore

pytestmark = pytest.mark.desktop
URL = "https://kimai.test.invalid"


@pytest.fixture
def bus():
    if not os.environ.get("DBUS_SESSION_BUS_ADDRESS"):
        pytest.skip("no session bus")
    connection = SessionBus()
    yield connection
    connection.close()


def test_secret_round_trip(bus):
    store = SecretServiceStore(bus, application="pl.websystems.KimaiTray.TEST")
    try:
        store.set(URL, "test-token-123")
        assert store.get(URL) == "test-token-123"
    finally:
        store.delete(URL)
    assert store.get(URL) is None


def test_notification_can_be_shown_and_withdrawn(bus):
    notifier = PortalNotifier(bus)
    note = render(Notification("kimai-tray-test", "notifConnectionRestored"), Translator("pl"))
    notifier.show(note)
    notifier.withdraw(note.id)


def test_background_request_without_autostart(bus):
    result = BackgroundPortal(bus).request(autostart=False, reason="Kimai Tray — test")
    assert result.autostart is False
    assert isinstance(BackgroundPortal(bus).set_status("Kimai Tray — test"), bool)
```

- [ ] **Step 2: Uruchom testy na sesji**

Run: `.venv/bin/pytest -m desktop -v`
Expected: 3 PASS (na KDE Plasma z odblokowanym portfelem). Przy zablokowanym portfelu pojawi się okno KWallet z pytaniem o hasło.

- [ ] **Step 3: `AGENTS.md` → „Komendy”** — w bloku „Python (rdzeń)” dopisz linię:

```bash
.venv/bin/pytest -m desktop                                   # D-Bus na prawdziwej sesji (portfel, powiadomienie, portal)
```

- [ ] **Step 4: Commit**

```bash
.venv/bin/ruff format . && .venv/bin/ruff check . && .venv/bin/pytest
git add tests/desktop/test_na_zywo.py AGENTS.md
git commit -m "test(desktop): testy integracji na prawdziwej sesji D-Bus"
```

---

## Poza tym planem

- Plan 3 (UI): wątek nasłuchu kliknięć (`PortalNotifier.listen()` w osobnym połączeniu), okno ustawień z zapisem tokenu (`SecretServiceStore.set`), opcja autostartu z komendą `--hidden`, obsługa `SecretsUnavailable` / `SecretsLocked` w UI (przy braku portfela — podpowiedź, jak go założyć; [0027](../../TODO/W-TRAKCIE/0027-drobne-uwagi-z-recenzji-planu-2/todo.md)). Nasłuch kliknięć może mieć osobne połączenie — sprawdzić na żywo.
- Plan 4 (Flatpak): `--talk-name=org.freedesktop.secrets` i moduł pip `jeepney` w manifeście.
