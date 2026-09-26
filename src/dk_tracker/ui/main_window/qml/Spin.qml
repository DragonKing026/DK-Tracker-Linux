// A number with − and + in one frame (the settings).
import QtQuick
import QtQuick.Controls

SpinBox {
    id: spin
    editable: true
    implicitWidth: 140
    implicitHeight: 34
    leftPadding: 34
    rightPadding: 34
    contentItem: TextInput {
        text: spin.displayText
        font: spin.font
        color: app.palette.fg
        horizontalAlignment: Qt.AlignHCenter
        verticalAlignment: Qt.AlignVCenter
        readOnly: !spin.editable
        validator: spin.validator
        inputMethodHints: Qt.ImhFormattedNumbersOnly
        selectByMouse: true
    }
    component Step: Rectangle {
        property bool over: false
        property string sign: ""
        implicitWidth: 34
        radius: 4
        color: over ? app.palette.control_hover : app.palette.control
        Label { anchors.centerIn: parent; text: parent.sign; font.pixelSize: 16; color: app.palette.fg }
        HoverHandler { cursorShape: Qt.PointingHandCursor }
    }
    down.indicator: Step {
        x: 1; y: 1
        height: spin.height - 2
        sign: "−"
        over: spin.down.hovered
    }
    up.indicator: Step {
        x: spin.width - width - 1; y: 1
        height: spin.height - 2
        sign: "+"
        over: spin.up.hovered
    }
    background: Rectangle {
        radius: 4
        color: app.palette.input
        border.width: 1
        border.color: spin.activeFocus ? app.palette.accent : app.palette.border
    }
}
