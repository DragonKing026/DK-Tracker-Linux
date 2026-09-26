"""The small DK Tracker mark: green ring and bigger letters in the text colour (currentColor), no tile."""
import sys
from pathlib import Path
from PySide6.QtGui import QGuiApplication, QPainterPath, QFont
app = QGuiApplication([])
font = QFont("DejaVu Sans"); font.setBold(True); font.setPixelSize(104)
text = QPainterPath(); text.addText(0, 0, font, "DK")
box = text.boundingRect()
text.translate(128 - box.center().x(), 128 - box.center().y())
def d(path):
    out = []
    for i in range(path.elementCount()):
        e = path.elementAt(i)
        if e.isMoveTo(): out.append(f"M{e.x:.1f} {e.y:.1f}")
        elif e.isLineTo(): out.append(f"L{e.x:.1f} {e.y:.1f}")
        elif e.isCurveTo():
            c2, end = path.elementAt(i + 1), path.elementAt(i + 2)
            out.append(f"C{e.x:.1f} {e.y:.1f} {c2.x:.1f} {c2.y:.1f} {end.x:.1f} {end.y:.1f}")
    return "".join(out) + "Z"
print(f"box {box.width():.0f}x{box.height():.0f}", file=sys.stderr)
Path(sys.argv[1]).write_text(f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <!-- DK Tracker mark for small sizes (window header): no tile; letters take the theme's text colour. -->
  <circle cx="128" cy="128" r="114" fill="none" stroke="#22c55e" stroke-opacity="0.25" stroke-width="24"/>
  <path d="M128 14 A114 114 0 1 1 29.3 71" fill="none" stroke="#22c55e" stroke-width="24" stroke-linecap="round"/>
  <path d="{d(text)}" fill="currentColor"/>
</svg>
""")
