// A flat icon button: the glyph keeps its own colour (Basic would tint it with the text colour,
// and a green "$" looked like a grey one), a background only under the pointer.
import QtQuick
import QtQuick.Controls

ToolButton {
    id: button
    property string glyph: ""
    property string tint: app.palette.muted || "#9aa0ac"
    property string tip: ""
    implicitWidth: 32
    opacity: enabled ? 1 : 0.4
    implicitHeight: 32
    icon.source: glyph ? "image://glyph/" + glyph + "/" + tint.replace("#", "") : ""
    icon.color: "transparent"
    icon.width: 18
    icon.height: 18
    HoverHandler { cursorShape: button.enabled ? Qt.PointingHandCursor : Qt.ArrowCursor }
    ToolTip.visible: hovered && tip !== ""
    ToolTip.text: tip
    background: Rectangle {
        radius: 4
        color: button.down ? (app.palette.line || "#2f333c")
                           : (button.hovered && button.enabled ? (app.palette.surface2 || "#272b33") : "transparent")
    }
}
