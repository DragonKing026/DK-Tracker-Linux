// The description in several lines. Enter confirms (`accepted`), Shift+Enter starts a new line, as
// in the quick window. Grows with the text up to `maxLines`, then scrolls.
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
    implicitHeight: Math.min(area.implicitHeight, area.font.pixelSize * 1.45 * maxLines + 16)
    clip: true
    ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

    TextArea {
        id: area
        wrapMode: TextEdit.Wrap
        leftPadding: 10
        rightPadding: 10
        topPadding: 8
        bottomPadding: 8
        color: box.enabled ? app.palette.fg : app.palette.muted
        placeholderTextColor: app.palette.placeholder
        selectByMouse: true
        HoverHandler { id: hover; cursorShape: Qt.IBeamCursor }
        background: Rectangle {
            radius: 4
            color: box.enabled ? app.palette.input : app.palette.panel
            border.width: 1
            border.color: area.activeFocus ? app.palette.accent
                        : hover.hovered && box.enabled ? app.palette.border_hover : app.palette.border
        }
        Keys.onReturnPressed: function (event) {
            if (event.modifiers & Qt.ShiftModifier) { event.accepted = false; return }  // a new line
            box.accepted()
        }
        Keys.onEnterPressed: box.accepted()
        onActiveFocusChanged: if (!activeFocus) box.editingFinished()
    }
}
