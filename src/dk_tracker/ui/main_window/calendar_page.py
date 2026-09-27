"""`app.calendarPage` in QML (Plan 7): the days shown, the entries as blocks, and what the calendar
does — a new entry from a dragged span, a block moved or resized.

It asks the controller for the entries of the days shown (`loadRequested`); an answer for other
days is dropped, and one that comes while a block is dragged waits until it is let go. A moved
block stands in its new place at once; if Kimai refuses, the controller loads the days again.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import replace
from datetime import date, datetime, tzinfo
from typing import Any

from PySide6.QtCore import Property, QObject, Signal, Slot

from dk_tracker.core.calendar import (
    DAY_MINUTES,
    SNAP_MINUTES,
    Mode,
    day_totals,
    hhmm_of,
    layout,
    shifted,
    snap,
    span_label,
    view_days,
)
from dk_tracker.core.i18n import Translator
from dk_tracker.core.models import Entry
from dk_tracker.core.timefmt import local_day, short_duration, wall_clock


class CalendarPage(QObject):
    dataChanged = Signal()
    loadRequested = Signal(object, object)  # first and last day shown (date)
    addRequested = Signal(dict)  # Tracker.add_entry keywords
    moveRequested = Signal(int, object, int, int)  # entry id, day (date), begin and end minutes

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._t: Callable[..., str] = Translator("en")  # until the controller says the language
        self._today = date.today()
        self._first_weekday = 0
        self._mode: Mode = "week"
        self._workweek = False
        self._anchor = self._today
        self._chosen = False  # still "this week" as the app started: a new day moves it along
        self._entries: list[Entry] = []
        self._shown: tuple[date, date] | None = None  # the days the entries are for
        self._hidden: set[int] = set()
        self._tz: tzinfo | None = None
        self._now: datetime | None = None
        self._loading = False
        self._dragging = False
        self._deferred: tuple[date, date, list[Entry]] | None = None
        self._data: dict[str, Any] = {}
        self._refresh()

    def _get_data(self) -> dict[str, Any]:
        return self._data

    data = Property("QVariantMap", _get_data, notify=dataChanged)

    @property
    def days(self) -> list[date]:
        return view_days(self._mode, self._anchor, self._first_weekday, workweek=self._workweek)

    # -- from the controller ---------------------------------------------------------------

    def configure(
        self, *, today: date, first_weekday: int, t: Callable[..., str], now: datetime, tz: tzinfo
    ) -> None:
        """The day, the account's first weekday, the language and the clock; redrawn only on a change."""
        minute = now.replace(second=0, microsecond=0)
        if (today, first_weekday, t, tz) == (self._today, self._first_weekday, self._t, self._tz) and (
            self._now is not None and minute == self._now.replace(second=0, microsecond=0)
        ):
            return
        self._today, self._first_weekday, self._t, self._tz, self._now = today, first_weekday, t, tz, now
        if not self._chosen:
            self._anchor = today
        self._refresh()

    def tick(self, now: datetime) -> None:
        """Every second from the window: the running block and the "now" line move once a minute."""
        if self._tz is not None:
            tz = self._tz
            self.configure(
                today=local_day(now, tz), first_weekday=self._first_weekday, t=self._t, now=now, tz=tz
            )

    def request(self) -> None:
        self._loading = True
        self._refresh()
        days = self.days
        self.loadRequested.emit(days[0], days[-1])

    def set_entries(
        self, first: date, last: date, entries: Iterable[Entry], *, tz: tzinfo, now: datetime
    ) -> None:
        days = self.days
        if (first, last) != (days[0], days[-1]):
            return  # the user has moved on; the answer for the days shown is on its way
        if self._dragging:  # rebuilding the blocks would drop the one under the pointer
            self._deferred = (first, last, list(entries))
            return
        self._entries, self._shown, self._tz, self._now = list(entries), (first, last), tz, now
        self._loading = False
        self._refresh()

    def set_loading(self, loading: bool) -> None:
        self._loading = loading
        self._refresh()

    def entry(self, entry_id: int) -> Entry | None:
        return next((entry for entry in self._entries if entry.id == entry_id), None)

    def hide_entry(self, entry_id: int) -> None:
        """Deleted: gone from the grid while the undo bar is up."""
        self._hidden.add(entry_id)
        self._refresh()

    def show_entry(self, entry_id: int) -> None:
        self._hidden.discard(entry_id)
        self._refresh()

    # -- from QML ----------------------------------------------------------------------------

    @Slot(str)
    def setMode(self, mode: str) -> None:  # noqa: N802
        if mode in ("day", "week") and mode != self._mode:
            if mode == "day" and not self.days[0] <= self._today <= self.days[-1]:
                self._anchor = self.days[0]  # the week's first day, not a day of another week
            elif mode == "day":
                self._anchor = self._today
            self._mode = mode  # type: ignore[assignment]
            self._go()

    @Slot(bool)
    def setWorkweek(self, value: bool) -> None:  # noqa: N802
        if value != self._workweek:
            self._workweek = value
            self._go()

    @Slot(int)
    def step(self, steps: int) -> None:
        self._anchor = shifted(self._mode, self._anchor, steps)
        self._go()

    @Slot()
    def today(self) -> None:
        self._anchor = self._today
        self._go()

    @Slot(int, int, int, str, int, int, "QVariant")
    def create(  # noqa: PLR0913
        self,
        day: int,
        begin: int,
        end: int,
        description: str,
        projectId: int,  # noqa: N803
        activityId: int,  # noqa: N803
        billable: Any,
    ) -> None:
        """A span dragged on an empty part of a day, filled in its bubble."""
        self.addRequested.emit(
            {
                "day": self.days[day],
                "begin": hhmm_of(begin),
                "end": hhmm_of(end),
                "description": description,
                "project_id": projectId or None,
                "activity_id": activityId or None,
                "billable": billable,
            }
        )

    @Slot(int, int, int, int)
    def move(self, entryId: int, day: int, begin: int, end: int) -> None:  # noqa: N803
        """A block let go in a new place (or with a new edge): shown there at once, then saved."""
        entry = self.entry(entryId)
        if entry is None or self._tz is None or not self._movable(entry) or end <= begin:
            return
        target = self.days[day]
        moved = replace(
            entry,
            begin=wall_clock(target, begin, self._tz),
            end=wall_clock(target, end, self._tz),
            duration=(end - begin) * 60,
        )
        self._entries = [moved if item.id == entryId else item for item in self._entries]
        self._refresh()
        self.moveRequested.emit(entryId, target, begin, end)

    @Slot(float, bool, result=int)
    def snap(self, minutes: float, exact: bool) -> int:
        """While dragging: quarter hours, or the exact minute with Alt."""
        return snap(minutes, 1 if exact else SNAP_MINUTES)

    @Slot(bool)
    def setDragging(self, value: bool) -> None:  # noqa: N802
        self._dragging = value
        if not value and self._deferred is not None:
            deferred, self._deferred = self._deferred, None
            if self._tz is not None and self._now is not None:
                self.set_entries(*deferred[:2], deferred[2], tz=self._tz, now=self._now)

    # -- internals ---------------------------------------------------------------------------

    def _go(self) -> None:
        self._chosen = True
        self.request()

    def _movable(self, entry: Entry) -> bool:
        """Finished, not invoiced, and on one day (ending at its midnight at the latest)."""
        if entry.end is None or entry.exported or self._tz is None:
            return False
        begin, end = entry.begin.astimezone(self._tz), entry.end.astimezone(self._tz)
        return end <= wall_clock(begin.date(), DAY_MINUTES, self._tz)

    def _refresh(self) -> None:
        t, days = self._t, self.days
        weekdays = t("weekdaysShort").split(",")
        shown = self._shown == (days[0], days[-1]) and self._tz is not None and self._now is not None
        entries = [entry for entry in self._entries if entry.id not in self._hidden] if shown else []
        tz, now = self._tz, self._now
        totals = day_totals(entries, days, tz, now) if shown else [0] * len(days)  # type: ignore[arg-type]
        blocks = layout(entries, days, tz, now) if shown else []  # type: ignore[arg-type]
        now_minutes = -1
        if tz is not None and now is not None and local_day(now, tz) in days:
            local = now.astimezone(tz)
            now_minutes = local.hour * 60 + local.minute
        self._data = {
            "mode": self._mode,
            "workweek": self._workweek,
            "label": span_label(days, self._today, t),
            "isToday": self._today in days,
            "loading": self._loading,
            "loaded": shown,
            "now": now_minutes,
            "days": [
                {
                    "date": day.isoformat(),
                    "label": t("sumBarDay", weekday=weekdays[day.weekday()], day=day.day),
                    "total": short_duration(total) if total else "",
                    "today": day == self._today,
                }
                for day, total in zip(days, totals, strict=True)
            ],
            "blocks": [self._block(block) for block in blocks],
        }
        self.dataChanged.emit()

    def _block(self, block: Any) -> dict[str, Any]:
        entry: Entry = block.entry
        names = [name for name in (entry.project_name, entry.activity_name) if name]
        return {
            "id": entry.id,
            "day": block.day,
            "start": block.start,
            "end": block.end,
            "column": block.column,
            "columns": block.columns,
            "description": " ".join(entry.description.split()),
            "project": " · ".join(names),
            "color": entry.project_color or "",
            "hours": f"{hhmm_of(block.start)} – {hhmm_of(block.end)}",  # a running one: until now
            "time": short_duration((block.end - block.start) * 60),
            "running": block.running,
            "exported": entry.exported,
            "billable": entry.billable,
            "projectId": entry.project_id or 0,
            "activityId": entry.activity_id or 0,
            "movable": self._movable(entry) and not block.continued and not block.continues,
            "continued": block.continued,
            "continues": block.continues,
        }
