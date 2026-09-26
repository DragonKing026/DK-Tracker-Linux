// The description: several lines. Enter confirms (`accepted`), Shift+Enter starts a new line, as in
// the quick window. Grows with the text up to `maxLines`, then scrolls.
import QtQuick
import QtQuick.Controls

ScrollView {
    id: box
    property alias text: area.text
    property alias placeholderText: area.placeholderText
    property alias readOnly: area.readOnly
    property alias area: area
    property int maxLines: 4
    signal accepted()
    signal editingFinished()
    implicitHeight: Math.min(area.implicitHeight, area.font.pixelSize * 1.45 * maxLines + 18)
    clip: true
    opacity: enabled ? 1 : 0.7
    ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

    TextArea {
        id: area
        wrapMode: TextEdit.Wrap
        color: app.palette.fg || "#eceef2"
        placeholderTextColor: app.palette.muted || "#9aa0ac"
        selectByMouse: true
        leftPadding: 10
        rightPadding: 10
        topPadding: 8
        bottomPadding: 8
        background: Rectangle {
            radius: 4
            color: app.palette.bg || "#16181d"
            border.width: 1
            border.color: area.activeFocus ? (app.palette.focus || "#7aa2ff") : (app.palette.border || "#5a6270")
        }
        Keys.onReturnPressed: function (event) {
            if (event.modifiers & Qt.ShiftModifier) { event.accepted = false; return }  // a new line
            box.accepted()
        }
        Keys.onEnterPressed: function (event) { box.accepted() }
        onActiveFocusChanged: if (!activeFocus) box.editingFinished()
    }
}
