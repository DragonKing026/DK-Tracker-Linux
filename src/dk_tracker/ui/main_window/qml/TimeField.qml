// A time chosen, not typed: a click opens hours and minutes side by side, every minute.
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

SelectButton {
    id: field
    property string placeholderText: ""
    property string value: ""  // "HH:MM" or ""
    signal edited()  // chosen by the user (not when `value` is set from outside)
    readonly property int hour: value ? Number(value.split(":")[0]) : -1
    readonly property int minute: value ? Number(value.split(":")[1]) : -1
    glyph: "clock"
    chevron: false
    empty: value === ""
    implicitWidth: 96
    text: value || placeholderText
    onClicked: {
        picker.open()
        hours.positionViewAtIndex(Math.max(0, hour), ListView.Center)
        minutes.positionViewAtIndex(Math.max(0, minutes.model.indexOf(minute)), ListView.Center)
    }

    function pad(n) { return (n < 10 ? "0" : "") + n }
    function choose(h, m) { value = pad(h) + ":" + pad(m); edited() }

    Popup {
        id: picker
        y: field.height + 4
        padding: 6
        background: Panel {}
        contentItem: RowLayout {
            spacing: 4
            component Column: ListView {
                property int chosen: -1
                signal picked(int value)
                implicitWidth: 56
                implicitHeight: 224
                clip: true
                ScrollBar.vertical: Scroller {}
                delegate: ItemDelegate {
                    id: cell
                    required property int modelData
                    readonly property bool isChosen: modelData === ListView.view.chosen
                    width: ListView.view.width
                    height: 32
                    HoverHandler { cursorShape: Qt.PointingHandCursor }
                    contentItem: Label {
                        text: field.pad(cell.modelData)
                        horizontalAlignment: Text.AlignHCenter
                        font.weight: cell.isChosen ? Font.Bold : Font.Normal
                        color: cell.isChosen ? app.palette.accent : app.palette.fg
                    }
                    // The chosen one as everywhere: accent text and edge, not a bright block.
                    background: Rectangle {
                        radius: 4
                        color: cell.isChosen ? app.palette.control : cell.hovered ? app.palette.control_hover : "transparent"
                        border.width: cell.isChosen ? 1 : 0
                        border.color: app.palette.accent
                    }
                    onClicked: ListView.view.picked(modelData)
                }
            }
            Column {
                id: hours
                objectName: "timeHours"
                model: Array.from({ length: 24 }, (_, i) => i)
                chosen: field.hour
                onPicked: function (h) { field.choose(h, Math.max(0, field.minute)) }
            }
            Rectangle { implicitWidth: 1; Layout.fillHeight: true; color: app.palette.divider }
            Column {
                id: minutes
                objectName: "timeMinutes"
                model: Array.from({ length: 60 }, (_, i) => i)
                chosen: field.minute
                onPicked: function (m) { field.choose(Math.max(0, field.hour), m); picker.close() }
            }
        }
    }
}
