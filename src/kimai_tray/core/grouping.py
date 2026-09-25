"""List shaping for the popup: entries by day (F-08), projects by customer (F-06)."""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable
from datetime import date, tzinfo

from .models import Entry, Project
from .timefmt import local_day

_COMBINING = re.compile(r"[̀-ͯ]")


def sort_key(text: str) -> str:
    """Alphabetical order a person expects: case and diacritics ignored ("Żabka" after "Hotel")."""
    return (
        _COMBINING.sub("", unicodedata.normalize("NFD", text)).replace("ł", "l").replace("Ł", "L").casefold()
    )


def group_by_day(entries: Iterable[Entry], tz: tzinfo) -> list[tuple[date, list[Entry]]]:
    """Consecutive days in the order entries arrived (newest first from the API)."""
    days: dict[date, list[Entry]] = {}
    for entry in entries:
        days.setdefault(local_day(entry.begin, tz), []).append(entry)
    return list(days.items())


def group_projects(projects: Iterable[Project]) -> list[tuple[str, list[Project]]]:
    """A flat list of 75 projects is unusable; grouped by customer it is not."""
    customers: dict[str, list[Project]] = {}
    for project in projects:
        customers.setdefault(project.customer_name, []).append(project)
    return [
        (customer, sorted(customers[customer], key=lambda p: sort_key(p.name)))
        for customer in sorted(customers, key=sort_key)
    ]


def day_total(entries: Iterable[Entry]) -> int:
    return sum(entry.duration for entry in entries)
