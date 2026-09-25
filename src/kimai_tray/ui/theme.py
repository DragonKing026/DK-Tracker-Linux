"""Colours of the WS Tracker add-on (popup/popup.css), light and dark, following the system.

The add-on switches on `prefers-color-scheme`; here Qt reports the scheme (through the
desktop portal on KDE and GNOME) and the window colour decides when it cannot tell.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

LIGHT = {
    "bg": "#ffffff",
    "surface": "#f7f8fa",
    "surface2": "#eceef2",
    "fg": "#17181c",
    "muted": "#71757f",
    "line": "#e3e5ea",
    "accent": "#2563eb",
    "start": "#16a34a",
    "stop": "#e02f2f",
    "ok_bg": "#eaf7ee",
    "ok_fg": "#12703a",
    "err_bg": "#fdecec",
    "err_fg": "#a41d1d",
    "focus": "#2563eb",
}
DARK = {
    **LIGHT,
    "bg": "#16181d",
    "surface": "#1e2127",
    "surface2": "#272b33",
    "fg": "#eceef2",
    "muted": "#9aa0ac",
    "line": "#2f333c",
    "accent": "#6f9bff",
    "ok_bg": "#14301f",
    "ok_fg": "#6ee7a0",
    "err_bg": "#3a1a1a",
    "err_fg": "#ff9d9d",
    "focus": "#7aa2ff",
}
PROJECT_NONE = "line"  # palette key of the grey dot when no project is chosen


def palette_for(scheme: Qt.ColorScheme, window: QColor) -> dict[str, str]:
    if scheme == Qt.ColorScheme.Dark:
        return DARK
    if scheme == Qt.ColorScheme.Light:
        return LIGHT
    return DARK if window.lightness() < 128 else LIGHT


def stylesheet(p: dict[str, str]) -> str:
    """QSS for the quick window; widgets are addressed by objectName, as popup.css does by id."""
    return f"""
#popup {{ background: {p["bg"]}; color: {p["fg"]}; font-size: 14px; }}
#popup QLabel {{ color: {p["fg"]}; background: transparent; }}
#header {{ background: {p["surface"]}; border-bottom: 1px solid {p["line"]}; }}
#brand {{ font-size: 13px; font-weight: 600; }}
#brandDim {{ color: {p["muted"]}; font-size: 13px; }}
#popup QLabel#totals {{ color: {p["muted"]}; font-size: 12px; }}
#iconButton {{ border: 0; border-radius: 7px; background: transparent; padding: 6px; }}
#iconButton:hover {{ background: {p["surface2"]}; }}
#description {{ border: 1px solid {p["line"]}; border-radius: 8px; background: {p["surface"]};
    color: {p["fg"]}; font-size: 15px; padding: 6px 8px; }}
#description:focus, #popup QLineEdit:focus {{ border: 1px solid {p["focus"]}; }}
#clock {{ font-size: 12px; font-weight: 600; }}
#toggle {{ border: 0; border-radius: 21px; min-width: 42px; max-width: 42px; min-height: 42px; max-height: 42px; }}
#toggle[state="start"] {{ background: {p["start"]}; }}
#toggle[state="stop"] {{ background: {p["stop"]}; }}
#toggle:disabled {{ background: {p["surface2"]}; }}
#popup QComboBox {{ border: 1px solid {p["line"]}; border-radius: 8px; background: {p["surface"]};
    color: {p["fg"]}; min-height: 32px; padding: 0 9px; font-size: 13px; }}
#popup QComboBox:disabled {{ color: {p["muted"]}; background: {p["surface2"]}; border-style: dashed; }}
#popup QComboBox QAbstractItemView {{ background: {p["bg"]}; color: {p["fg"]};
    selection-background-color: {p["surface2"]}; selection-color: {p["fg"]}; }}
#billable {{ border: 1px solid {p["start"]}; border-radius: 8px; background: rgba(22, 163, 74, 26);
    min-width: 32px; max-width: 32px; min-height: 32px; max-height: 32px; }}
#billable[on="false"] {{ border-color: {p["line"]}; background: {p["surface"]}; }}
#billable:disabled {{ border-style: dashed; }}
#times {{ border: 1px solid {p["line"]}; border-radius: 8px; background: {p["surface"]}; }}
#timesLabel, #hint {{ color: {p["muted"]}; font-size: 11px; }}
#popup QLineEdit {{ border: 1px solid {p["line"]}; border-radius: 6px; background: {p["bg"]};
    color: {p["fg"]}; min-height: 28px; padding: 0 8px; font-size: 13px; }}
#popup QLabel#error {{ margin: 0 14px 12px 14px; background: {p["err_bg"]}; color: {p["err_fg"]}; border-radius: 8px; padding: 8px 10px; font-size: 12px; }}
#popup QLabel#saved {{ margin: 0 14px 12px 14px; background: {p["ok_bg"]}; color: {p["ok_fg"]}; border-radius: 8px; padding: 8px 10px; font-size: 12px; }}
#popup QLabel#warning {{ margin: 0 14px 12px 14px; background: {p["surface2"]}; color: {p["fg"]}; border-radius: 8px; padding: 8px 10px; font-size: 12px; }}
#recentHead, #popup QLabel#recentDayName, #popup QLabel#recentDaySum {{ color: {p["muted"]}; font-size: 10px; font-weight: 700; }}
#recentPanel {{ border-top: 1px solid {p["line"]}; }}
#day {{ background: {p["bg"]}; border-bottom: 1px solid {p["line"]}; }}
#entry {{ border-bottom: 1px solid {p["line"]}; }}
#entry:hover {{ background: {p["surface"]}; }}
#popup QLabel#entryDesc {{ font-size: 13px; }}
#popup QLabel#entryDescEmpty {{ font-size: 13px; color: {p["muted"]}; font-style: italic; }}
#popup QLabel#entryMeta, #popup QLabel#entrySpan {{ color: {p["muted"]}; font-size: 11px; }}
#popup QLabel#entryDuration {{ font-size: 13px; font-weight: 600; }}
#rowBillable {{ border: 0; border-radius: 11px; background: transparent; }}
#rowBillable:hover {{ background: {p["surface2"]}; }}
#resume {{ border: 0; border-radius: 13px; background: {p["surface2"]};
    min-width: 26px; max-width: 26px; min-height: 26px; max-height: 26px; }}
#resume:hover {{ background: {p["start"]}; }}
#recentList, #recentList > QWidget > QWidget {{ background: {p["bg"]}; border: 0; }}
#popup QLabel#empty {{ color: {p["muted"]}; font-size: 12px; }}
#allEntries {{ border: 0; border-top: 1px solid {p["line"]}; background: {p["surface"]}; color: {p["accent"]};
    font-size: 12px; font-weight: 600; text-align: left; padding: 10px 14px; }}
#allEntries:hover {{ text-decoration: underline; }}
#primary {{ border: 0; border-radius: 8px; background: {p["accent"]}; color: #ffffff;
    min-height: 40px; font-size: 14px; font-weight: 600; }}
#popup QLabel#notConfigured {{ color: {p["muted"]}; font-size: 13px; }}
"""
