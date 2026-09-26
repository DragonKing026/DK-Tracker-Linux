// A text field of the main window: rounded, in the theme's colours (Basic draws square white ones).
import QtQuick
import QtQuick.Controls

TextField {
    id: field
    color: app.palette.fg || "#eceef2"
    placeholderTextColor: app.palette.muted || "#9aa0ac"
    selectByMouse: true
    leftPadding: 10
    rightPadding: 10
    topPadding: 8
    bottomPadding: 8
    background: Rectangle {
        radius: 8
        color: field.enabled ? (app.palette.bg || "#16181d") : (app.palette.surface2 || "#272b33")
        border.width: 1
        border.color: field.activeFocus ? (app.palette.focus || "#7aa2ff") : (app.palette.line || "#2f333c")
    }
}
