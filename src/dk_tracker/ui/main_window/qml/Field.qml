// A text field of the main window: rounded, in the theme's colours (Basic draws square white ones).
import QtQuick
import QtQuick.Controls

TextField {
    id: field
    color: app.palette.fg || "#eceef2"
    opacity: enabled ? 1 : 0.7
    placeholderTextColor: app.palette.muted || "#9aa0ac"
    selectByMouse: true
    leftPadding: 10
    rightPadding: 10
    topPadding: 8
    bottomPadding: 8
    background: Rectangle {
        radius: 4
        color: field.enabled ? (app.palette.input || "#0d0f13") : (app.palette.panel || "#262b35")
        border.width: 1
        border.color: field.activeFocus ? (app.palette.focus || "#7aa2ff") : (app.palette.border || "#6b7486")
    }
}
