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
        color: button.highlighted ? (app.palette.accent || "#6f9bff") : (app.palette.fg || "#eceef2")
        opacity: button.enabled ? 1 : 0.5
        elide: Text.ElideRight
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
    // The main action: the accent as a tint and a thin border, not a bright block (live test).
    background: Rectangle {
        radius: 5
        readonly property color accent: app.palette.accent || "#6f9bff"
        color: button.highlighted
               ? Qt.rgba(accent.r, accent.g, accent.b, button.down ? 0.32 : (button.hovered ? 0.24 : 0.16))
               : button.down || button.hovered ? (app.palette.line || "#2f333c") : (app.palette.surface2 || "#272b33")
        border.width: button.highlighted ? 1 : 0
        border.color: Qt.rgba(accent.r, accent.g, accent.b, 0.55)
        opacity: button.enabled ? 1 : 0.6
    }
}
