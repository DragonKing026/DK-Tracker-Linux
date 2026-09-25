"""Thin client for the Kimai REST API (bearer token only; X-AUTH-* is deliberately unsupported).

Endpoints and quirks: docs/integracje/kimai-api.md.
"""

from __future__ import annotations

from typing import Any

import httpx

from .errors import ApiError, ErrorKind
from .models import Activity, Customer, Entry, Project, User


class KimaiClient:
    def __init__(
        self,
        url: str,
        token: str,
        *,
        transport: httpx.BaseTransport | None = None,
        timeout: float = 10.0,
    ) -> None:
        self._http = httpx.Client(
            base_url=url.strip().rstrip("/"),
            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
            timeout=timeout,
            transport=transport,
        )

    def close(self) -> None:
        self._http.close()

    def _request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        try:
            response = self._http.request(method, path, **kwargs)
        except httpx.TransportError as error:
            raise ApiError.from_transport(error) from None
        if response.is_success:
            return response
        raise ApiError.from_response(response)

    def _json(self, method: str, path: str, **kwargs: Any) -> Any:
        response = self._request(method, path, **kwargs)
        return response.json() if response.content else None

    def me(self) -> User:
        return User.from_api(self._json("GET", "/api/users/me"))

    def version(self) -> str:
        return str(self._json("GET", "/api/version")["version"])

    def projects(self) -> list[Project]:
        # Without ignoreDates the API hides projects whose start/end window has passed.
        data = self._json("GET", "/api/projects", params={"visible": "1", "ignoreDates": "1"})
        return [Project.from_api(item) for item in data]

    def customers(self) -> list[Customer]:
        return [
            Customer.from_api(item) for item in self._json("GET", "/api/customers", params={"visible": "1"})
        ]

    def activities(self, project_id: int | None = None) -> list[Activity]:
        params = {"visible": "1", "globals": "true"}
        if project_id:
            params["project"] = str(project_id)
        return [Activity.from_api(item) for item in self._json("GET", "/api/activities", params=params)]

    def active(self) -> list[Entry]:
        return [Entry.from_api(item) for item in self._json("GET", "/api/timesheets/active")]

    def latest(self, size: int = 20) -> list[Entry]:
        # Not /api/timesheets/recent: that collapses the list to one row per project + activity.
        params = {"size": str(size), "orderBy": "begin", "order": "DESC", "full": "true"}
        return [Entry.from_api(item) for item in self._json("GET", "/api/timesheets", params=params)]

    def range(self, begin: str, end: str, *, page_size: int = 500, max_pages: int = 10) -> list[Entry]:
        """Every entry starting inside the window; Kimai answers 404 past the last page."""
        collected: list[Entry] = []
        for page in range(1, max_pages + 1):
            params = {"begin": begin, "end": end, "size": str(page_size), "page": str(page)}
            try:
                response = self._request("GET", "/api/timesheets", params=params)
            except ApiError as error:
                if error.kind is ErrorKind.NOT_FOUND and page > 1:
                    break
                raise
            collected.extend(Entry.from_api(item) for item in response.json())
            if page >= int(response.headers.get("X-Total-Pages", page)):
                break
        return collected

    def start(
        self,
        *,
        project_id: int,
        activity_id: int,
        description: str,
        begin: str,
        billable: bool | None = None,
    ) -> Entry:
        body: dict[str, Any] = {
            "begin": begin,
            "project": project_id,
            "activity": activity_id,
            "description": description,
        }
        if billable is not None:  # untouched switch: Kimai derives billable itself
            body["billable"] = billable
        return Entry.from_api(self._json("POST", "/api/timesheets", json=body))

    def stop(self, entry_id: int) -> Entry:
        return Entry.from_api(self._json("PATCH", f"/api/timesheets/{entry_id}/stop"))

    def update(self, entry_id: int, changes: dict[str, object]) -> Entry:
        return Entry.from_api(self._json("PATCH", f"/api/timesheets/{entry_id}", json=changes))
