// A day chosen from a calendar, not typed. `value` is "YYYY-MM-DD".
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

SelectButton {
    id: field
    property string value: ""
    signal edited()
    readonly property date day: value ? new Date(value + "T12:00:00") : new Date()
    property int shownMonth: day.getMonth()
    property int shownYear: day.getFullYear()
    glyph: "calendar"
    chevron: false
    implicitWidth: 190
    text: value ? day.toLocaleDateString(Qt.locale(), "ddd, d MMM yyyy") : ""
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
        padding: 10
        background: Panel {}
        contentItem: ColumnLayout {
            spacing: 6
            RowLayout {
                Layout.fillWidth: true
                IconButton { glyph: "chevron_left"; onClicked: field.shift(-1) }
                Label {
                    Layout.fillWidth: true
                    horizontalAlignment: Text.AlignHCenter
                    font.weight: Font.DemiBold
                    color: app.palette.fg
                    // The month on its own ("wrzesień", not "września"); QML has no "LLLL" format.
                    text: Qt.locale().standaloneMonthName(field.shownMonth, Locale.LongFormat) + " " + field.shownYear
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
                    color: app.palette.muted
                    font.pixelSize: 12
                }
            }
            MonthGrid {
                id: grid
                objectName: "dateGrid"
                Layout.fillWidth: true
                implicitWidth: 266
                month: field.shownMonth
                year: field.shownYear
                locale: Qt.locale()
                delegate: Rectangle {
                    required property var model
                    readonly property bool chosen: field.value !== "" && field.iso(model.date) === field.value
                    implicitWidth: 36
                    implicitHeight: 32
                    radius: 4
                    color: chosen ? app.palette.accent : dayHover.hovered ? app.palette.control_hover : "transparent"
                    border.width: model.today && !chosen ? 1 : 0
                    border.color: app.palette.accent
                    Label {
                        anchors.centerIn: parent
                        text: model.day
                        color: parent.chosen ? "#ffffff" : model.month === grid.month ? app.palette.fg : app.palette.placeholder
                    }
                    HoverHandler { id: dayHover; cursorShape: Qt.PointingHandCursor }
                }
                onClicked: function (date) { field.value = field.iso(date); field.edited(); picker.close() }
            }
        }
    }
}
