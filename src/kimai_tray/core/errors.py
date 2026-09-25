"""Errors raised by the Kimai client and the tracker, and their user-facing text."""

from __future__ import annotations

import json
from collections.abc import Callable
from enum import StrEnum

import httpx


class ErrorKind(StrEnum):
    CONNECTION = "connection"
    TIMEOUT = "timeout"
    TLS = "tls"
    AUTH = "auth"  # 401: bad, revoked or expired token
    FORBIDDEN = "forbidden"  # 403: exported/locked or someone else's entry, missing permission
    REJECTED = "rejected"
    NOT_FOUND = "not_found"
    SERVER = "server"
    REDIRECT = "redirect"  # 3xx: Kimai lives elsewhere (http -> https, new domain)
    BAD_RESPONSE = "bad_response"  # 200 that is not Kimai JSON: captive portal, wrong URL, proxy


class ApiError(Exception):
    """Kimai could not be reached or refused a request."""

    def __init__(
        self, kind: ErrorKind, status: int, message: str = "", *, location: str | None = None
    ) -> None:
        super().__init__(message or kind.value)
        self.kind = kind
        self.status = status
        self.message = message
        self.location = location  # REDIRECT only: the Kimai base address to use instead

    @classmethod
    def from_response(cls, response: httpx.Response) -> ApiError:
        status = response.status_code
        if 300 <= status < 400 and response.headers.get("Location"):
            return cls(ErrorKind.REDIRECT, status, location=_redirect_base(response))
        if status == 401:
            return cls(ErrorKind.AUTH, status)
        if status == 403:
            # Not a token problem (verified on Kimai 2.65): the token works, the action is refused.
            return cls(ErrorKind.FORBIDDEN, status, read_error(response))
        message = read_error(response)
        if status == 400:
            return cls(ErrorKind.REJECTED, status, message)
        if status == 404:
            return cls(ErrorKind.NOT_FOUND, status, message)
        return cls(ErrorKind.SERVER, status, message)

    @classmethod
    def from_transport(cls, error: httpx.TransportError, secret: str | None = None) -> ApiError:
        """`secret` (the token) is cut out of the message: transport errors may quote headers."""
        text = str(error).replace(secret, "***") if secret else str(error)
        if isinstance(error, httpx.TimeoutException):
            return cls(ErrorKind.TIMEOUT, 0, text)
        if isinstance(error, httpx.LocalProtocolError):
            # Our own request is malformed; the only header the user controls is the token.
            return cls(ErrorKind.AUTH, 0)
        if "CERTIFICATE_VERIFY_FAILED" in text:
            return cls(ErrorKind.TLS, 0, text)
        return cls(ErrorKind.CONNECTION, 0, text)


class TrackerError(Exception):
    """A rule of the app refused an action; `key` is an i18n message key."""

    def __init__(self, key: str, **params: object) -> None:
        super().__init__(key)
        self.key = key
        self.params = params


def _redirect_base(response: httpx.Response) -> str:
    """The Kimai address the redirect points to, without the /api/... part we asked for.

    Followed automatically, the redirect would send the token once more on every poll
    (and first over plain http); naming the new address lets the user fix the setting.
    """
    location = httpx.URL(response.headers["Location"])
    try:
        location = response.request.url.join(location)
    except RuntimeError:  # response built without a request (tests)
        pass
    text = str(location.copy_with(query=None, fragment=None))
    cut = text.find("/api/")
    return (text[:cut] if cut != -1 else text).rstrip("/")


def collect_form_errors(node: object, found: list[str] | None = None) -> list[str]:
    """Kimai nests form errors per field: {errors: [...], children: {field: {...}}}."""
    found = [] if found is None else found
    if not isinstance(node, dict):
        return found
    errors = node.get("errors")
    if isinstance(errors, list):
        found.extend(str(error) for error in errors)
    elif isinstance(errors, dict):
        collect_form_errors(errors, found)
    for child in (node.get("children") or {}).values():
        collect_form_errors(child, found)
    return found


def read_error(response: httpx.Response) -> str:
    """Kimai's own explanation beats a bare status code; an HTML page is cut short."""
    text = response.text
    try:
        body = json.loads(text)
    except ValueError:
        return text[:200]
    if isinstance(body, dict):
        messages = collect_form_errors(body.get("errors"))
        if messages:
            return " ".join(messages)
        if body.get("message"):
            return str(body["message"])
    return text[:200]


def describe(error: BaseException, t: Callable[..., str]) -> str:
    """User-facing text for any error the core raises."""
    if isinstance(error, TrackerError):
        return t(error.key, **error.params)
    if not isinstance(error, ApiError):
        return str(error)
    match error.kind:
        case ErrorKind.CONNECTION | ErrorKind.TIMEOUT:
            return t("errConnection")
        case ErrorKind.TLS:
            return t("errTls")
        case ErrorKind.AUTH:
            return t("errAuth")
        case ErrorKind.REDIRECT:
            return t("errRedirect", url=error.location or "")
        case ErrorKind.FORBIDDEN:
            return t("errForbidden")
        case ErrorKind.BAD_RESPONSE:
            return t("errUnexpected")
        case ErrorKind.REJECTED if error.message:
            return t("errRejected", msg=error.message)
        case _:
            return t("errServer", code=error.status)
