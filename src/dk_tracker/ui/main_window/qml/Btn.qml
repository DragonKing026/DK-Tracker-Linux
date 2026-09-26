// A button. `variant`: "default" (control colour, edge), "primary" (accent text and edge — the main
// action, not a bright block), "danger" (red text, icon and edge; red tint under the pointer),
// "flat" (no background until the pointer is over it). Optional `glyph` before the text.
import QtQuick
import QtQuick.Controls

Button {
    id: button
    property string variant: "default"
    property string glyph: ""
    readonly property color ink: !enabled ? app.palette.placeholder
                               : variant === "primary" ? app.palette.accent
                               : variant === "danger" ? app.palette.danger : app.palette.fg
    implicitHeight: 34
    leftPadding: 14
    rightPadding: 14
    HoverHandler { cursorShape: button.enabled ? Qt.PointingHandCursor : Qt.ArrowCursor }
    contentItem: Item {
        implicitWidth: row.implicitWidth
        implicitHeight: row.implicitHeight
        Row {
            id: row
            anchors.centerIn: parent
            spacing: 6
            Image {
                visible: button.glyph !== ""
                anchors.verticalCenter: parent.verticalCenter
                source: button.glyph ? "image://glyph/" + button.glyph + "/" + button.ink.toString().slice(1, 7) : ""
                sourceSize.width: 15
                sourceSize.height: 15
            }
            Label {
                anchors.verticalCenter: parent.verticalCenter
                text: button.text
                font: button.font
                color: button.ink
            }
        }
    }
    background: Rectangle {
        radius: 4
        readonly property bool over: button.enabled && (button.hovered || button.down)
        color: button.variant === "danger" && over ? app.palette.danger_bg
             : button.variant === "flat" && !over ? "transparent"
             : button.down ? app.palette.control_down
             : over ? app.palette.control_hover : app.palette.control
        border.width: button.variant === "flat" ? 0 : 1
        border.color: !button.enabled ? app.palette.divider
                    : button.variant === "primary" ? app.palette.accent
                    : button.variant === "danger" ? app.palette.danger
                    : over ? app.palette.border_hover : app.palette.border
    }
}
