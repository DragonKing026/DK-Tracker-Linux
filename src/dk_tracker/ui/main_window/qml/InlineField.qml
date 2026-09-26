// Text that can be edited in place: it looks like text, and shows it is a field under the pointer
// and while typing (Toggl-style). Tells `app` while it is being edited: a refresh then waits.
import QtQuick
import QtQuick.Controls

TextField {
    id: field
    property string shown: ""  // the value from Kimai; Esc brings it back
    property bool reportEditing: true
    text: shown
    color: app.palette.fg || "#eceef2"
    selectByMouse: true
    leftPadding: 6
    rightPadding: 6
    background: Rectangle {
        radius: 5
        color: field.activeFocus ? (app.palette.bg || "#16181d") : "transparent"
        border.width: field.activeFocus || (hover.hovered && !field.readOnly) ? 1 : 0
        border.color: field.activeFocus ? (app.palette.focus || "#7aa2ff") : (app.palette.line || "#2f333c")
    }
    HoverHandler { id: hover; cursorShape: field.readOnly ? Qt.ArrowCursor : Qt.IBeamCursor }
    Component.onCompleted: cursorPosition = 0  // a long text shows its beginning
    onActiveFocusChanged: {
        if (reportEditing) app.setEditing(activeFocus)
        if (!activeFocus) cursorPosition = 0
    }
    Keys.onEscapePressed: { text = shown; focus = false }
}
