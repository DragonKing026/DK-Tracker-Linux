"""The Kimai API token in the system secret store (KWallet / GNOME Keyring) via Secret Service.

Plain session, `default` collection, items found by attributes — verified on Plasma 6.7.5
(ksecretd), also from inside Flatpak with --talk-name=org.freedesktop.secrets. See ADR-0004.
The token is never logged, stored elsewhere or put into exception messages.
"""

from __future__ import annotations

from collections.abc import Callable
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
# The cached session is gone, e.g. after ksecretd / gnome-keyring restarted.
_STALE_SESSION = {"org.freedesktop.Secret.Error.NoSession", "org.freedesktop.DBus.Error.UnknownObject"}


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
        (secrets,) = self._with_session(
            lambda session: self._call(_ROOT, _SVC, "GetSecrets", "aoo", (items[:1], session))
        )
        value = secrets[items[0]][2]
        return bytes(value).decode("utf-8")

    def set(self, url: str, token: str) -> None:
        collection = self._collection()
        address = _normalize(url)
        properties = {
            "org.freedesktop.Secret.Item.Label": ("s", f"Kimai Tray — {address}"),
            "org.freedesktop.Secret.Item.Attributes": ("a{ss}", self._attributes(url)),
        }
        value = token.strip().encode("utf-8")
        _, prompt = self._with_session(
            lambda session: self._call(
                collection,
                _COLL,
                "CreateItem",
                "a{sv}(oayays)b",
                (properties, (session, b"", value, "text/plain"), True),
            )
        )
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

    def _with_session(self, action: Callable[[str], Any]) -> Any:
        """Run a call that needs the session; reopen it once if the service forgot it."""
        try:
            return action(self._session())
        except DBusCallError as error:
            if error.name not in _STALE_SESSION:
                raise
        self._session_path = None
        try:
            return action(self._session())
        except DBusCallError as error:
            raise SecretsUnavailable(error.name) from None

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
        except OSError as error:  # includes TimeoutError: the service hangs or the bus went away
            raise SecretsUnavailable(type(error).__name__) from None
        except DBusCallError as error:
            if error.name in _UNAVAILABLE or error.name.startswith("org.freedesktop.DBus.Error.Spawn."):
                raise SecretsUnavailable(error.name) from None
            if error.name.endswith(".IsLocked"):
                raise SecretsLocked(error.name) from None
            raise


def _normalize(url: str) -> str:
    return url.strip().rstrip("/")
