"""Build the DK Tracker icon: variant C with the letters as outlines (no font needed where it is shown)."""
import sys
from pathlib import Path
from PySide6.QtGui import QGuiApplication, QPainterPath, QFont, QFontDatabase, QImage, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QByteArray, Qt
app = QGuiApplication([])
font = QFont("DejaVu Sans"); font.setBold(True); font.setPixelSize(68)
text = QPainterPath(); text.addText(0, 0, font, "DK")
box = text.boundingRect()
text.translate(128 - box.center().x(), 128 - box.center().y())
def d(path):
    out = []
    for i in range(path.elementCount()):
        e = path.elementAt(i)
        if e.isMoveTo(): out.append(f"M{e.x:.2f} {e.y:.2f}")
        elif e.isLineTo(): out.append(f"L{e.x:.2f} {e.y:.2f}")
        elif e.isCurveTo():
            c2, end = path.elementAt(i + 1), path.elementAt(i + 2)
            out.append(f"C{e.x:.2f} {e.y:.2f} {c2.x:.2f} {c2.y:.2f} {end.x:.2f} {end.y:.2f}")
    return "".join(out) + "Z"
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <!-- DK Tracker: dark tile, green progress ring, "DK" as outlines (DejaVu Sans Bold). -->
  <rect x="8" y="8" width="240" height="240" rx="56" fill="#1f2937" stroke="#4b5563" stroke-width="4"/>
  <circle cx="128" cy="128" r="88" fill="none" stroke="#374151" stroke-width="20"/>
  <path d="M128 40 A88 88 0 1 1 51.8 84" fill="none" stroke="#22c55e" stroke-width="20" stroke-linecap="round"/>
  <path d="{d(text)}" fill="#ffffff" fill-rule="nonzero"/>
</svg>
"""
Path(sys.argv[1]).write_text(svg)
r = QSvgRenderer(QByteArray(svg.encode()))
img = QImage(512, 512, QImage.Format.Format_ARGB32); img.fill(Qt.GlobalColor.transparent)
p = QPainter(img); p.setRenderHint(QPainter.RenderHint.Antialiasing); r.render(p); p.end()
img.save(sys.argv[2])
