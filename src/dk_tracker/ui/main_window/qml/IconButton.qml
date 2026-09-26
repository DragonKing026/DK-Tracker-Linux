// An icon button: no background until the pointer is over it. The glyph keeps its own colour
// (Basic would tint it). `danger`: red background and a white glyph under the pointer, as a
// window's own close button.
import QtQuick
import QtQuick.Controls

ToolButton {
    id: button
    property string glyph: ""
    property color tint: app.palette.muted
    property string tip: ""
    property bool danger: false
    readonly property color ink: !enabled ? app.palette.placeholder : danger && hovered ? "#ffffff" : tint
    implicitWidth: 32
    implicitHeight: 32
    icon.source: glyph ? "image://glyph/" + glyph + "/" + ink.toString().slice(1, 7) : ""
    icon.color: "transparent"
    icon.width: 18
    icon.height: 18
    HoverHandler { cursorShape: button.enabled ? Qt.PointingHandCursor : Qt.ArrowCursor }
    ToolTip.visible: hovered && tip !== ""
    ToolTip.text: tip
    background: Rectangle {
        radius: 4
        color: !button.enabled || !(button.hovered || button.down) ? "transparent"
             : button.danger ? app.palette.danger
             : button.down ? app.palette.control_down : app.palette.control_hover
    }
}
