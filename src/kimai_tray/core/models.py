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
            timezone=data.get("timezone") or "UTC",
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
        )
