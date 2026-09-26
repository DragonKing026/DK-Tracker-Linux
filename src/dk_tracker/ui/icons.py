"""Icons drawn at runtime: the tray icon (F-02, variant C chosen by the user) and the small
glyphs of the window, taken from the add-on's SVG markup so the look stays the same."""

from __future__ import annotations

from importlib import resources

from PySide6.QtCore import QByteArray, QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QFontMetrics, QIcon, QPainter, QPen, QPixmap
from PySide6.QtSvg import QSvgRenderer

GREY, GREEN, RED = "#6b7280", "#16a34a", "#dc2626"  # background.js badge colours
TRAY_SIZES = (16, 22, 24, 32, 44, 48, 64)

_PATHS = {
    "play": '<path fill="currentColor" d="M8 5v14l11-7z"/>',
    "stop": '<rect fill="currentColor" x="7" y="7" width="10" height="10" rx="1.5"/>',
    "gear": (
        '<g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83'
        "l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4"
        "a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.6 15a1.65 1.65 0 0 0"
        "-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83"
        "l.06.06A1.65 1.65 0 0 0 9 4.6 1.65 1.65 0 0 0 10 3.09V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51"
        " 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9c.14.35.4.64.73.83"
        'H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></g>'
    ),
    "close": '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M6 6l12 12M18 6 6 18"/>',
    "money": (
        '<g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 2v20"/>'
        '<path d="M17 6.5c0-1.9-2.2-3-5-3s-5 1.1-5 3 2.2 3 5 3.5 5 1.6 5 3.5-2.2 3-5 3-5-1.1-5-3"/></g>'
    ),
    "money_off": (
        '<g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 2v20"/>'
        '<path d="M17 6.5c0-1.9-2.2-3-5-3s-5 1.1-5 3 2.2 3 5 3.5 5 1.6 5 3.5-2.2 3-5 3-5-1.1-5-3"/>'
        '<path d="M3 21 21 3"/></g>'
    ),
    "external": (
        '<g fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M14 4h6v6"/><path d="M20 4 10 14"/><path d="M19 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h5"/></g>'
    ),
    # Plan 5, the main window (lucide-style outlines, 24 x 24).
    "timer": (
        '<g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">'
        '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 2.5M10 2h4"/></g>'
    ),
    "pencil": (
        '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        'd="M17 3a2.8 2.8 0 0 1 4 4L7.5 20.5 2 22l1.5-5.5z"/>'
    ),
    "dots": (
        '<g fill="currentColor"><circle cx="12" cy="5" r="1.8"/><circle cx="12" cy="12" r="1.8"/>'
        '<circle cx="12" cy="19" r="1.8"/></g>'
    ),
    "lock": (
        '<g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">'
        '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></g>'
    ),
    "list": (
        '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        'd="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>'
    ),
    "plus": '<path fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" d="M12 5v14M5 12h14"/>',
    "trash": (
        '<g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6M10 11v6M14 11v6"/></g>'
    ),
}
GLYPHS = tuple(_PATHS)


def app_icon() -> QIcon:
    """Our own icon (data/icons/dk-tracker.svg rendered to 512 px), not Kimai's logo: Kimai's
    trademark policy forbids looking like an official Kimai app. A small margin keeps it off
    title-bar edges."""
    data = resources.files("dk_tracker.ui").joinpath("assets", "dk-tracker.png").read_bytes()
    logo = QPixmap()
    logo.loadFromData(data)
    icon = QIcon()
    for size in (16, 22, 24, 32, 48, 64, 128, 256):
        margin = max(1, round(size * 0.08))
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.drawPixmap(
            QRectF(margin, margin, size - 2 * margin, size - 2 * margin), logo, QRectF(logo.rect())
        )
        painter.end()
        icon.addPixmap(pixmap)
    return icon


def mark(color: str, size: int) -> QPixmap:
    """The small WS mark for the window header (0065): the icon's dark tile vanished on a dark
    header at 18 px, so this one has no tile and draws the letters in the theme's text colour."""
    svg = resources.files("dk_tracker.ui").joinpath("assets", "dk-tracker-znak.svg").read_text()
    renderer = QSvgRenderer(QByteArray(svg.replace("currentColor", color).encode()))
    pixmap = QPixmap(size * 2, size * 2)  # drawn at 2x: sharp on scaled screens
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    renderer.render(painter)
    painter.end()
    pixmap.setDevicePixelRatio(2)
    return pixmap


def glyph(name: str, color: str, size: int = 20) -> QIcon:
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">{_PATHS[name]}</svg>'
    renderer = QSvgRenderer(QByteArray(svg.replace("currentColor", color).encode()))
    icon = QIcon()
    for scale in (1, 2):
        pixmap = QPixmap(size * scale, size * scale)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        pixmap.setDevicePixelRatio(scale)
        icon.addPixmap(pixmap)
    return icon


def tray_pixmap(kind: str, label: str, size: int) -> QPixmap:
    """Grey clock when nothing runs; the time (or "!") on a coloured square otherwise."""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
    rect = QRectF(0, 0, size, size)
    if not label:
        _clock(painter, rect, GREY)
    else:
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(RED if kind == "error" else GREEN))
        painter.drawRoundedRect(rect, size * 0.2, size * 0.2)
        # The text keeps ~12 % of the icon free on each side, then is shrunk to fit that box.
        inner = rect.adjusted(size * 0.12, size * 0.12, -size * 0.12, -size * 0.12)
        font = QFont()
        font.setBold(True)
        pixels = max(6, round(size * 0.55))
        font.setPixelSize(pixels)
        while pixels > 6 and QFontMetrics(font).horizontalAdvance(label) > inner.width():
            pixels -= 1
            font.setPixelSize(pixels)
        painter.setFont(font)
        painter.setPen(QColor("white"))
        painter.drawText(inner, Qt.AlignmentFlag.AlignCenter, label)
    painter.end()
    return pixmap


def tray_icon(kind: str, label: str) -> QIcon:
    icon = QIcon()
    for size in TRAY_SIZES:
        icon.addPixmap(tray_pixmap(kind, label, size))
    return icon


def _clock(painter: QPainter, rect: QRectF, color: str) -> None:
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor(color))
    painter.drawEllipse(rect)
    pen = QPen(QColor("white"), max(1.5, rect.width() * 0.09))
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(pen)
    centre = rect.center()
    painter.drawLine(centre, centre + QPointF(0, -rect.height() * 0.3))
    painter.drawLine(centre, centre + QPointF(rect.width() * 0.22, 0))
