"""Colours of the WS Tracker add-on (popup/popup.css), light and dark, following the system.

The add-on switches on `prefers-color-scheme`; here Qt reports the scheme (through the
desktop portal on KDE and GNOME) and the window colour decides when it cannot tell.
"""

from __future__ import annotations

import os
from pathlib import Path

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


_CHEVRON = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 12"><path d="M3 4.5 6 7.5 9 4.5" fill="none" '
    'stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
)


def write_assets(p: dict[str, str], directory: Path | None = None) -> dict[str, str]:
    """QSS can only take images from files: the smooth combo-box chevron, in the palette's colours."""
    cache = os.environ.get("XDG_CACHE_HOME") or str(Path.home() / ".cache")
    directory = directory or Path(cache) / "ws-tracker-tray" / "theme"
    assets = {}
    try:
        directory.mkdir(parents=True, exist_ok=True)
        for name, color in (("chevron", p["muted"]), ("chevron_disabled", p["line"])):
            path = directory / f"{name}-{color.lstrip('#')}.svg"
            path.write_text(_CHEVRON.format(color=color), encoding="utf-8")
            assets[name] = path.as_posix()
    except OSError:
        return {}  # a read-only or full cache only costs the smooth arrows: Qt draws its own
    return assets


def stylesheet(p: dict[str, str], assets: dict[str, str] | None = None) -> str:
    """QSS for the quick window; widgets are addressed by objectName, as popup.css does by id."""
    assets = assets or {}
    arrows = (
        f"""
#popup QComboBox::down-arrow {{ image: url("{assets["chevron"]}"); width: 12px; height: 12px; }}
#popup QComboBox::down-arrow:disabled {{ image: url("{assets["chevron_disabled"]}"); }}"""
        if assets
        else ""
    )
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
#popup QComboBox::drop-down {{ subcontrol-origin: padding; subcontrol-position: center right; width: 26px; border: 0; }}{arrows}
#popup QScrollBar:vertical {{ background: transparent; width: 8px; margin: 2px 1px; }}
#popup QScrollBar::handle:vertical {{ background: {p["line"]}; border-radius: 3px; min-height: 28px; }}
#popup QScrollBar::handle:vertical:hover {{ background: {p["muted"]}; }}
#popup QScrollBar::add-line:vertical, #popup QScrollBar::sub-line:vertical {{ height: 0; border: 0; }}
#popup QScrollBar::add-page:vertical, #popup QScrollBar::sub-page:vertical {{ background: none; }}
#projectPopup {{ background: {p["bg"]}; border: 1px solid {p["line"]}; border-radius: 8px; }}
#projectPopup QListView {{ background: {p["bg"]}; color: {p["fg"]}; border: 0; font-size: 13px;
    selection-background-color: {p["surface2"]}; selection-color: {p["fg"]}; }}
#projectPopup QListView::item {{ padding: 4px 6px; }}
#projectPopup QListView::item:disabled {{ color: {p["muted"]}; font-weight: 700; }}
#popup QComboBox QAbstractItemView {{ background: {p["bg"]}; color: {p["fg"]};
    selection-background-color: {p["surface2"]}; selection-color: {p["fg"]}; }}
#billable {{ border: 1px solid {p["start"]}; border-radius: 8px; background: rgba(22, 163, 74, 26);
    min-width: 32px; max-width: 32px; min-height: 32px; max-height: 32px; }}
#billable:hover {{ background: rgba(22, 163, 74, 60); }}
#billable[on="false"] {{ border-color: {p["muted"]}; background: {p["surface"]}; }}
#billable[on="false"]:hover {{ background: {p["surface2"]}; }}
#billable:disabled {{ border-style: dashed; border-color: {p["line"]}; }}
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
#rowBillable {{ border: 1px solid {p["line"]}; border-radius: 11px; background: transparent; }}
#rowBillable[on="true"] {{ border-color: {p["start"]}; background: rgba(22, 163, 74, 30); }}
#rowBillable:hover {{ background: {p["surface2"]}; }}
#rowBillable:disabled {{ border-style: dashed; }}
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
