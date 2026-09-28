"""A time chosen, not typed (0077): the widget twin of the main window's TimeField.qml.

A click opens hours and minutes side by side; minutes in steps of 5, and a value from Kimai
with other minutes (16:21) is on the list too. Picking an hour keeps the list open, picking a
minute closes it. The choice is reported once, when the list closes, so a change of the start
time is one request to Kimai, not two.
"""

from __future__ import annotations

from PySide6.QtCore import QPoint, QSize, Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .icons import glyph

PLACEHOLDER = "--:--"
LIST_HEIGHT = 224
COLUMN_WIDTH = 64  # the number stays clear of the 8 px scroll bar


def _pad(number: int) -> str:
    return f"{number:02d}"


class _Column(QListWidget):
    picked = Signal(int)

    def __init__(self) -> None:
        super().__init__()
        self.setFixedSize(COLUMN_WIDTH, LIST_HEIGHT)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setUniformItemSizes(True)
        self.viewport().setCursor(Qt.CursorShape.PointingHandCursor)
        self.itemClicked.connect(lambda item: self.picked.emit(item.data(Qt.ItemDataRole.UserRole)))

    def fill(self, values: list[int], chosen: int) -> None:
        self.clear()
        for value in values:
            item = QListWidgetItem(_pad(value))
            item.setData(Qt.ItemDataRole.UserRole, value)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setSizeHint(QSize(COLUMN_WIDTH - 12, 32))
            if value == chosen:
                font = QFont(item.font())
                font.setBold(True)
                item.setFont(font)
            self.addItem(item)
        row = values.index(chosen) if chosen in values else 0
        self.setCurrentRow(row if chosen in values else -1)
        self.scrollToItem(self.item(row), QListWidget.ScrollHint.PositionAtCenter)


class TimePopup(QFrame):
    closed = Signal()

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent, Qt.WindowType.Popup)
        self.setObjectName("timePopup")
        self.hours = _Column()
        self.hours.setObjectName("timeHours")
        self.minutes = _Column()
        self.minutes.setObjectName("timeMinutes")
        self.divider = QFrame(objectName="timeDivider")
        self.divider.setFixedWidth(1)
        self.clear_button = QPushButton(objectName="timeClear")
        self.clear_button.setCursor(Qt.CursorShape.PointingHandCursor)
        columns = QHBoxLayout()
        columns.setSpacing(4)
        columns.addWidget(self.hours)
        columns.addWidget(self.divider)
        columns.addWidget(self.minutes)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)
        layout.addLayout(columns)
        layout.addWidget(self.clear_button)

    def hideEvent(self, event) -> None:  # noqa: N802 - Qt API
        super().hideEvent(event)
        self.closed.emit()


class TimePicker(QPushButton):
    """A button with a clock and the time ("HH:MM", or "--:--" when empty)."""

    edited = Signal(str)  # the user's choice, reported when the list closes; "" = cleared

    def __init__(self, *, clearable: bool = False, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("timePicker")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setIconSize(QSize(15, 15))
        self._value = ""
        self._before = ""  # the value when the list opened
        self._clearable = clearable
        self.popup = TimePopup(self)
        self.popup.hours.picked.connect(self._on_hour)
        self.popup.minutes.picked.connect(self._on_minute)
        self.popup.clear_button.clicked.connect(self._on_clear)
        self.popup.closed.connect(self._on_closed)
        self.clicked.connect(self.open_list)
        self.set_icon_color("#9aa0ac")
        self._paint()

    @property
    def value(self) -> str:
        return self._value

    @property
    def hour(self) -> int:
        return int(self._value.split(":")[0]) if self._value else -1

    @property
    def minute(self) -> int:
        return int(self._value.split(":")[1]) if self._value else -1

    def set_value(self, value: str) -> None:
        """From outside (Kimai, a reset): no `edited`."""
        self._value = value
        self._paint()

    def clear(self) -> None:
        self.set_value("")

    def set_icon_color(self, color: str) -> None:
        self.setIcon(glyph("clock", color, 15))

    def set_clear_text(self, text: str) -> None:
        self.popup.clear_button.setText(text)

    def minute_steps(self) -> list[int]:
        steps = list(range(0, 60, 5))
        if self.minute >= 0 and self.minute not in steps:
            steps = sorted([*steps, self.minute])
        return steps

    def open_list(self) -> None:
        self._before = self._value
        self._fill()
        self.popup.clear_button.setVisible(self._clearable and bool(self._value))
        self.popup.adjustSize()
        self.popup.move(self.mapToGlobal(QPoint(0, self.height() + 4)))
        self.popup.show()
        self.popup.hours.setFocus(Qt.FocusReason.PopupFocusReason)

    def choose(self, hour: int, minute: int) -> None:
        self._value = f"{_pad(hour)}:{_pad(minute)}"
        self._paint()

    def _fill(self) -> None:
        self.popup.hours.fill(list(range(24)), self.hour)
        self.popup.minutes.fill(self.minute_steps(), self.minute)

    def _on_hour(self, hour: int) -> None:
        self.choose(hour, max(0, self.minute))
        self._fill()

    def _on_minute(self, minute: int) -> None:
        self.choose(max(0, self.hour), minute)
        self.popup.hide()

    def _on_clear(self) -> None:
        self.clear()
        self.popup.hide()

    def _on_closed(self) -> None:
        if self._value != self._before:
            self._before = self._value
            self.edited.emit(self._value)

    def _paint(self) -> None:
        self.setText(self._value or PLACEHOLDER)
        self.setProperty("empty", "false" if self._value else "true")
        self.style().unpolish(self)
        self.style().polish(self)
