// A choice of a few (the period, the breakdown): buttons in one frame. The chosen one is marked as
// every selection is — accent text and edge on the control colour, not a solid blue block.
import QtQuick
import QtQuick.Controls

Rectangle {
    id: segmented
    property var options: []  // [{code, label}]
    property string current: ""
    signal chosen(string code)
    implicitWidth: row.implicitWidth + 2
    implicitHeight: 34
    radius: 4
    color: app.palette.control
    border.width: 1
    border.color: app.palette.border

    Row {
        id: row
        x: 1
        y: 1
        height: parent.height - 2
        Repeater {
            model: segmented.options
            delegate: AbstractButton {
                id: option
                required property var modelData
                required property int index
                objectName: "segment_" + modelData.code
                readonly property bool active: modelData.code === segmented.current
                height: row.height
                implicitWidth: label.implicitWidth + 24
                HoverHandler { cursorShape: Qt.PointingHandCursor }
                onClicked: if (!active) segmented.chosen(modelData.code)
                contentItem: Label {
                    id: label
                    text: option.modelData.label
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    font.weight: option.active ? Font.DemiBold : Font.Normal
                    color: option.active ? app.palette.accent : app.palette.fg
                }
                background: Rectangle {
                    radius: 3
                    color: option.active ? app.palette.control
                         : option.down ? app.palette.control_down
                         : option.hovered ? app.palette.control_hover : "transparent"
                    border.width: option.active ? 1 : 0
                    border.color: app.palette.accent
                }
                Rectangle {  // a thin divider between two unchosen neighbours
                    visible: option.index > 0 && !option.active && segmented.options[option.index - 1].code !== segmented.current
                    width: 1
                    height: parent.height - 12
                    anchors.verticalCenter: parent.verticalCenter
                    color: app.palette.border
                }
            }
        }
    }
}
