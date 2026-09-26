// A check box: an 18 px square with an edge; checked — accent with a white tick.
import QtQuick
import QtQuick.Controls

CheckBox {
    id: box
    HoverHandler { cursorShape: box.enabled ? Qt.PointingHandCursor : Qt.ArrowCursor }
    indicator: Rectangle {
        x: box.leftPadding
        y: (box.height - height) / 2
        implicitWidth: 18
        implicitHeight: 18
        radius: 4
        color: box.checked ? app.palette.accent : app.palette.input
        border.width: box.checked ? 0 : 1
        border.color: box.hovered ? app.palette.border_hover : app.palette.border
        Image {
            anchors.centerIn: parent
            visible: box.checked
            source: "image://glyph/check/ffffff"
            sourceSize.width: 13
            sourceSize.height: 13
        }
    }
    contentItem: Label {
        leftPadding: box.indicator.width + 10
        text: box.text
        color: box.enabled ? app.palette.fg : app.palette.muted
        wrapMode: Text.Wrap
        verticalAlignment: Text.AlignVCenter
    }
}
