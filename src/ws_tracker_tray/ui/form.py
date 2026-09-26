"""The tracker bar of the quick window (F-04 … F-09): description, start/stop, project,
activity, the billable switch and — while an entry runs — its start and end times.

The form never talks to Kimai. It emits what the user asked for and redraws from Snapshots;
the controller (app.py) runs the tracker on a worker thread.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from datetime import datetime, tzinfo

from PySide6.QtCore import (
    QRegularExpression,
    QSize,
    Qt,
    QTimer,
    Signal,
)
from PySide6.QtGui import (
    QColor,
    QIcon,
    QKeyEvent,
    QPainter,
    QPixmap,
    QRegularExpressionValidator,
    QStandardItem,
)
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ws_tracker_tray.core.billable import default_billable
from ws_tracker_tray.core.grouping import group_projects
from ws_tracker_tray.core.models import Activity, Entry, Project
from ws_tracker_tray.core.timefmt import clock, elapsed_seconds, hhmm
from ws_tracker_tray.core.tracker import Snapshot

from .icons import glyph
from .project_picker import ProjectComboBox

GREY_DOT = "#9aa0ac"
_HHMM = QRegularExpression(r"^([01]?\d|2[0-3]):[0-5]\d$")


def dot(color: str | None, size: int = 10) -> QIcon:
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor(color or GREY_DOT))
    painter.drawEllipse(0, 0, size, size)
    painter.end()
    return QIcon(pixmap)


class DescriptionEdit(QPlainTextEdit):
    """Enter submits, Shift+Enter adds a line; grows from one line up to 96 px (popup.css)."""

    submitted = Signal()
    focusLost = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("description")
        self.setTabChangesFocus(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textChanged.connect(self._grow)
        self._grow()

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802 - Qt API
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter) and not (
            event.modifiers() & Qt.KeyboardModifier.ShiftModifier
        ):
            self.submitted.emit()
            return
        super().keyPressEvent(event)

    def focusOutEvent(self, event) -> None:  # noqa: N802 - Qt API
        super().focusOutEvent(event)
        self.focusLost.emit()

    def _grow(self) -> None:
        lines = max(1, self.document().size().height())
        height = int(lines * self.fontMetrics().lineSpacing()) + 18
        self.setFixedHeight(max(38, min(96, height)))
        # A scroll bar only once the text is taller than the field may grow.
        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded if height > 96 else Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )


class TrackerForm(QWidget):
    startRequested = Signal(object)  # {"project_id", "activity_id", "description", "billable"}
    stopRequested = Signal(str)  # "HH:MM" typed in "to", or "" for now
    descriptionCommitted = Signal(str, bool)  # text, quiet (the save-while-typing path)
    beginCommitted = Signal(str)
    billableChanged = Signal(bool)  # the running entry's switch
    projectChosen = Signal(object)  # project id or None — the controller loads its activities
    edited = Signal()  # any typing: the window clears a stale error, as the add-on does

    def __init__(self, t: Callable[..., str], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("tracker")
        self.save_delay_ms = 1200  # F-07: quiet save 1.2 s after typing stops
        self._t = t
        self._running: Entry | None = None
        self._shown_text = ""  # the description as last rendered; differs once the user types
        self._projects: dict[int, Project] = {}
        self._non_billable: frozenset[int] = frozenset()
        self._activities: dict[int, Activity] = {}
        self._billable = True
        self._touched = False
        self._allowed = True
        self._tz: tzinfo | None = None

        self.description = DescriptionEdit()
        self.clock = QLabel(objectName="clock")
        self.toggle = QPushButton(objectName="toggle")
        self.toggle.setIconSize(QSize(20, 20))
        # Its list opens with a search field on top (project_picker.py).
        self.project = ProjectComboBox(t)
        self.activity = QComboBox()
        self.billable = QPushButton(objectName="billable")
        self.billable.setIconSize(QSize(17, 17))
        self.times = QFrame(objectName="times")
        self.begin = QLineEdit()
        self.end = QLineEdit()
        self.from_label = QLabel(objectName="timesLabel")
        self.to_label = QLabel(objectName="timesLabel")
        self.end_hint = QLabel(objectName="hint")
        for field in (self.begin, self.end):
            field.setValidator(QRegularExpressionValidator(_HHMM, field))
            field.setPlaceholderText("--:--")
            field.setMaxLength(5)

        right = QVBoxLayout()
        right.setSpacing(4)
        right.addWidget(self.clock, alignment=Qt.AlignmentFlag.AlignHCenter)
        right.addWidget(self.toggle, alignment=Qt.AlignmentFlag.AlignHCenter)
        main = QHBoxLayout()
        main.setSpacing(12)
        main.addWidget(self.description, 1, Qt.AlignmentFlag.AlignBottom)
        main.addLayout(right)
        second = QHBoxLayout()
        second.setSpacing(8)
        second.addWidget(self.activity, 1)
        second.addWidget(self.billable)
        times = QGridLayout(self.times)
        times.setContentsMargins(11, 10, 11, 10)
        times.addWidget(self.from_label, 0, 0)
        times.addWidget(self.to_label, 0, 1)
        times.addWidget(self.begin, 1, 0)
        times.addWidget(self.end, 1, 1)
        times.addWidget(self.end_hint, 2, 0, 1, 2)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(8)
        layout.addLayout(main)
        layout.addWidget(self.project)
        layout.addLayout(second)
        layout.addWidget(self.times)

        self._save_timer = QTimer(self, singleShot=True)
        self._save_timer.timeout.connect(lambda: self._commit_description(quiet=True))
        self.description.submitted.connect(self._on_enter)
        self.description.focusLost.connect(lambda: self._commit_description(quiet=False))
        self.description.textChanged.connect(self._on_typed)
        self.toggle.clicked.connect(self._on_toggle)
        self.billable.clicked.connect(self._on_billable)
        self.project.activated.connect(lambda _index: self._on_project(user=True))
        self.activity.activated.connect(lambda _index: self._on_activity())
        self.begin.editingFinished.connect(self._on_begin)
        self.clock.hide()
        self.times.hide()
        self.retranslate(t)

    # -- data from the controller ---------------------------------------------

    @property
    def billable_value(self) -> bool:
        return self._billable

    @property
    def running(self) -> Entry | None:
        return self._running

    def set_catalog(self, snapshot: Snapshot, remembered_project: int | None) -> None:
        """Projects grouped by customer, as in the add-on (a flat list of 75 was unusable)."""
        self._projects = {project.id: project for project in snapshot.projects}
        self._non_billable = snapshot.non_billable_customers
        chosen = self.project.currentData() or remembered_project
        self.project.clear()
        self.project.addItem(dot(None), self._t("chooseProject"), None)
        model = self.project.model()
        for customer, projects in group_projects(snapshot.projects):
            header = QStandardItem(customer)
            header.setEnabled(False)
            font = header.font()
            font.setBold(True)
            header.setFont(font)
            model.appendRow(header)
            for project in projects:
                self.project.addItem(dot(project.color), project.name, project.id)
        running = self._running
        if running is not None and self.project.findData(running.project_id) < 0:
            # The running entry's project may be missing from the catalog (hidden, archived).
            self.project.addItem(dot(running.project_color), running.project_name or "?", running.project_id)
        self._select(self.project, running.project_id if running is not None else chosen)
        if self._running is None:
            self._reset_billable()

    def set_activities(self, activities: Iterable[Activity], remembered_activity: int | None) -> None:
        if self._running is not None:
            return  # the picker holds the running entry's activity; rebuilt after stop
        chosen = self.activity.currentData() or remembered_activity
        self._activities = {activity.id: activity for activity in activities}
        self.activity.clear()
        self.activity.addItem(self._t("chooseActivity"), None)
        for activity in self._activities.values():
            self.activity.addItem(activity.name, activity.id)
        self._select(self.activity, chosen)
        if not self._touched:
            self._reset_billable()

    def select_project(self, project_id: int | None) -> None:
        self._select(self.project, project_id)
        self._on_project(user=True)

    def render(self, snapshot: Snapshot, tz: tzinfo, now: datetime) -> None:
        self._tz = tz
        self._allowed = snapshot.billable_allowed
        current = snapshot.current
        previous, self._running = self._running, current
        if current is None:
            if previous is not None:
                self._enter_idle()
        else:
            self._enter_running(current, changed=previous is None or previous.id != current.id)
        self._paint_toggle()
        self._paint_billable()
        self.tick(now)

    def tick(self, now: datetime) -> None:
        if self._running is not None:
            self.clock.setText(clock(elapsed_seconds(self._running.begin, now)))

    def retranslate(self, t: Callable[..., str]) -> None:
        self._t = t
        self.description.setPlaceholderText(t("descriptionPlaceholder"))
        self.description.setToolTip(t("descriptionLabel"))
        self.project.setToolTip(t("projectLabel"))
        self.project.retranslate(t)
        self.activity.setToolTip(t("activityLabel"))
        self.from_label.setText(t("fromLabel").upper())
        self.to_label.setText(t("toLabel").upper())
        self.end_hint.setText(t("endHint"))
        if self.project.count():
            self.project.setItemText(0, t("chooseProject"))
        if self.activity.count() and self._running is None:
            self.activity.setItemText(0, t("chooseActivity"))
        self._paint_toggle()
        self._paint_billable()

    # -- states -----------------------------------------------------------------

    def _enter_running(self, entry: Entry, *, changed: bool) -> None:
        typed = self.description.toPlainText() != self._shown_text
        if changed or not typed:
            self._set_text(entry.description)
        if changed or not self.begin.hasFocus():
            self.begin.setText(hhmm(entry.begin, self._tz))  # type: ignore[arg-type]
        if changed:
            self.end.clear()
        if entry.project_id not in self._projects:
            self.project.addItem(dot(entry.project_color), entry.project_name or "?", entry.project_id)
        self._select(self.project, entry.project_id)
        self.activity.clear()
        self.activity.addItem(entry.activity_name or "", entry.activity_id)
        self.project.setEnabled(False)
        self.activity.setEnabled(False)
        self._billable = entry.billable
        self._touched = False
        self.times.show()
        self.clock.show()

    def _enter_idle(self) -> None:
        self._save_timer.stop()
        self._set_text("")
        self.end.clear()
        self.times.hide()
        self.clock.hide()
        self.project.setEnabled(True)
        self.activity.setEnabled(True)
        self._touched = False
        # The activity picker held only the stopped entry's label: ask for the real list again.
        self.projectChosen.emit(self.project.currentData())

    # -- user actions -------------------------------------------------------------

    def _on_enter(self) -> None:
        if self._running is not None:
            self._commit_description(quiet=False)
        else:
            self._on_toggle()

    def _on_toggle(self) -> None:
        if self._running is not None:
            self.stopRequested.emit(self.end.text().strip() if self.end.hasAcceptableInput() else "")
            return
        self.startRequested.emit(
            {
                "project_id": self.project.currentData(),
                "activity_id": self.activity.currentData(),
                "description": self.description.toPlainText(),
                "billable": self._billable if self._touched else None,
            }
        )

    def _on_typed(self) -> None:
        self.edited.emit()
        if self._running is not None and self.description.toPlainText() != self._shown_text:
            self._save_timer.start(self.save_delay_ms)

    def _commit_description(self, *, quiet: bool) -> None:
        self._save_timer.stop()
        if self._running is None:
            return
        text = self.description.toPlainText()
        if text.strip() == self._running.description:
            return
        self._shown_text = text
        self.descriptionCommitted.emit(text, quiet)

    def _on_begin(self) -> None:
        if self._running is not None and self.begin.hasAcceptableInput():
            if self.begin.text() != hhmm(self._running.begin, self._tz):  # type: ignore[arg-type]
                self.beginCommitted.emit(self.begin.text())

    def _on_billable(self) -> None:
        if not self._allowed:
            return
        self._billable = not self._billable
        self._paint_billable()
        if self._running is not None:
            self.billableChanged.emit(self._billable)
        else:
            self._touched = True

    def _on_project(self, *, user: bool) -> None:
        if user:
            self._touched = False
            self._reset_billable()
        self.projectChosen.emit(self.project.currentData())

    def _on_activity(self) -> None:
        if not self._touched:
            self._reset_billable()

    # -- painting -------------------------------------------------------------------

    def _reset_billable(self) -> None:
        project = self._projects.get(self.project.currentData())
        activity = self._activities.get(self.activity.currentData())
        self._billable = default_billable(project, activity, self._non_billable)
        self._paint_billable()

    def _paint_toggle(self) -> None:
        running = self._running is not None
        self.toggle.setProperty("state", "stop" if running else "start")
        self.toggle.setIcon(glyph("stop" if running else "play", "#ffffff"))
        self.toggle.setToolTip(self._t("stop" if running else "start"))
        self.toggle.style().unpolish(self.toggle)
        self.toggle.style().polish(self.toggle)

    def _paint_billable(self) -> None:
        on = self._billable
        self.billable.setProperty("on", "true" if on else "false")
        self.billable.setIcon(glyph("money" if on else "money_off", "#16a34a" if on else GREY_DOT))
        self.billable.setEnabled(self._allowed)
        self.billable.setToolTip(
            self._t("billableOn" if on else "billableOff") if self._allowed else self._t("billableLocked")
        )
        self.billable.setAccessibleName(self._t("billableChipOn" if on else "billableChipOff"))
        self.billable.style().unpolish(self.billable)
        self.billable.style().polish(self.billable)

    def _set_text(self, text: str) -> None:
        self.description.blockSignals(True)
        self.description.setPlainText(text)
        self.description.blockSignals(False)
        self.description._grow()
        self._shown_text = text

    @staticmethod
    def _select(combo: QComboBox, value: object) -> None:
        index = combo.findData(value) if value is not None else -1
        combo.setCurrentIndex(index if index >= 0 else 0)
