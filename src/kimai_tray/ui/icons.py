"""Icons drawn at runtime: the tray icon (F-02, variant C chosen by the user) and the small
glyphs of the window, taken from the add-on's SVG markup so the look stays the same."""

from __future__ import annotations

from importlib import resources

from PySide6.QtCore import QByteArray, QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QIcon, QPainter, QPen, QPixmap
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
}
GLYPHS = tuple(_PATHS)


def app_icon() -> QIcon:
    """The Kimai logo (public/touch-icon-512x512.png of Kimai, AGPL-3.0-or-later)."""
    data = resources.files("kimai_tray.ui").joinpath("assets", "kimai.png").read_bytes()
    pixmap = QPixmap()
    pixmap.loadFromData(data)
    return QIcon(pixmap)


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
        font = QFont()
        font.setBold(True)
        font.setPixelSize(max(6, round(size * (0.62 if len(label) <= 2 else 0.47))))
        painter.setFont(font)
        painter.setPen(QColor("white"))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, label)
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
