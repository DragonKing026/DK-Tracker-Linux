"""In-memory stand-in for KimaiClient that behaves like Kimai 2.67 where the tracker cares."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
from zoneinfo import ZoneInfo

from dk_tracker.core.errors import ApiError, ErrorKind
from dk_tracker.core.models import Activity, Customer, Entry, EntryDetails, Project, User
from dk_tracker.core.timefmt import STAMP

NOW = datetime(2026, 9, 25, 16, 4, 3, tzinfo=UTC)  # Friday, 18:04:03 in Warsaw
EXTRA_FIELDS = "This form should not contain extra fields."


def make_entry(
    entry_id,
    begin,
    end=None,
    *,
    description="Formularz rezerwacji pokoi",
    billable=True,
    project_id=1,
    activity_id=1,
    language="pl",
):
    duration = int((end - begin).total_seconds()) if end else 0
    return Entry(
        entry_id,
        begin,
        end,
        duration,
        description,
        billable,
        project_id,
        "Moduł rezerwacji",
        "#008000",
        activity_id,
        "Programowanie",
        language,
    )


class FakeClient:
    def __init__(self, timezone="Europe/Warsaw"):
        self.user = User(2, "jan", None, "pl", timezone)
        self.now = NOW
        self.entries: dict[int, Entry] = {}
        self.next_id = 100
        self.calls: list[tuple] = []
        self.fail: dict[str, list[Exception]] = {}
        self.billable_forbidden = False
        self.start_timeout: str | None = None  # "before" (nothing saved) | "after" (saved, reply lost)
        self.range_entries: list[Entry] | None = None
        self.details: dict[
            int, dict
        ] = {}  # what GET /api/timesheets/{id} adds to an entry: tags, rates, meta
        self.projects_list = [
            Project(1, "Moduł rezerwacji", 10, "Hotel Morski", "#008000", True),
            Project(2, "Administracja", 20, "Sprawy wewnętrzne", "#808080", True),
        ]
        self.customers_list = [Customer(10, "Hotel Morski", True), Customer(20, "Sprawy wewnętrzne", False)]
        self.activities_list = [
            Activity(2, "Spotkanie", True, None),
            Activity(1, "Programowanie", True, None),
        ]

    # -- helpers ------------------------------------------------------------
    def add(self, entry: Entry) -> Entry:
        self.entries[entry.id] = entry
        return entry

    def _check(self, name):
        queue = self.fail.get(name)
        if queue:
            raise queue.pop(0)

    def _parse(self, stamp: str) -> datetime:
        return datetime.strptime(stamp, STAMP).replace(tzinfo=ZoneInfo(self.user.timezone))

    @staticmethod
    def _as_posted(entry: Entry) -> Entry:
        """POST/PATCH answers carry related objects as bare ids."""
        return replace(entry, project_name=None, project_color=None, activity_name=None)

    # -- API ------------------------------------------------------------------
    def me(self):
        self.calls.append(("me",))
        self._check("me")
        return self.user

    def active(self):
        self.calls.append(("active",))
        self._check("active")
        return [e for e in self.entries.values() if e.running]

    def latest(self, size=20):
        self.calls.append(("latest", size))
        self._check("latest")
        return sorted(self.entries.values(), key=lambda e: e.begin, reverse=True)[:size]

    def search(self, term, size=50):
        """Like Kimai 2.67: every word must occur in the description, case-insensitive; newest first."""
        self.calls.append(("search", term, size))
        self._check("search")
        words = term.lower().split()
        found = [e for e in self.entries.values() if all(w in e.description.lower() for w in words)]
        return sorted(found, key=lambda e: e.begin, reverse=True)[:size]

    def range(self, begin, end):
        """Like Kimai: entries that start inside the window (begin and end are Kimai-local stamps)."""
        self.calls.append(("range", begin, end))
        self._check("range")
        if self.range_entries is not None:
            return list(self.range_entries)
        try:
            low, high = self._parse(begin), self._parse(end)
        except (ValueError, KeyError):  # a made-up account zone: the tracker falls back, so do we
            return list(self.entries.values())
        return [e for e in self.entries.values() if low <= e.begin <= high]

    def create_entry(self, *, project_id, activity_id, description, begin, end, billable=None):
        self.calls.append(("create_entry", project_id, activity_id, description, begin, end, billable))
        self._check("create_entry")
        if billable is not None and self.billable_forbidden:
            raise ApiError(ErrorKind.REJECTED, 400, EXTRA_FIELDS)
        project = next((p for p in self.projects_list if p.id == project_id), None)
        activity = next((a for a in self.activities_list if a.id == activity_id), None)
        entry = replace(
            make_entry(
                self.next_id,
                self._parse(begin),
                self._parse(end),
                description=description,
                billable=True if billable is None else billable,
                project_id=project_id,
                activity_id=activity_id,
            ),
            project_name=project.name if project else None,
            project_color=project.color if project else None,
            activity_name=activity.name if activity else None,
        )
        self.next_id += 1
        self.add(entry)
        return self._as_posted(entry)

    def delete_entry(self, entry_id):
        self.calls.append(("delete_entry", entry_id))
        self._check("delete_entry")
        del self.entries[entry_id]

    def projects(self):
        self._check("projects")
        return list(self.projects_list)

    def customers(self):
        self._check("customers")
        return list(self.customers_list)

    def activities(self, project_id=None):
        self.calls.append(("activities", project_id))
        return list(self.activities_list)

    def start(self, *, project_id, activity_id, description, begin, billable=None):
        self.calls.append(("start", project_id, activity_id, description, begin, billable))
        self._check("start")
        if self.start_timeout == "before":
            raise ApiError(ErrorKind.TIMEOUT, 0, "timed out")
        if billable is not None and self.billable_forbidden:
            raise ApiError(ErrorKind.REJECTED, 400, EXTRA_FIELDS)
        began = self._parse(begin)
        for entry in list(self.entries.values()):  # default limit 1: the running one is stopped
            if entry.running:
                self.entries[entry.id] = make_entry(
                    entry.id, entry.begin, began, description=entry.description
                )
        entry = make_entry(
            self.next_id,
            began,
            description=description,
            billable=True if billable is None else billable,
            project_id=project_id,
            activity_id=activity_id,
        )
        self.next_id += 1
        self.add(entry)
        if self.start_timeout == "after":
            raise ApiError(ErrorKind.TIMEOUT, 0, "timed out")
        return self._as_posted(entry)

    def stop(self, entry_id):
        self.calls.append(("stop", entry_id))
        self._check("stop")
        entry = self.entries[entry_id]
        if entry.running:
            entry = self.add(
                make_entry(
                    entry.id, entry.begin, self.now, description=entry.description, billable=entry.billable
                )
            )
        return self._as_posted(entry)

    def entry_details(self, entry_id):
        self.calls.append(("entry_details", entry_id))
        self._check("entry_details")
        entry = self.entries[entry_id]
        raw = {
            "id": entry.id, "begin": entry.begin.isoformat(),
            "end": entry.end.isoformat() if entry.end else None,
            "project": entry.project_id, "activity": entry.activity_id, "description": entry.description,
            "billable": entry.billable, "exported": entry.exported, "tags": [], "break": 0, "metaFields": [],
            **self.details.get(entry_id, {}),
        }  # fmt: skip
        return EntryDetails.from_api(raw)

    def set_meta(self, entry_id, name, value):
        self.calls.append(("set_meta", entry_id, name, value))
        self._check("set_meta")

    def update(self, entry_id, changes):
        self.calls.append(("update", entry_id, dict(changes)))
        self._check("update")
        if "billable" in changes and self.billable_forbidden:
            raise ApiError(ErrorKind.REJECTED, 400, EXTRA_FIELDS)
        entry = self.entries[entry_id]
        if "description" in changes:
            entry = replace(entry, description=changes["description"])
        if "billable" in changes:
            entry = replace(entry, billable=changes["billable"])
        if "project" in changes:
            project = next(p for p in self.projects_list if p.id == changes["project"])
            entry = replace(
                entry, project_id=project.id, project_name=project.name, project_color=project.color
            )
        if "activity" in changes:
            activity = next(a for a in self.activities_list if a.id == changes["activity"])
            entry = replace(entry, activity_id=activity.id, activity_name=activity.name)
        if "begin" in changes:
            entry = replace(entry, begin=self._parse(changes["begin"]))
        if "end" in changes:
            end = self._parse(changes["end"])
            entry = replace(entry, end=end, duration=int((end - entry.begin).total_seconds()))
        self.add(entry)
        return self._as_posted(entry)
