"""Repro issue #1 (0081): log every paint of the layer canvas and where the header is at that moment.

Run on a KDE Wayland session from the repo root (the system PySide6, so layer-shell works):
    PYTHONPATH=src:. /usr/bin/python3 TODO/W-TRAKCIE/0081-smieciowe-piksele-przy-starcie/testy/\
odtworz_malowanie_plotna.py
"""

import sys
from datetime import timedelta

from PySide6.QtCore import QEvent, QObject, QPoint, QSize, QTimer
from PySide6.QtWidgets import QApplication

from dk_tracker.core.i18n import Translator
from dk_tracker.core.settings import Settings
from dk_tracker.core.tracker import Snapshot, Totals
from dk_tracker.ui import placement
from dk_tracker.ui.popup import QuickWindow
from dk_tracker.ui.state import AppState
from tests.core.fakes import NOW, FakeClient, make_entry

LOGGED = (
    QEvent.Type.Resize,
    QEvent.Type.Show,
    QEvent.Type.LayoutRequest,
    QEvent.Type.UpdateRequest,
    QEvent.Type.Paint,
)


class Spy(QObject):
    def __init__(self, popup: QuickWindow) -> None:
        super().__init__()
        self.popup = popup

    def eventFilter(self, watched, event) -> bool:  # noqa: N802 - Qt API
        if watched is self.popup and event.type() in LOGGED:
            popup = self.popup
            region = f"region={event.region().boundingRect()}" if event.type() == QEvent.Type.Paint else ""
            margins = popup.layout().contentsMargins()
            header = popup.header.mapTo(popup, QPoint(0, 0))
            print(
                event.type().name,
                region,
                "header@",
                header,
                popup.header.width(),
                "margins",
                margins.left(),
                margins.top(),
                flush=True,
            )
        return False


def main() -> None:
    app = QApplication(sys.argv[:1])
    state = AppState(Settings(url="https://kimai.test"), Translator("pl"))
    popup = QuickWindow(state, now=lambda: NOW)
    recent = (make_entry(3, NOW - timedelta(hours=3), NOW - timedelta(hours=2)),)
    state.update(
        configured=True,
        snapshot=Snapshot(user=FakeClient().user, totals=Totals(today=3600, week=7200), recent=recent),
    )
    mode = placement.apply(popup, "layer")
    popup.set_preferred_size(QSize(700, 650))
    print("mode", mode, "size", popup.size(), "panel", popup.panel_rect())
    spy = Spy(popup)
    popup.installEventFilter(spy)
    popup.show()
    QTimer.singleShot(700, lambda: (print("--- shrink"), popup.set_preferred_size(QSize(500, 480))))
    QTimer.singleShot(1500, app.quit)
    app.exec()


if __name__ == "__main__":
    main()
