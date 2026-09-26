"""Kimai entities as the app needs them, parsed defensively from API payloads."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self


def _ref(value: Any) -> tuple[int | None, dict[str, Any]]:
    """Kimai returns related objects either expanded or as a bare id, depending on the endpoint."""
    if isinstance(value, dict):
        return value.get("id"), value
    return value, {}


def _preference(data: dict[str, Any], name: str) -> str:
    """Older Kimai keeps some account settings only in the `preferences` list.

    "" means the server did not say — never guess UTC: a wrong zone shifts every entry.
    """
    for item in data.get("preferences") or []:
        if isinstance(item, dict) and item.get("name") == name and item.get("value"):
            return str(item["value"])
    return ""


def _flag(value: Any) -> bool:
    """A missing flag means yes, as in Kimai: only an explicit false turns billable off."""
    return value is not False


@dataclass(frozen=True)
class User:
    id: int
    username: str
    alias: str | None
    language: str
    timezone: str
    first_weekday: str = "monday"  # Kimai profile setting; weeks may start on Sunday

    @property
    def display_name(self) -> str:
        return self.alias or self.username

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        return cls(
            id=data["id"],
            username=data.get("username") or "",
            alias=data.get("alias") or None,
            language=data.get("language") or "en",
            timezone=data.get("timezone") or _preference(data, "timezone"),
            first_weekday=_preference(data, "first_weekday").lower() or "monday",
        )


@dataclass(frozen=True)
class Customer:
    id: int
    name: str
    billable: bool

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        return cls(id=data["id"], name=data.get("name") or "", billable=_flag(data.get("billable")))


@dataclass(frozen=True)
class Project:
    id: int
    name: str
    customer_id: int | None
    customer_name: str
    color: str | None
    billable: bool

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        customer_id, customer = _ref(data.get("customer"))
        return cls(
            id=data["id"],
            name=data.get("name") or "",
            customer_id=customer_id,
            customer_name=data.get("parentTitle") or customer.get("name") or "-",
            color=data.get("color") or None,
            billable=_flag(data.get("billable")),
        )


@dataclass(frozen=True)
class Activity:
    id: int
    name: str
    billable: bool
    project_id: int | None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        project_id, _ = _ref(data.get("project"))
        return cls(
            id=data["id"],
            name=data.get("name") or "",
            billable=_flag(data.get("billable")),
            project_id=project_id,
        )


@dataclass(frozen=True)
class Entry:
    id: int
    begin: datetime
    end: datetime | None
    duration: int
    description: str
    billable: bool
    project_id: int | None
    project_name: str | None
    project_color: str | None
    activity_id: int | None
    activity_name: str | None
    user_language: str | None
    exported: bool = False  # exported (e.g. invoiced) entries are locked: Kimai answers 403

    @property
    def running(self) -> bool:
        return self.end is None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        project_id, project = _ref(data.get("project"))
        activity_id, activity = _ref(data.get("activity"))
        _, user = _ref(data.get("user"))
        end = data.get("end")
        return cls(
            id=data["id"],
            begin=datetime.fromisoformat(data["begin"]),
            end=datetime.fromisoformat(end) if end else None,
            duration=int(data.get("duration") or 0),
            description=data.get("description") or "",
            billable=_flag(data.get("billable")),
            project_id=project_id,
            project_name=project.get("name"),
            project_color=project.get("color") or None,
            activity_id=activity_id,
            activity_name=activity.get("name"),
            user_language=user.get("language"),
            exported=data.get("exported") is True,
        )


@dataclass(frozen=True)
class EntryDetails:
    """Everything Kimai tells about one entry (`GET /api/timesheets/{id}`), for the edit window.

    Rates are left out on purpose: Kimai sends them to accounts that may see them, but offers them in
    its edit form only to those that may change them (edit_rate), which the API does not tell.
    Meta fields are the custom fields the server keeps for this entry, whatever they are.
    """

    id: int
    begin: datetime
    end: datetime | None
    project_id: int | None
    activity_id: int | None
    description: str
    tags: tuple[str, ...]
    billable: bool
    exported: bool
    break_seconds: int
    meta: tuple[tuple[str, str], ...]

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        project_id, _ = _ref(data.get("project"))
        activity_id, _ = _ref(data.get("activity"))
        end = data.get("end")
        tags = data.get("tags") or []
        meta = data.get("metaFields") or []
        return cls(
            id=data["id"],
            begin=datetime.fromisoformat(data["begin"]),
            end=datetime.fromisoformat(end) if end else None,
            project_id=project_id,
            activity_id=activity_id,
            description=data.get("description") or "",
            tags=tuple(str(tag.get("name", "") if isinstance(tag, dict) else tag) for tag in tags),
            billable=_flag(data.get("billable")),
            exported=data.get("exported") is True,
            break_seconds=int(data.get("break") or 0),
            meta=tuple(
                (str(field.get("name", "")), "" if field.get("value") is None else str(field.get("value")))
                for field in meta
                if isinstance(field, dict) and field.get("name")
            ),
        )


@dataclass(frozen=True)
class Tag:
    """A tag to choose in the edit window; `color` is Kimai's "color-safe" (always set)."""

    name: str
    color: str

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        return cls(name=str(data["name"]), color=str(data.get("color-safe") or data.get("color") or ""))
