// A number field with − and + (the settings): rounded, a pointer on the buttons.
import QtQuick
import QtQuick.Controls

SpinBox {
    id: spin
    editable: true
    implicitWidth: 150
    contentItem: TextInput {
        text: spin.displayText
        font: spin.font
        color: app.palette.fg || "#eceef2"
        horizontalAlignment: Qt.AlignHCenter
        verticalAlignment: Qt.AlignVCenter
        readOnly: !spin.editable
        validator: spin.validator
        inputMethodHints: Qt.ImhFormattedNumbersOnly
        selectByMouse: true
    }
    up.indicator: Rectangle {
        x: spin.width - width
        height: spin.height
        implicitWidth: 38
        radius: 4
        color: spin.up.hovered ? (app.palette.line || "#2f333c") : (app.palette.surface2 || "#272b33")
        Label { anchors.centerIn: parent; text: "+"; font.pixelSize: 18; color: app.palette.fg || "#eceef2" }
        HoverHandler { cursorShape: Qt.PointingHandCursor }
    }
    down.indicator: Rectangle {
        height: spin.height
        implicitWidth: 38
        radius: 4
        color: spin.down.hovered ? (app.palette.line || "#2f333c") : (app.palette.surface2 || "#272b33")
        Label { anchors.centerIn: parent; text: "−"; font.pixelSize: 18; color: app.palette.fg || "#eceef2" }
        HoverHandler { cursorShape: Qt.PointingHandCursor }
    }
    background: Rectangle {
        implicitHeight: 38
        radius: 4
        color: app.palette.bg || "#16181d"
        border.width: 1
        border.color: spin.activeFocus ? (app.palette.focus || "#7aa2ff") : (app.palette.border || "#5a6270")
    }
}
