// A button of the main window: rounded, a pointer under the mouse; `highlighted` = the main action.
import QtQuick
import QtQuick.Controls

Button {
    id: button
    leftPadding: 14
    rightPadding: 14
    topPadding: 8
    bottomPadding: 8
    opacity: enabled ? 1 : 0.7  // the whole button: pickers bring their own label
    HoverHandler { cursorShape: button.enabled ? Qt.PointingHandCursor : Qt.ArrowCursor }
    contentItem: Label {
        text: button.text
        font: button.font
        color: button.highlighted ? (app.palette.accent || "#6f9bff") : (app.palette.fg || "#eceef2")
        elide: Text.ElideRight
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
    // The main action: the accent as a tint and a thin border, not a bright block (live test).
    background: Rectangle {
        radius: 4
        readonly property color accent: app.palette.accent || "#6f9bff"
        color: button.highlighted
               ? (button.down || button.hovered ? (app.palette.control_hover || "#363c48") : (app.palette.control || "#2c313b"))
               : button.down || button.hovered ? (app.palette.control_hover || "#424a5a") : (app.palette.control || "#353b48")
        border.width: 1
        border.color: button.highlighted ? Qt.rgba(accent.r, accent.g, accent.b, 0.45) : (app.palette.border || "#6b7486")
    }
}
