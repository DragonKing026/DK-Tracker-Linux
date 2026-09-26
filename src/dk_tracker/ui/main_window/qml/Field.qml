// A text field: darker (light theme: white) than what is around it, always with an edge.
import QtQuick
import QtQuick.Controls

TextField {
    id: field
    implicitHeight: 34
    leftPadding: 10
    rightPadding: 10
    color: enabled ? app.palette.fg : app.palette.muted
    placeholderTextColor: app.palette.placeholder
    selectByMouse: true
    HoverHandler { id: hover; cursorShape: Qt.IBeamCursor }
    background: Rectangle {
        radius: 4
        color: field.enabled ? app.palette.input : app.palette.panel
        border.width: 1
        border.color: field.activeFocus ? app.palette.accent
                    : hover.hovered && field.enabled ? app.palette.border_hover : app.palette.border
    }
}
