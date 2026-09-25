"""Mock-up of tray icon variants (F-02) at real tray sizes, on dark and light panels.

Run: python3 ikony_makieta.py OUT.png   (system PySide6; throwaway, not product code)
"""

import sys

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QFont, QGuiApplication, QImage, QPainter, QPen

GREY, GREEN, RED, BLUE = "#6b7280", "#16a34a", "#dc2626", "#2563eb"
STATES = [("nic nie trwa", GREY, ""), ("trwa 47 min", GREEN, "47m"), ("trwa 1 h 22", GREEN, "1:22"), ("błąd", RED, "!")]
PANELS = [("ciemny panel", "#2a2e32", "#eff0f1"), ("jasny panel", "#eff0f1", "#232629")]


def clock(p: QPainter, r: QRectF, fill: str) -> None:
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QColor(fill))
    p.drawEllipse(r)
    pen = QPen(QColor("white"), max(1.5, r.width() * 0.09))
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    p.setPen(pen)
    c = r.center()
    p.drawLine(c, c + (r.topLeft() - r.topLeft()) + type(c)(0, -r.height() * 0.3))
    p.drawLine(c, c + type(c)(r.width() * 0.22, 0))


def variant_a(p, r, color, text):
    """Extension clock, whole disc takes the state colour (grey/green/red)."""
    clock(p, r, color if color != GREY else GREY)
    if text == "!":
        clock(p, r, RED)


def variant_b(p, r, color, text):
    """Extension clock (blue) + a small state dot in the corner."""
    clock(p, r.adjusted(0, 0, -r.width() * 0.12, -r.height() * 0.12), BLUE)
    d = r.width() * 0.45
    dot = QRectF(r.right() - d, r.bottom() - d, d, d)
    p.setPen(QPen(QColor("#00000000"), 0))
    p.setBrush(QColor(color))
    p.drawEllipse(dot)


def variant_c(p, r, color, text):
    """Badge like the extension: time text on a coloured rounded square; clock when idle."""
    if not text:
        clock(p, r, GREY)
        return
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QColor(color))
    p.drawRoundedRect(r, r.width() * 0.2, r.height() * 0.2)
    f = QFont("Noto Sans")
    f.setBold(True)
    f.setPixelSize(int(r.height() * (0.62 if len(text) <= 2 else 0.47)))
    p.setFont(f)
    p.setPen(QColor("white"))
    p.drawText(r, Qt.AlignmentFlag.AlignCenter, text)


VARIANTS = [("A: zegar w kolorze stanu", variant_a), ("B: zegar + kropka stanu", variant_b),
            ("C: czas w ikonie (jak badge)", variant_c)]


def main(out: str) -> None:
    app = QGuiApplication(sys.argv)  # noqa: F841
    cell_w, row_h, left, top = 150, 118, 230, 40
    img = QImage(left + cell_w * len(STATES), top + row_h * len(VARIANTS), QImage.Format.Format_ARGB32)
    img.fill(QColor("#ffffff"))
    p = QPainter(img)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setRenderHint(QPainter.RenderHint.TextAntialiasing)
    label = QFont("Noto Sans")
    label.setPixelSize(13)
    p.setFont(label)
    p.setPen(QColor("#17181c"))
    for i, (name, _, _) in enumerate(STATES):
        p.drawText(QRectF(left + i * cell_w, 8, cell_w, 24), Qt.AlignmentFlag.AlignCenter, name)
    for j, (vname, draw) in enumerate(VARIANTS):
        y0 = top + j * row_h
        p.setFont(label)
        p.setPen(QColor("#17181c"))
        p.drawText(QRectF(8, y0, left - 16, row_h), Qt.AlignmentFlag.AlignVCenter | Qt.TextFlag.TextWordWrap, vname)
        for i, (_, color, text) in enumerate(STATES):
            for k, (_, bg, _) in enumerate(PANELS):
                band = QRectF(left + i * cell_w + 4, y0 + 4 + k * (row_h / 2 - 2), cell_w - 8, row_h / 2 - 6)
                p.setPen(Qt.PenStyle.NoPen)
                p.setBrush(QColor(bg))
                p.drawRect(band)
                # 22 px (100 %) and 44 px (200 % HiDPI) side by side, as a panel would show them
                small = QRectF(band.left() + 22, band.center().y() - 11, 22, 22)
                big = QRectF(band.left() + 70, band.center().y() - 22 if band.height() > 44 else band.top() + 2,
                             min(44, band.height() - 4), min(44, band.height() - 4))
                p.save()
                draw(p, small, color, text)
                p.restore()
                p.save()
                draw(p, big, color, text)
                p.restore()
    p.end()
    img.save(out)


if __name__ == "__main__":
    main(sys.argv[1])
