// A time chosen, not typed (live test of 0.10.0): a click opens hours and minutes side by side.
// Minutes go in steps of 5; a value from Kimai with other minutes (16:21) is on the list too.
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Btn {
    id: field
    property string placeholderText: ""
    property string value: ""  // "HH:MM" or ""
    signal edited()  // chosen by the user (not when `value` is set from outside)
    readonly property int hour: value ? Number(value.split(":")[0]) : -1
    readonly property int minute: value ? Number(value.split(":")[1]) : -1
    implicitWidth: 96
    text: value || placeholderText
    contentItem: Row {
        spacing: 6
        Image {
            anchors.verticalCenter: parent.verticalCenter
            source: "image://glyph/clock/" + (app.palette.muted || "#9aa0ac").slice(1)
            sourceSize.width: 15
            sourceSize.height: 15
        }
        Label {
            anchors.verticalCenter: parent.verticalCenter
            text: field.text
            color: field.value ? (app.palette.fg || "#eceef2") : (app.palette.muted || "#9aa0ac")
        }
    }
    onClicked: { picker.open(); hours.positionViewAtIndex(Math.max(0, hour), ListView.Center);
                 minutes.positionViewAtIndex(Math.max(0, minutes.model.indexOf(minute)), ListView.Center) }

    function pad(n) { return (n < 10 ? "0" : "") + n }
    function choose(h, m) { value = pad(h) + ":" + pad(m); edited() }

    Popup {
        id: picker
        y: field.height + 4
        padding: 6
        background: Rectangle {
            radius: 6
            color: (app.palette.panel || "#262b35")
            border.color: (app.palette.border || "#6b7486")
        }
        contentItem: RowLayout {
            spacing: 4
            component Column: ListView {
                property int chosen: -1
                signal picked(int value)
                implicitWidth: 52
                implicitHeight: 220
                clip: true
                delegate: ItemDelegate {
                    id: cell
                    required property int modelData
                    readonly property bool isChosen: modelData === ListView.view.chosen
                    width: ListView.view.width
                    height: 30
                    HoverHandler { cursorShape: Qt.PointingHandCursor }
                    contentItem: Label {
                        text: field.pad(modelData)
                        horizontalAlignment: Text.AlignHCenter
                        font.bold: cell.isChosen
                        color: cell.isChosen ? (app.palette.accent || "#6f9bff") : (app.palette.fg || "#eceef2")
                    }
                    background: Rectangle {
                        radius: 4
                        color: parent.hovered ? (app.palette.control || "#353b48") : "transparent"
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
            Rectangle { implicitWidth: 1; Layout.fillHeight: true; color: app.palette.line || "#2f333c" }
            Column {
                id: minutes
                objectName: "timeMinutes"
                model: {
                    const steps = Array.from({ length: 12 }, (_, i) => i * 5)
                    if (field.minute >= 0 && steps.indexOf(field.minute) < 0) {
                        steps.push(field.minute)
                        steps.sort((a, b) => a - b)
                    }
                    return steps
                }
                chosen: field.minute
                onPicked: function (m) { field.choose(Math.max(0, field.hour), m); picker.close() }
            }
        }
    }
}
