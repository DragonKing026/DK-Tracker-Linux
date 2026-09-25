"""Probe: can layer-shell-qt 6.7 make ONE window a layer surface without QT_WAYLAND_SHELL_INTEGRATION?

Shows a layer-shell popup (bottom-right) and an ordinary dialog side by side for a few seconds.
Throwaway; run with system PySide6 on a Plasma Wayland session.
"""

import ctypes
import json
import os
import sys

import shiboken6
from PySide6.QtCore import QMargins, QObject, QTimer
from PySide6.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QVBoxLayout, QWidget

assert "QT_WAYLAND_SHELL_INTEGRATION" not in os.environ
app = QApplication(sys.argv)
popup = QWidget()
popup.resize(460, 300)
QVBoxLayout(popup).addWidget(QLabel("LAYER POPUP (powinno być w prawym dolnym rogu, bez ramki)"))
popup.setStyleSheet("background:#16a34a; color:white; font-size:16px")
popup.winId()
lib = ctypes.CDLL("libLayerShellQtInterface.so.6")
get = lib["_ZN12LayerShellQt6Window3getEP7QWindow"]
get.restype, get.argtypes = ctypes.c_void_p, [ctypes.c_void_p]
layer = shiboken6.wrapInstance(get(shiboken6.getCppPointer(popup.windowHandle())[0]), QObject)
ok = {k: layer.setProperty(k, v) for k, v in {"anchors": 2 | 8, "layer": 2, "keyboardInteractivity": 2,
      "margins": QMargins(0, 0, 12, 12), "scope": "kimai-tray-probe"}.items()}

dialog = QDialog()
dialog.setWindowTitle("Zwykłe okno (ustawienia) — powinno mieć ramkę")
lay = QVBoxLayout(dialog)
lay.addWidget(QLabel("ZWYKŁE OKNO"))
edit = QLineEdit()
lay.addWidget(edit)
dialog.resize(420, 160)
popup.show()
dialog.show()
print(json.dumps({"platform": app.platformName(), "set_ok": ok}), flush=True)
QTimer.singleShot(int(sys.argv[1]) if len(sys.argv) > 1 else 6000, app.quit)
app.exec()
