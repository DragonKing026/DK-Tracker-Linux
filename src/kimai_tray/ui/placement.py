"""Where the quick window appears (ADR-0005).

KDE Plasma on Wayland: a layer-shell surface anchored bottom-right, just above the panel.
Other desktops: a frameless window (the compositor centres it). No tray host: an ordinary
window with a frame. layer-shell-qt has no Python bindings, so one C++ symbol is called
through ctypes; in 6.7.5 `Window::get()` turns only that window into a layer surface.
"""

from __future__ import annotations

import ctypes
import logging
import os

from PySide6.QtCore import QMargins, QObject, Qt
from PySide6.QtWidgets import QWidget

LAYER_LIBRARY = "libLayerShellQtInterface.so.6"
LAYER_SYMBOL = "_ZN12LayerShellQt6Window3getEP7QWindow"  # LayerShellQt::Window::get(QWindow*)
_ANCHOR_BOTTOM, _ANCHOR_RIGHT = 2, 8
_LAYER_TOP, _KEYBOARD_ON_DEMAND = 2, 2
log = logging.getLogger(__name__)


def choose_mode(platform: str, desktop: str, *, tray_available: bool, layer_available: bool) -> str:
    if not tray_available:
        return "window"
    if platform == "wayland" and "KDE" in desktop.upper().split(":") and layer_available:
        return "layer"
    return "frameless"


def layer_available() -> bool:
    try:
        return hasattr(ctypes.CDLL(LAYER_LIBRARY), LAYER_SYMBOL)
    except OSError:
        return False


def detect_mode(platform: str, tray_available: bool) -> str:
    return choose_mode(
        platform,
        os.environ.get("XDG_CURRENT_DESKTOP", ""),
        tray_available=tray_available,
        layer_available=platform == "wayland" and layer_available(),
    )


def apply(window: QWidget, mode: str) -> str:
    """Configure the window before it is first shown; returns the mode actually used."""
    if mode == "window":
        window.setWindowFlags(Qt.WindowType.Window)
        window.hide_on_deactivate = False
        return mode
    window.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint)
    window.hide_on_deactivate = True
    if mode == "layer" and not _anchor_to_panel(window):
        return "frameless"
    return mode


def _anchor_to_panel(window: QWidget) -> bool:
    try:
        import shiboken6

        window.winId()  # creates the QWindow; layer-shell hooks in when its surface is made
        get = ctypes.CDLL(LAYER_LIBRARY)[LAYER_SYMBOL]
        get.restype, get.argtypes = ctypes.c_void_p, [ctypes.c_void_p]
        pointer = get(shiboken6.getCppPointer(window.windowHandle())[0])
        layer = shiboken6.wrapInstance(pointer, QObject)
        layer.setProperty("anchors", _ANCHOR_BOTTOM | _ANCHOR_RIGHT)
        layer.setProperty("layer", _LAYER_TOP)
        layer.setProperty("keyboardInteractivity", _KEYBOARD_ON_DEMAND)
        layer.setProperty("margins", QMargins(0, 0, 12, 12))
        layer.setProperty("scope", "kimai-tray")
    except (OSError, AttributeError, RuntimeError, ImportError) as error:
        log.warning("layer-shell unavailable, using a frameless window: %s", error)
        return False
    return True
