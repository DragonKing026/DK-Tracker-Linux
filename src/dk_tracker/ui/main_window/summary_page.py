"""`app.summary` in QML (Plan 6): the period and breakdown the user chose, and what the view draws.

It asks the controller for the period's entries (`loadRequested`) and counts them with
core/summary.py; an answer for a period no longer shown is dropped. The choice lasts while the
app runs (spec: a start shows this week).
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from datetime import date, datetime, timedelta, tzinfo
from typing import Any

from PySide6.QtCore import Property, QObject, Signal, Slot

from dk_tracker.core.i18n import Translator
from dk_tracker.core.models import Entry
from dk_tracker.core.summary import (
    GROUPS,
    KINDS,
    Span,
    Summary,
    present,
    range_span,
    shifted,
    span_for,
    span_label,
    summarize,
)


class SummaryPage(QObject):
    dataChanged = Signal()
    loadRequested = Signal(object, object)  # first and last day (date), both included

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._t: Callable[..., str] = Translator("en")  # until the controller says the language
        self._today = date.today()
        self._first_weekday = 0
        self._span = span_for("week", self._today, 0)
        self._chosen = False  # still "this week" as the app started, so a new week follows along
        self._group = "project"
        self._summary: Summary | None = None
        self._loading = False
        self._data: dict[str, Any] = {}
        self._refresh()

    def _get_data(self) -> dict[str, Any]:
        return self._data

    data = Property("QVariantMap", _get_data, notify=dataChanged)

    @property
    def span(self) -> Span:
        return self._span

    # -- from the controller ---------------------------------------------------------------

    def configure(self, *, today: date, first_weekday: int, t: Callable[..., str]) -> None:
        """The day, the account's first weekday and the language; the period shown stays."""
        if (today, first_weekday, t) == (self._today, self._first_weekday, self._t):
            return  # the window renders every second; the view is redrawn only when something changed
        self._today, self._first_weekday, self._t = today, first_weekday, t
        if not self._chosen:  # "this week" as the app started: a new day or account setting moves it
            self._span = span_for("week", today, first_weekday)
        self._refresh()

    def request(self) -> None:
        """Ask for the entries of the period shown (a change, the minute's refresh, an edit)."""
        self._loading = True
        self._refresh()
        self.loadRequested.emit(self._span.first, self._span.last)

    def set_entries(
        self, first: date, last: date, entries: Iterable[Entry], *, tz: tzinfo, now: datetime, norm: int
    ) -> None:
        if (first, last) != (self._span.first, self._span.last):
            return  # the user has moved on; the answer for the new period is on its way
        self._summary = summarize(
            entries, self._span, tz, now=now, norm=norm, first_weekday=self._first_weekday
        )
        self._loading = False
        self._refresh()

    def set_loading(self, loading: bool) -> None:
        self._loading = loading
        self._refresh()

    def retranslate(self, t: Callable[..., str]) -> None:
        self._t = t
        self._refresh()

    # -- from QML ----------------------------------------------------------------------------

    @Slot(str)
    def setPeriod(self, kind: str) -> None:  # noqa: N802
        if kind not in KINDS:
            return
        if kind == "range":  # a range starts as the period shown, to be changed from there
            self._go(range_span(self._span.first, self._span.last))
        else:
            anchor = self._today if self._span.first <= self._today <= self._span.last else self._span.first
            self._go(span_for(kind, anchor, self._first_weekday))  # type: ignore[arg-type]

    @Slot(int)
    def step(self, steps: int) -> None:
        self._go(shifted(self._span, steps, self._first_weekday))

    @Slot()
    def today(self) -> None:
        if self._span.kind == "range":
            self._go(range_span(self._today - timedelta(days=self._span.days - 1), self._today))
        else:
            self._go(span_for(self._span.kind, self._today, self._first_weekday))

    @Slot(str, str)
    def setRange(self, first: str, last: str) -> None:  # noqa: N802
        try:
            chosen = range_span(date.fromisoformat(first), date.fromisoformat(last))
        except ValueError:  # half typed or impossible
            return
        self._go(chosen)

    @Slot(str)
    def setGroup(self, group: str) -> None:  # noqa: N802
        if group in GROUPS:
            self._group = group
            self._refresh()

    # -- internals ---------------------------------------------------------------------------

    def _go(self, span: Span) -> None:
        self._chosen = True
        self._span = span
        self.request()

    def _refresh(self) -> None:
        span, t = self._span, self._t
        # A refresh keeps the numbers on screen (no flash of an empty view); another period's would
        # sit under the new period's name, so a new period starts blank.
        summary = self._summary if self._summary is not None and self._summary.span == span else None
        data = present(summary, t, group=self._group, today=self._today) if summary else {}  # type: ignore[arg-type]
        self._data = {
            **data,
            "loaded": bool(data),
            "loading": self._loading,
            "kind": span.kind,
            "group": self._group,
            "label": span_label(span, self._today, t),
            "first": span.first.isoformat(),
            "last": span.last.isoformat(),
            "isToday": span.first <= self._today <= span.last,
        }
        self.dataChanged.emit()
