"""The list of recent entries (F-08): days with totals, rows with the billable switch (F-09)
and the resume button (F-10). Rebuilt from each Snapshot; the scroll position is kept.

The search field above it (F-33) swaps the list for results from all of the user's entries in
Kimai until the field is cleared; the controller runs the query and hands the results back."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, tzinfo

from PySide6.QtCore import QSize, Qt, QTimer, Signal
from PySide6.QtGui import QKeyEvent, QMouseEvent
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from dk_tracker.core.grouping import day_total, group_by_day
from dk_tracker.core.models import Entry
from dk_tracker.core.presentation import day_label, entry_row
from dk_tracker.core.timefmt import local_day, short_duration
from dk_tracker.core.tracker import SEARCH_MIN_CHARS, Snapshot

from .form import GREY_DOT, dot
from .icons import glyph

SEARCH_DELAY_MS = 400  # a query when typing pauses, not on every key
COLLAPSED_LINES = 2.5  # the add-on shows two; the cut half line tells that more text follows
UNLIMITED = 16777215  # QWIDGETSIZE_MAX


class EntryRow(QFrame):
    toggled = Signal()  # a click on the row (not on its buttons) expands or collapses the description

    def __init__(
        self, entry: Entry, tz: tzinfo, t: Callable[..., str], *, allowed: bool, expanded: bool = False
    ) -> None:
        super().__init__(objectName="entry")
        self.entry = entry
        text = entry_row(entry, tz, t)
        self.marker = marker = QLabel()
        marker.setPixmap(dot(entry.project_color, 9).pixmap(9, 9))
        self.description = description = QLabel(
            text.description, objectName="entryDescEmpty" if text.empty else "entryDesc"
        )
        description.setWordWrap(True)
        # Top-aligned: centred text in a height-limited label is clipped at the top as well.
        description.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        description.setToolTip(entry.description)
        self.set_expanded(expanded)
        meta = QLabel(text.meta, objectName="entryMeta")
        meta.setWordWrap(True)
        duration = QLabel(text.duration, objectName="entryDuration")
        span = QLabel(text.span, objectName="entrySpan")
        for label in (duration, span):
            label.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.billable = QToolButton(objectName="rowBillable")
        self.billable.setIconSize(QSize(13, 13))
        self.billable.setFixedSize(22, 22)
        self._paint_billable(entry.billable, t)
        self.billable.setEnabled(allowed and not entry.exported)
        if entry.exported:
            self.billable.setToolTip(t("errExported"))
        elif not allowed:
            self.billable.setToolTip(t("billableLocked"))
        self.resume = QToolButton(objectName="resume")
        self.resume.setIcon(glyph("play", "#9aa0ac", 12))
        self.resume.setToolTip(t("resume"))

        grid = QGridLayout(self)
        grid.setContentsMargins(14, 9, 14, 9)
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(2)
        centre = Qt.AlignmentFlag.AlignVCenter
        grid.addWidget(marker, 0, 0, 2, 1, centre)
        grid.addWidget(description, 0, 1)
        grid.addWidget(meta, 1, 1)
        grid.addWidget(duration, 0, 2)
        grid.addWidget(span, 1, 2)
        grid.addWidget(self.billable, 0, 3, 2, 1, centre)
        grid.addWidget(self.resume, 0, 4, 2, 1, centre)
        grid.setColumnStretch(1, 1)

    def set_expanded(self, expanded: bool) -> None:
        self.expanded = expanded
        lines = round(self.description.fontMetrics().lineSpacing() * COLLAPSED_LINES)
        self.description.setMaximumHeight(UNLIMITED if expanded else lines)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802 - Qt API
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(event.position().toPoint()):
            self.toggled.emit()
        super().mouseReleaseEvent(event)

    def mark_pending(self, value: bool, t: Callable[..., str]) -> None:
        self._paint_billable(value, t)
        self.billable.setEnabled(False)

    def _paint_billable(self, on: bool, t: Callable[..., str]) -> None:
        self.billable.setProperty("on", "true" if on else "false")
        self.billable.setIcon(glyph("money" if on else "money_off", "#16a34a" if on else GREY_DOT, 13))
        self.billable.setToolTip(t("billableRowOn" if on else "billableRowOff"))


class _SearchField(QLineEdit):
    """Esc clears the search first; only an empty field lets Esc close the window."""

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802 - Qt API
        if event.key() == Qt.Key.Key_Escape and self.text():
            self.clear()
            event.accept()
        else:
            super().keyPressEvent(event)
            if event.key() == Qt.Key.Key_Escape:
                event.ignore()


class RecentList(QWidget):
    resumeRequested = Signal(object)  # Entry
    billableRequested = Signal(int, bool)  # entry id, new value
    searchRequested = Signal(str)  # normalised term, at least SEARCH_MIN_CHARS long

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("recentPanel")
        self.rows: list[EntryRow] = []
        self._expanded: set[int] = set()  # entry ids whose description is unfolded; kept across refreshes
        self._t: Callable[..., str] = str
        self._snapshot: Snapshot | None = None
        self._tz: tzinfo | None = None
        self._now: datetime | None = None
        self._results: tuple[Entry, ...] | None = None  # None: the recent list is shown
        self.head = QLabel(objectName="recentHead")
        self.search = _SearchField(objectName="recentSearch")
        self.search.setClearButtonEnabled(True)
        self.empty = QLabel(objectName="empty")
        self.empty.setWordWrap(True)
        self.scroll = QScrollArea(objectName="recentList")
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        head = QHBoxLayout()
        head.setContentsMargins(14, 10, 14, 6)
        head.addWidget(self.head)
        layout.addLayout(head)
        search = QHBoxLayout()
        search.setContentsMargins(14, 0, 14, 8)
        search.addWidget(self.search)
        layout.addLayout(search)
        layout.addWidget(self.scroll)
        layout.addWidget(self.empty)
        self.empty.setContentsMargins(14, 18, 14, 18)
        self._delay = QTimer(self, singleShot=True, interval=SEARCH_DELAY_MS)
        self._delay.timeout.connect(self._ask)
        self.search.textChanged.connect(self._on_text)

    @property
    def term(self) -> str:
        return " ".join(self.search.text().split())

    @property
    def searching(self) -> bool:
        return self._results is not None

    def render(self, snapshot: Snapshot, tz: tzinfo, now: datetime, t: Callable[..., str]) -> None:
        self._snapshot, self._tz, self._now, self._t = snapshot, tz, now, t
        self.search.setPlaceholderText(t("searchEntries"))
        if self._results is None:
            self._show(snapshot.recent, allowed=snapshot.billable_allowed)
        else:
            self._show(self._results, allowed=snapshot.billable_allowed)

    def show_results(self, term: str, entries: tuple[Entry, ...], tz: tzinfo, now: datetime) -> None:
        """Results arrive later than typing: only those for the text still in the field count."""
        if term != self.term or len(term) < SEARCH_MIN_CHARS:
            return
        self._results = tuple(entries)
        self._tz, self._now = tz, now
        allowed = self._snapshot.billable_allowed if self._snapshot is not None else True
        self._show(self._results, allowed=allowed)

    def _on_text(self, _text: str) -> None:
        if len(self.term) < SEARCH_MIN_CHARS:
            self._delay.stop()
            if self._results is not None:
                self._results = None
                if self._snapshot is not None:
                    self._show(self._snapshot.recent, allowed=self._snapshot.billable_allowed)
            return
        self._delay.start()

    def _ask(self) -> None:
        if len(self.term) >= SEARCH_MIN_CHARS:
            self.searchRequested.emit(self.term)

    def _show(self, entries: tuple[Entry, ...], *, allowed: bool) -> None:
        t, tz, now = self._t, self._tz, self._now
        if tz is None or now is None:
            return
        if self._results is None:
            self.head.setText(t("recent").upper())
            self.empty.setText(t("recentEmpty"))
        else:
            self.head.setText(t("searchResults", count=len(entries)).upper())
            self.empty.setText(t("searchEmpty"))
        position = self.scroll.verticalScrollBar().value()
        body = QWidget()
        column = QVBoxLayout(body)
        column.setContentsMargins(0, 0, 0, 0)
        column.setSpacing(0)
        self.rows = []
        today = local_day(now, tz)
        for day, day_entries in group_by_day(entries, tz):
            column.addWidget(
                self._day(day_label(day, today, t).upper(), short_duration(day_total(day_entries)))
            )
            for entry in day_entries:
                row = EntryRow(entry, tz, t, allowed=allowed, expanded=entry.id in self._expanded)
                row.toggled.connect(lambda r=row: self._toggle(r))
                row.resume.clicked.connect(lambda _checked=False, e=entry: self.resumeRequested.emit(e))
                row.billable.clicked.connect(lambda _checked=False, r=row: self._on_billable(r))
                self.rows.append(row)
                column.addWidget(row)
        column.addStretch(1)
        self.scroll.setWidget(body)
        self.scroll.verticalScrollBar().setValue(position)
        self.scroll.setVisible(bool(self.rows))
        self.empty.setVisible(not self.rows)

    def _toggle(self, row: EntryRow) -> None:
        self._expanded.symmetric_difference_update({row.entry.id})
        row.set_expanded(row.entry.id in self._expanded)

    def _on_billable(self, row: EntryRow) -> None:
        value = not row.entry.billable
        row.mark_pending(value, self._t)  # optimistic; the next render shows what Kimai kept
        self.billableRequested.emit(row.entry.id, value)

    @staticmethod
    def _day(name: str, total: str) -> QFrame:
        frame = QFrame(objectName="day")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(14, 6, 14, 5)
        layout.addWidget(QLabel(name, objectName="recentDayName"))
        layout.addStretch(1)
        layout.addWidget(QLabel(total, objectName="recentDaySum"))
        return frame
