"""`app` in QML: the main window's state, texts and palette, and its actions as signals.

QML only draws and calls slots; the controller turns the signals into tracker actions. Deleting
waits for the undo bar (as in Toggl): the row goes at once, Kimai hears of it only afterwards.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import date, datetime, tzinfo
from typing import Any

from PySide6.QtCore import Property, QObject, QTimer, Signal, Slot

from dk_tracker.core.entry_list import ListRow
from dk_tracker.core.errors import describe
from dk_tracker.core.models import Activity, Project
from dk_tracker.core.timefmt import clock, elapsed_seconds, hhmm, short_duration
from dk_tracker.core.tracker import Snapshot, live_totals

from .models import ActivityModel, EntryListModel, ProjectModel

UNDO_MS = 6000


class MainBridge(QObject):
    viewChanged = Signal()
    textsChanged = Signal()
    paletteChanged = Signal()
    rowErrorsChanged = Signal()
    prefill = Signal("QVariantMap")  # "Duplicate": the timer bar in manual mode, filled in
    # -- to the controller
    startRequested = Signal(dict)
    stopRequested = Signal()
    addRequested = Signal(dict)
    editRequested = Signal(int, dict)  # entry id, what changed (Tracker.edit_entry keywords)
    deleteRequested = Signal(int)
    resumeRequested = Signal(int)
    runningEdited = Signal(dict)  # {"description"} | {"project_id", "activity_id"} | {"begin"} | {"billable"}
    loadMoreRequested = Signal()
    searchRequested = Signal(str)
    activitiesRequested = Signal(int)
    settingsRequested = Signal()
    windowClosed = Signal()  # the window's own close button (QML's onClosing)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.entries = EntryListModel(self)
        self.projects = ProjectModel(self)
        self.activities = ActivityModel(self)
        self.undo_ms = UNDO_MS
        # Every key exists from the start: QML warns about a missing one.
        self._view: dict[str, Any] = dict.fromkeys(
            (
                "description",
                "projectName",
                "projectColor",
                "activityName",
                "begin",
                "clock",
                "today",
                "week",
                "error",
                "undo",
            ),
            "",
        )
        self._view.update(configured=False, running=False, projectId=0, activityId=0, billable=True,
                          billableAllowed=True, offline=False, loading=False)  # fmt: skip
        self._texts: dict[str, str] = {}
        self._palette: dict[str, str] = {}
        self._row_errors: dict[str, str] = {}
        self._t: Callable[..., str] = str
        self._pending: int | None = None
        self._undo_timer = QTimer(self, singleShot=True)
        self._undo_timer.timeout.connect(self._commit_delete)

    # -- properties QML binds to ---------------------------------------------------------

    def _get_view(self) -> dict[str, Any]:
        return self._view

    def _get_texts(self) -> dict[str, str]:
        return self._texts

    def _get_palette(self) -> dict[str, str]:
        return self._palette

    def _get_row_errors(self) -> dict[str, str]:
        return self._row_errors

    def _get_entries(self) -> EntryListModel:
        return self.entries

    def _get_projects(self) -> ProjectModel:
        return self.projects

    def _get_activities(self) -> ActivityModel:
        return self.activities

    view = Property("QVariantMap", _get_view, notify=viewChanged)
    texts = Property("QVariantMap", _get_texts, notify=textsChanged)
    palette = Property("QVariantMap", _get_palette, notify=paletteChanged)
    rowErrors = Property("QVariantMap", _get_row_errors, notify=rowErrorsChanged)
    entryList = Property(QObject, _get_entries, constant=True)
    projectList = Property(QObject, _get_projects, constant=True)
    activityList = Property(QObject, _get_activities, constant=True)

    # -- from the controller ---------------------------------------------------------------

    def render(
        self, snapshot: Snapshot, *, configured: bool, t: Callable[..., str], now: datetime, tz: tzinfo
    ) -> None:
        if t is not self._t:
            self._t = t
            messages = getattr(t, "messages", None)
            self._texts = messages() if messages else {}
            self.textsChanged.emit()
        current = snapshot.current
        totals = live_totals(snapshot, now, tz) if snapshot.totals is not None else None
        self._update(
            configured=configured,
            running=current is not None,
            description=current.description if current else "",
            projectId=(current.project_id or 0) if current else 0,
            projectName=(current.project_name or "") if current else "",
            projectColor=(current.project_color or "") if current else "",
            activityId=(current.activity_id or 0) if current else 0,
            activityName=(current.activity_name or "") if current else "",
            billable=current.billable if current else True,
            begin=hhmm(current.begin, tz) if current else "",
            clock=clock(elapsed_seconds(current.begin, now)) if current else "",
            today=t("todayTotal", time=short_duration(totals.today)) if totals else "",
            week=t("weekTotal", time=short_duration(totals.week)) if totals else "",
            billableAllowed=snapshot.billable_allowed,
            offline=snapshot.error is not None,
            error=describe(snapshot.error, t) if snapshot.error is not None else "",
        )

    def set_entries(self, rows: list[ListRow], tz: tzinfo) -> None:
        self.entries.set_rows(rows, tz)

    def set_projects(self, projects: list[Project]) -> None:
        self.projects.set_projects(projects)

    def set_activities(self, activities: list[Activity]) -> None:
        self.activities.set_activities(activities)

    def set_palette(self, palette: dict[str, str]) -> None:
        self._palette = dict(palette)
        self.paletteChanged.emit()

    def set_loading(self, loading: bool) -> None:
        self._update(loading=loading)

    def show_error(self, text: str) -> None:
        self._update(error=text)

    def show_row_error(self, entry_id: int, text: str) -> None:
        self._row_errors = {**self._row_errors, str(entry_id): text}
        self.rowErrorsChanged.emit()

    def flush_deletes(self) -> None:
        """Quitting within the undo time: the delete is not lost."""
        if self._pending is not None:
            self._undo_timer.stop()
            self._commit_delete()

    # -- slots QML calls ---------------------------------------------------------------------

    @Slot(str, int, int, "QVariant")
    def start(self, description: str, projectId: int, activityId: int, billable: Any) -> None:  # noqa: N803
        self.startRequested.emit(
            {"project_id": projectId or None, "activity_id": activityId or None, "description": description,
             "billable": billable}
        )  # fmt: skip

    @Slot()
    def stop(self) -> None:
        self.stopRequested.emit()

    @Slot(str, str, str, str, int, int, "QVariant")
    def addManual(  # noqa: N802
        self,
        day: str,
        begin: str,
        end: str,
        description: str,
        projectId: int,
        activityId: int,
        billable: Any,  # noqa: N803
    ) -> None:
        self.addRequested.emit(
            {
                "day": date.fromisoformat(day),
                "begin": begin,
                "end": end,
                "description": description,
                "project_id": projectId or None,
                "activity_id": activityId or None,
                "billable": billable,
            }
        )

    @Slot(int, str)
    def editDescription(self, entryId: int, text: str) -> None:  # noqa: N802, N803
        self._edit(entryId, {"description": text})

    @Slot(int, int, int)
    def editWork(self, entryId: int, projectId: int, activityId: int) -> None:  # noqa: N802, N803
        self._edit(entryId, {"project_id": projectId, "activity_id": activityId})

    @Slot(int, str, str)
    def editTimes(self, entryId: int, begin: str, end: str) -> None:  # noqa: N802, N803
        self._edit(entryId, {"begin": begin or None, "end": end or None})

    @Slot(int, bool)
    def setBillable(self, entryId: int, value: bool) -> None:  # noqa: N802, N803
        self._edit(entryId, {"billable": value})

    @Slot(int)
    def deleteEntry(self, entryId: int) -> None:  # noqa: N802, N803
        self.flush_deletes()  # one undo at a time, as in Toggl
        self._pending = entryId
        self.entries.hide_entry(entryId)
        self._update(undo=self._t("deletedEntry"))
        self._undo_timer.start(self.undo_ms)

    @Slot()
    def undoDelete(self) -> None:  # noqa: N802
        if self._pending is None:
            return
        self._undo_timer.stop()
        self.entries.show_entry(self._pending)
        self._pending = None
        self._update(undo="")

    @Slot(int)
    def resume(self, entryId: int) -> None:  # noqa: N803
        self.resumeRequested.emit(entryId)

    @Slot(int)
    def duplicate(self, entryId: int) -> None:  # noqa: N803
        entry = self.entries.entry(entryId)
        if entry is not None:
            self.prefill.emit(
                {"description": entry.description, "projectId": entry.project_id or 0,
                 "activityId": entry.activity_id or 0, "billable": entry.billable}
            )  # fmt: skip

    @Slot(str)
    def runningDescription(self, text: str) -> None:  # noqa: N802
        self.runningEdited.emit({"description": text})

    @Slot(int, int)
    def runningWork(self, projectId: int, activityId: int) -> None:  # noqa: N802, N803
        self.runningEdited.emit({"project_id": projectId, "activity_id": activityId})

    @Slot(str)
    def runningBegin(self, text: str) -> None:  # noqa: N802
        self.runningEdited.emit({"begin": text})

    @Slot(bool)
    def runningBillable(self, value: bool) -> None:  # noqa: N802
        self.runningEdited.emit({"billable": value})

    @Slot()
    def loadMore(self) -> None:  # noqa: N802
        self.loadMoreRequested.emit()

    @Slot(str)
    def search(self, text: str) -> None:
        self.searchRequested.emit(text)

    @Slot(str)
    def filterProjects(self, text: str) -> None:  # noqa: N802
        self.projects.set_filter(text)

    @Slot(int, result=str)
    def projectName(self, projectId: int) -> str:  # noqa: N802, N803
        project = self.projects.project(projectId)
        return project.name if project else ""

    @Slot(int)
    def chooseProject(self, projectId: int) -> None:  # noqa: N802, N803
        self.activitiesRequested.emit(projectId)

    @Slot()
    def closeWindow(self) -> None:  # noqa: N802
        self.windowClosed.emit()

    @Slot()
    def openSettings(self) -> None:  # noqa: N802
        self.settingsRequested.emit()

    # -- internals -----------------------------------------------------------------------------

    def _edit(self, entry_id: int, changes: dict[str, Any]) -> None:
        if str(entry_id) in self._row_errors:
            self._row_errors = {k: v for k, v in self._row_errors.items() if k != str(entry_id)}
            self.rowErrorsChanged.emit()
        self.editRequested.emit(entry_id, changes)

    def _commit_delete(self) -> None:
        entry_id, self._pending = self._pending, None
        self._update(undo="")
        if entry_id is not None:
            self.deleteRequested.emit(entry_id)

    def _update(self, **changes: Any) -> None:
        self._view = {**self._view, **changes}
        self.viewChanged.emit()
