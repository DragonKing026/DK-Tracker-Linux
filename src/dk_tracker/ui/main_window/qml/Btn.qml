// A button of the main window: rounded, a pointer under the mouse; `highlighted` = the main action.
import QtQuick
import QtQuick.Controls

Button {
    id: button
    leftPadding: 14
    rightPadding: 14
    topPadding: 8
    bottomPadding: 8
    HoverHandler { cursorShape: button.enabled ? Qt.PointingHandCursor : Qt.ArrowCursor }
    contentItem: Label {
        text: button.text
        font: button.font
        color: button.highlighted ? "#ffffff" : (app.palette.fg || "#eceef2")
        opacity: button.enabled ? 1 : 0.5
        elide: Text.ElideRight
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
    background: Rectangle {
        radius: 8
        color: button.highlighted ? (app.palette.accent || "#6f9bff")
             : button.down ? (app.palette.line || "#2f333c")
             : button.hovered ? (app.palette.line || "#2f333c") : (app.palette.surface2 || "#272b33")
        opacity: button.enabled ? (button.highlighted && button.hovered ? 0.9 : 1) : 0.6
    }
}
