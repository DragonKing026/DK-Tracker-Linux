// A check box of the main window: a rounded box in the theme's colours, a pointer under the mouse.
import QtQuick
import QtQuick.Controls

CheckBox {
    id: box
    HoverHandler { cursorShape: Qt.PointingHandCursor }
    indicator: Rectangle {
        x: box.leftPadding
        y: (box.height - height) / 2
        implicitWidth: 20
        implicitHeight: 20
        radius: 5
        color: box.checked ? (app.palette.accent || "#6f9bff") : (app.palette.bg || "#16181d")
        border.width: box.checked ? 0 : 1
        border.color: box.hovered ? (app.palette.muted || "#9aa0ac") : (app.palette.line || "#2f333c")
        Image {
            anchors.centerIn: parent
            visible: box.checked
            source: "image://glyph/check/ffffff"
            sourceSize.width: 14
            sourceSize.height: 14
        }
    }
    contentItem: Label {
        leftPadding: box.indicator.width + 10
        text: box.text
        color: app.palette.fg || "#eceef2"
        wrapMode: Text.Wrap
        verticalAlignment: Text.AlignVCenter
    }
}
