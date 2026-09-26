"""List models the QML main window draws: the entry list, the projects and the activities.

QML only reads roles by name; every text and rule is made here (and in core/), where it is tested.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import tzinfo
from typing import Any

from PySide6.QtCore import QAbstractListModel, QByteArray, QModelIndex, QObject, Qt

from dk_tracker.core.entry_list import ListRow
from dk_tracker.core.grouping import group_projects, sort_key
from dk_tracker.core.models import Activity, Entry, Project
from dk_tracker.core.timefmt import hhmm

_FIRST = Qt.ItemDataRole.UserRole + 1


class _RoleModel(QAbstractListModel):
    """Rows are plain dicts; the role names are their keys."""

    NAMES: tuple[str, ...] = ()

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._rows: list[dict[str, Any]] = []

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: B008, N802 - Qt API
        return 0 if parent.isValid() else len(self._rows)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or not 0 <= index.row() < len(self._rows):
            return None
        position = role - _FIRST
        if not 0 <= position < len(self.NAMES):
            return None
        return self._rows[index.row()][self.NAMES[position]]

    def roleNames(self) -> dict[int, QByteArray]:  # noqa: N802 - Qt API
        return {_FIRST + i: QByteArray(name.encode()) for i, name in enumerate(self.NAMES)}

    def _replace(self, rows: list[dict[str, Any]]) -> None:
        self.beginResetModel()
        self._rows = rows
        self.endResetModel()

    def _merge(self, rows: list[dict[str, Any]]) -> None:
        """Rows matched by their "key": what stays keeps its delegate, so a refresh neither scrolls
        the list back to the top nor closes a popup open in a row (a reset did both)."""
        old = self._rows
        head = 0
        while head < min(len(old), len(rows)) and old[head]["key"] == rows[head]["key"]:
            head += 1
        tail = 0
        while tail < min(len(old), len(rows)) - head and old[-1 - tail]["key"] == rows[-1 - tail]["key"]:
            tail += 1
        if len(old) - tail > head:
            self.beginRemoveRows(QModelIndex(), head, len(old) - tail - 1)
            del self._rows[head : len(old) - tail]
            self.endRemoveRows()
        if len(rows) - tail > head:
            self.beginInsertRows(QModelIndex(), head, len(rows) - tail - 1)
            self._rows[head:head] = rows[head : len(rows) - tail]
            self.endInsertRows()
        for row, fresh in enumerate(rows):
            if self._rows[row] != fresh:
                self._rows[row] = fresh
                self.dataChanged.emit(self.index(row), self.index(row))


class EntryListModel(_RoleModel):
    """Weeks, days and entries (core/entry_list.py), minus entries hidden by the undo bar."""

    NAMES = (
        "kind", "key", "label", "total", "entryId", "description", "projectId", "projectName",
        "projectColor", "activityId", "activityName", "billable", "begin", "end", "exported",
    )  # fmt: skip

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._all: list[ListRow] = []
        self._tz: tzinfo | None = None
        self._hidden: set[int] = set()

    def set_rows(self, rows: list[ListRow], tz: tzinfo) -> None:
        self._all, self._tz = list(rows), tz
        self._show()

    def entry(self, entry_id: int) -> Entry | None:
        return next(
            (row.entry for row in self._all if row.entry is not None and row.entry.id == entry_id), None
        )

    def hide_entry(self, entry_id: int) -> None:
        self._hidden.add(entry_id)
        self._show()

    def show_entry(self, entry_id: int) -> None:
        self._hidden.discard(entry_id)
        self._show()

    def _show(self) -> None:
        tz = self._tz
        rows = []
        for row in self._all:
            entry = row.entry
            if entry is not None and entry.id in self._hidden:
                continue
            rows.append(
                {
                    "kind": row.kind,
                    "key": row.key,
                    "label": row.label,
                    "total": row.total,
                    "entryId": entry.id if entry else 0,
                    "description": entry.description if entry else "",
                    "projectId": (entry.project_id or 0) if entry else 0,
                    "projectName": (entry.project_name or "") if entry else "",
                    "projectColor": (entry.project_color or "") if entry else "",
                    "activityId": (entry.activity_id or 0) if entry else 0,
                    "activityName": (entry.activity_name or "") if entry else "",
                    "billable": entry.billable if entry else False,
                    "begin": hhmm(entry.begin, tz) if entry and tz else "",
                    "end": hhmm(entry.end, tz) if entry and entry.end and tz else "",
                    "exported": entry.exported if entry else False,
                }
            )
        self._merge(rows)


class ProjectModel(_RoleModel):
    """Projects grouped by customer; the filter ignores case and Polish letters (as F-06)."""

    NAMES = ("kind", "projectId", "name", "color", "customer")

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._projects: list[Project] = []
        self._needle = ""

    def set_projects(self, projects: Iterable[Project]) -> None:
        self._projects = list(projects)
        self._show()

    def set_filter(self, text: str) -> None:
        self._needle = sort_key(text.strip())
        self._show()

    def project(self, project_id: int | None) -> Project | None:
        return next((p for p in self._projects if p.id == project_id), None)

    def _show(self) -> None:
        rows = []
        for customer, projects in group_projects(self._projects):
            matching = [p for p in projects if self._needle in sort_key(f"{p.name} {customer}")]
            if not matching:
                continue
            rows.append(
                {"kind": "header", "projectId": 0, "name": customer, "color": "", "customer": customer}
            )
            rows.extend(
                {
                    "kind": "project",
                    "projectId": p.id,
                    "name": p.name,
                    "color": p.color or "",
                    "customer": customer,
                }
                for p in matching
            )
        self._replace(rows)


class ActivityModel(_RoleModel):
    NAMES = ("activityId", "name")

    def set_activities(self, activities: Iterable[Activity]) -> None:
        self._replace([{"activityId": a.id, "name": a.name} for a in activities])
