"""Public holidays of the country chosen in the settings (task 0088, ADR-0009).

Fetched from Nager.Date only when the user asks (a country chosen, the ↻ button), kept in
`holidays.json` next to the app state and overwritten as a whole by each successful fetch. The
summaries and the calendar get a plain `{day: name}` mapping — nothing here is needed to count.

Integration and quirks: docs/integracje/nager-date.md.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

import httpx

from .errors import ApiError, ErrorKind

BASE_URL = "https://date.nager.at"
YEARS_BEFORE, YEARS_AFTER = 1, 1  # the year before, this one and the next
SEPARATOR = " · "  # two holidays of one day, in one name
STAMP = "%Y-%m-%d %H:%M"


@dataclass(frozen=True)
class Holiday:
    day: date
    local_name: str
    name: str  # English, as Nager.Date gives it

    def shown(self, language: str) -> str:
        """English interface: the English name; any other: the country's own."""
        return (self.name if language == "en" else self.local_name) or self.name or self.local_name


@dataclass(frozen=True)
class HolidayData:
    """What was last fetched: for which country, when (local time, "RRRR-MM-DD GG:MM") and the days."""

    country: str = ""
    synced: str = ""
    holidays: tuple[Holiday, ...] = ()

    def names(self, language: str, country: str | None = None) -> dict[date, str]:
        """The days' names; with `country` given, data of another country counts for nothing."""
        if country is not None and country != self.country:
            return {}
        return {holiday.day: holiday.shown(language) for holiday in self.holidays}


def parse_year(payload: Any) -> list[Holiday]:
    """A year's answer: only the nationwide public holidays (`global` and "Public" in `types`)."""
    if not isinstance(payload, list):
        raise _bad()
    found: list[Holiday] = []
    for item in payload:
        try:
            if item["global"] is not True or "Public" not in item["types"]:
                continue
            day = date.fromisoformat(item["date"])
            found.append(Holiday(day, str(item["localName"]), str(item["name"])))
        except (KeyError, TypeError, ValueError):
            raise _bad() from None
    return found


def merge_days(holidays: list[Holiday]) -> tuple[Holiday, ...]:
    """Sorted by day; two holidays of one day become one, their names joined."""
    by_day: dict[date, list[Holiday]] = {}
    for holiday in holidays:
        by_day.setdefault(holiday.day, []).append(holiday)
    merged = []
    for day in sorted(by_day):
        same = by_day[day]
        local = _join(h.local_name for h in same)
        english = _join(h.name for h in same)
        merged.append(Holiday(day, local, english))
    return tuple(merged)


def _join(names: Any) -> str:
    unique = list(dict.fromkeys(name for name in names if name))
    return SEPARATOR.join(unique)


def describe_error(error: BaseException, t: Callable[..., str]) -> str:
    """Why the fetch failed, in words that name Nager.Date, not Kimai."""
    if isinstance(error, ApiError):
        match error.kind:
            case ErrorKind.CONNECTION | ErrorKind.TIMEOUT | ErrorKind.TLS:
                return t("holErrConnection")
            case ErrorKind.NOT_FOUND:
                return t("holErrCountry")
            case ErrorKind.BAD_RESPONSE:
                return t("holErrUnexpected")
            case _:
                return t("holErrServer", code=error.status)
    return str(error)


def _bad() -> ApiError:
    return ApiError(ErrorKind.BAD_RESPONSE, 200, "unexpected response")


# -- the file --------------------------------------------------------------------------------


def load_holidays(path: Path) -> HolidayData:
    """Nothing for a missing or broken file (a hand-edited one included)."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        holidays = tuple(
            Holiday(date.fromisoformat(item["date"]), str(item["localName"]), str(item["name"]))
            for item in data["holidays"]
        )
        return HolidayData(str(data["country"]), str(data["synced"]), holidays)
    except (OSError, ValueError, KeyError, TypeError):
        return HolidayData()


def save_holidays(data: HolidayData, path: Path) -> None:
    """Whole file at once, through a temporary one: a crash never leaves half a file."""
    body = {
        "country": data.country,
        "synced": data.synced,
        "holidays": [
            {"date": h.day.isoformat(), "localName": h.local_name, "name": h.name} for h in data.holidays
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(body, indent=2, ensure_ascii=False), encoding="utf-8")
    temporary.replace(path)


# -- the service -----------------------------------------------------------------------------


class HolidayService:
    """Fetching and keeping the holidays; a client of its own (another address, no token)."""

    def __init__(
        self,
        path: Path,
        *,
        transport: httpx.BaseTransport | None = None,
        timeout: float = 10.0,
    ) -> None:
        self._path = path
        self._transport = transport
        self._timeout = timeout

    def load(self) -> HolidayData:
        return load_holidays(self._path)

    def clear(self) -> None:
        """Country "none": the saved holidays go."""
        self._path.unlink(missing_ok=True)

    def sync(self, country: str, now: datetime) -> HolidayData:
        """Fetch the three years and replace what was kept. Any failure raises ApiError and
        leaves the file as it was."""
        year = now.astimezone().year
        found: list[Holiday] = []
        with httpx.Client(
            base_url=BASE_URL,
            headers={"Accept": "application/json"},
            timeout=self._timeout,
            transport=self._transport,
        ) as http:
            for each in range(year - YEARS_BEFORE, year + YEARS_AFTER + 1):
                found += parse_year(self._get(http, f"/api/v3/PublicHolidays/{each}/{country}"))
        data = HolidayData(country, now.astimezone().strftime(STAMP), merge_days(found))
        save_holidays(data, self._path)
        return data

    @staticmethod
    def _get(http: httpx.Client, path: str) -> Any:
        try:
            response = http.get(path)
        except httpx.TransportError as error:
            raise ApiError.from_transport(error) from None
        if not response.is_success:
            raise ApiError.from_response(response)
        try:
            return response.json()
        except ValueError:
            raise _bad() from None
