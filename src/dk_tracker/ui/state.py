"""What the UI shows, in one place: the last Snapshot plus settings, language and flags.

Widgets never ask the tracker; they read this and redraw on `changed` (spec, section 5).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from PySide6.QtCore import QObject, Signal

from dk_tracker.core.settings import Settings
from dk_tracker.core.tracker import Snapshot


class AppState(QObject):
    changed = Signal()

    def __init__(self, settings: Settings, t: Callable[..., str], parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.snapshot = Snapshot()
        self.settings = settings
        self.t = t
        self.configured = False  # address and token known
        self.secrets_problem: str | None = None  # i18n key: "secretsUnavailable" | "secretsLocked"
        self.warnings: list[tuple[str, dict[str, object]]] = []  # standing notes: timezone, no tray

    def update(self, **changes: Any) -> None:
        for name, value in changes.items():
            if not hasattr(self, name):
                raise AttributeError(name)
            setattr(self, name, value)
        self.changed.emit()
