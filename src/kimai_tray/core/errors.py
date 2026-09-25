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
    AUTH = "auth"
    REJECTED = "rejected"
    NOT_FOUND = "not_found"
    SERVER = "server"
    BAD_RESPONSE = "bad_response"  # 200 that is not Kimai JSON: captive portal, wrong URL, proxy


class ApiError(Exception):
    """Kimai could not be reached or refused a request."""

    def __init__(self, kind: ErrorKind, status: int, message: str = "") -> None:
        super().__init__(message or kind.value)
        self.kind = kind
        self.status = status
        self.message = message

    @classmethod
    def from_response(cls, response: httpx.Response) -> ApiError:
        status = response.status_code
        if status in (401, 403):
            return cls(ErrorKind.AUTH, status)
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
        case ErrorKind.BAD_RESPONSE:
            return t("errUnexpected")
        case ErrorKind.REJECTED if error.message:
            return t("errRejected", msg=error.message)
        case _:
            return t("errServer", code=error.status)
