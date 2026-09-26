// A drop-down list of the main window: rounded, its list rounded too, a pointer under the mouse.
import QtQuick
import QtQuick.Controls

ComboBox {
    id: combo
    HoverHandler { cursorShape: Qt.PointingHandCursor }
    leftPadding: 10
    contentItem: Label {
        leftPadding: 10
        rightPadding: combo.indicator.width + 6
        text: combo.displayText
        color: combo.currentIndex < 0 ? (app.palette.muted || "#9aa0ac") : (app.palette.fg || "#eceef2")
        elide: Text.ElideRight
        verticalAlignment: Text.AlignVCenter
    }
    background: Rectangle {
        implicitHeight: 38
        radius: 8
        color: combo.hovered ? (app.palette.line || "#2f333c") : (app.palette.surface2 || "#272b33")
        border.width: combo.activeFocus ? 1 : 0
        border.color: app.palette.focus || "#7aa2ff"
    }
    popup.background: Rectangle {
        radius: 8
        color: app.palette.surface || "#1e2127"
        border.color: app.palette.line || "#2f333c"
    }
    delegate: ItemDelegate {
        required property var model
        required property int index
        width: combo.width
        highlighted: combo.highlightedIndex === index
        HoverHandler { cursorShape: Qt.PointingHandCursor }
        contentItem: Label {
            text: model[combo.textRole]
            color: app.palette.fg || "#eceef2"
            elide: Text.ElideRight
        }
        background: Rectangle {
            radius: 6
            color: parent.highlighted || parent.hovered ? (app.palette.surface2 || "#272b33") : "transparent"
        }
    }
}
