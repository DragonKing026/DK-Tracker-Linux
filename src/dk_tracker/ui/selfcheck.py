"""`python3 -m dk_tracker.ui.selfcheck` — does this installation of the app start at all? (0086)

Loads every Qt module the app uses, builds the real main window from QML and the quick window, without a
desktop (offscreen) and without touching the user's settings or token. Exit code 0 and one line per check;
anything else means the package is broken on this runtime. The Qt guard in CI runs it against the published
package (.github/workflows/straznik.yml); after a runtime or Qt update it is the first thing to try.
"""

from __future__ import annotations

import os
import sys


def run() -> list[str]:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    import PySide6
    from PySide6 import QtCore, QtNetwork, QtQml, QtQuick, QtQuickControls2, QtSvg  # noqa: F401
    from PySide6.QtWidgets import QApplication

    from . import placement
    from .main_window.bridge import MainBridge
    from .main_window.window import MainWindow

    app = QApplication.instance() or QApplication(sys.argv[:1])
    report = [f"PySide6 {PySide6.__version__}, Qt {QtCore.qVersion()}, platform {app.platformName()}"]
    window = MainWindow(MainBridge())
    report.append(f"main window: {type(window.window).__name__} from QML")
    window.engine.deleteLater()
    report.append(f"layer-shell-qt: {'loads' if placement.layer_available() else 'not available'}")
    return report


def main() -> int:
    try:
        for line in run():
            print(line)
    except Exception as error:  # noqa: BLE001 — any failure means the installation is broken
        print(f"FAILED: {type(error).__name__}: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
