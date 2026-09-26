// A day chosen from a calendar, not typed (live test of 0.10.0). `value` is "YYYY-MM-DD".
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Btn {
    id: field
    property string value: ""
    signal edited()
    readonly property date day: value ? new Date(value + "T12:00:00") : new Date()
    property int shownMonth: day.getMonth()
    property int shownYear: day.getFullYear()
    implicitWidth: 130
    text: value ? day.toLocaleDateString(Qt.locale(), "ddd, d MMM yyyy") : ""
    contentItem: Label {
        text: field.text
        color: app.palette.fg || "#eceef2"
        elide: Text.ElideRight
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
    onClicked: { shownMonth = day.getMonth(); shownYear = day.getFullYear(); picker.open() }

    function iso(d) {
        return d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2)
    }
    function shift(months) {
        const d = new Date(shownYear, shownMonth + months, 1)
        shownMonth = d.getMonth()
        shownYear = d.getFullYear()
    }

    Popup {
        id: picker
        y: field.height + 4
        padding: 8
        background: Rectangle {
            radius: 6
            color: app.palette.surface || "#1e2127"
            border.color: app.palette.line || "#2f333c"
        }
        contentItem: ColumnLayout {
            spacing: 4
            RowLayout {
                Layout.fillWidth: true
                IconButton { glyph: "chevron_left"; onClicked: field.shift(-1) }
                Label {
                    Layout.fillWidth: true
                    horizontalAlignment: Text.AlignHCenter
                    font.bold: true
                    color: app.palette.fg || "#eceef2"
                    text: new Date(field.shownYear, field.shownMonth, 1).toLocaleDateString(Qt.locale(), "LLLL yyyy")
                }
                IconButton { glyph: "chevron_right"; onClicked: field.shift(1) }
            }
            DayOfWeekRow {
                Layout.fillWidth: true
                locale: grid.locale
                delegate: Label {
                    required property string shortName
                    text: shortName
                    horizontalAlignment: Text.AlignHCenter
                    color: app.palette.muted || "#9aa0ac"
                    font.pixelSize: 12
                }
            }
            MonthGrid {
                id: grid
                objectName: "dateGrid"
                Layout.fillWidth: true
                implicitWidth: 260
                month: field.shownMonth
                year: field.shownYear
                locale: Qt.locale()
                delegate: Rectangle {
                    required property var model
                    readonly property bool chosen: field.value !== "" && field.iso(model.date) === field.value
                    implicitWidth: 34
                    implicitHeight: 30
                    radius: 4
                    color: chosen ? (app.palette.accent || "#6f9bff") : (dayHover.hovered ? (app.palette.surface2 || "#272b33") : "transparent")
                    opacity: model.month === grid.month ? 1 : 0.35
                    Label {
                        anchors.centerIn: parent
                        text: model.day
                        font.bold: model.today
                        color: parent.chosen ? "#ffffff" : (app.palette.fg || "#eceef2")
                    }
                    HoverHandler { id: dayHover; cursorShape: Qt.PointingHandCursor }
                }
                onClicked: function (date) { field.value = field.iso(date); field.edited(); picker.close() }
            }
        }
    }
}
