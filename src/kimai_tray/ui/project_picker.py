"""The project picker: a combo box whose list opens with a search field on top (like Select2).

Not in the add-on — the user asked for it, because a company Kimai has many projects. Typing
filters projects by their name or their customer's, ignoring case and Polish letters; Enter
takes the first match, arrows move through projects (customer headers are not choices).
"""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QModelIndex, QPoint, QSortFilterProxyModel, Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QComboBox, QFrame, QLineEdit, QListView, QVBoxLayout, QWidget

from kimai_tray.core.grouping import sort_key

LIST_HEIGHT = 320


class _Filter(QSortFilterProxyModel):
    """Keeps a project when its name or its customer matches; a header when any of its projects does."""

    def __init__(self) -> None:
        super().__init__()
        self._needle = ""

    def set_text(self, text: str) -> None:
        self.beginFilterChange()  # Qt 6.10+: replaces the deprecated invalidateFilter()
        self._needle = sort_key(text.strip())
        self.endFilterChange(QSortFilterProxyModel.Direction.Rows)

    def filterAcceptsRow(self, row: int, parent: QModelIndex) -> bool:  # noqa: N802 - Qt API
        model = self.sourceModel()
        if not self._needle:
            return True
        if row == 0:
            return False  # "choose a project" is a placeholder, never a result
        if _is_header(model, row):
            return any(self._matches(model, child) for child in _children(model, row))
        return self._matches(model, row)

    def _matches(self, model, row: int) -> bool:
        customer = _header_of(model, row)
        text = f"{model.index(row, 0).data() or ''} {customer}"
        return self._needle in sort_key(text)


def _is_header(model, row: int) -> bool:
    item = model.index(row, 0)
    return model.data(item, Qt.ItemDataRole.UserRole) is None and row > 0


def _children(model, row: int) -> list[int]:
    rows = []
    for child in range(row + 1, model.rowCount()):
        if _is_header(model, child):
            break
        rows.append(child)
    return rows


def _header_of(model, row: int) -> str:
    for above in range(row - 1, 0, -1):
        if _is_header(model, above):
            return model.index(above, 0).data() or ""
    return ""


class _SearchField(QLineEdit):
    """Up/Down and Enter act on the list below while the cursor stays in the field."""

    def __init__(self, popup: SearchPopup) -> None:
        super().__init__()
        self._popup = popup

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802 - Qt API
        key = event.key()
        if key in (Qt.Key.Key_Down, Qt.Key.Key_Up):
            self._popup.move_current(1 if key == Qt.Key.Key_Down else -1)
        elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self._popup.choose_current()
        elif key == Qt.Key.Key_Escape:
            self._popup.hide()
        else:
            super().keyPressEvent(event)


class SearchPopup(QFrame):
    chosen = Signal(int)  # row in the combo box model

    def __init__(self, combo: QComboBox) -> None:
        super().__init__(combo, Qt.WindowType.Popup)
        self.setObjectName("projectPopup")
        self._filter = _Filter()
        self._filter.setSourceModel(combo.model())
        self.search = _SearchField(self)
        self.view = QListView()
        self.view.setModel(self._filter)
        self.view.setUniformItemSizes(True)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)
        layout.addWidget(self.search)
        layout.addWidget(self.view)
        self.search.textChanged.connect(self._on_text)
        self.view.clicked.connect(self._choose)

    def open_below(self, anchor: QWidget) -> None:
        self.search.clear()
        self._filter.set_text("")
        self.setFixedWidth(anchor.width())
        self.setFixedHeight(
            min(LIST_HEIGHT, 60 + self.view.sizeHintForRow(0) * max(1, self._filter.rowCount()))
        )
        self.move(anchor.mapToGlobal(QPoint(0, anchor.height())))
        self.show()
        self.search.setFocus(Qt.FocusReason.PopupFocusReason)
        self._select_first(from_row=0, step=1)

    def move_current(self, step: int) -> None:
        row = self.view.currentIndex().row()
        self._select_first(from_row=row + step if row >= 0 else 0, step=step)

    def choose_current(self) -> None:
        index = self.view.currentIndex()
        if index.isValid():
            self._choose(index)

    def _on_text(self, text: str) -> None:
        self._filter.set_text(text)
        self._select_first(from_row=0, step=1)

    def _select_first(self, *, from_row: int, step: int) -> None:
        row = from_row
        while 0 <= row < self._filter.rowCount():
            index = self._filter.index(row, 0)
            source = self._filter.mapToSource(index).row()
            if source > 0 and not _is_header(self._filter.sourceModel(), source):
                self.view.setCurrentIndex(index)
                return
            row += step

    def _choose(self, index: QModelIndex) -> None:
        source = self._filter.mapToSource(index).row()
        if source <= 0 or _is_header(self._filter.sourceModel(), source):
            return
        self.hide()
        self.chosen.emit(source)


class ProjectComboBox(QComboBox):
    """Row 0 is the "choose a project" placeholder; rows without data are customer headers."""

    def __init__(self, t: Callable[..., str]) -> None:
        super().__init__()
        self.popup = SearchPopup(self)
        self.popup.chosen.connect(self._on_chosen)
        self.retranslate(t)

    def retranslate(self, t: Callable[..., str]) -> None:
        self.popup.search.setPlaceholderText(t("projectSearch"))

    def showPopup(self) -> None:  # noqa: N802 - Qt API
        self.popup.open_below(self)

    def hidePopup(self) -> None:  # noqa: N802 - Qt API
        self.popup.hide()

    def _on_chosen(self, row: int) -> None:
        self.setCurrentIndex(row)
        self.activated.emit(row)
