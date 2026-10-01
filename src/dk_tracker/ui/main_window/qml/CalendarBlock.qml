// One entry in the calendar (Plan 7): a tint of the project's colour with a bar of it on the left,
// the description, project and hours. Dragged by its middle it moves (also to another day), by an
// edge it changes that hour; let go, it is saved. A click without moving opens its bubble.
// Snapping (15 min, Alt: the minute) is core/calendar.py's, through app.calendarPage.snap.
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: block
    required property var modelData
    required property var canvas  // the CalendarView grid: columnWidth, dayX(), minuteHeight, dayAt()
    readonly property var b: modelData
    readonly property bool locked: app.view.offline || !b.movable
    // Where it is drawn: its place, or where the pointer takes it while dragged.
    property int day: b.day
    property real start: b.start  // minutes, the seconds as a fraction
    property real end: b.end
    property bool dragging: false
    signal opened(var block, var item)
    objectName: "calendarBlock_" + b.id

    x: canvas.dayX(day) + (dragging ? 0 : b.column * canvas.columnWidth / b.columns) + 2
    width: (dragging ? canvas.columnWidth : canvas.columnWidth / b.columns) - 4
    y: start * canvas.minuteHeight + 1
    height: Math.max(14, (end - start) * canvas.minuteHeight - 2)
    z: dragging ? 5 : 1

    readonly property color ink: b.color || app.palette.muted
    Rectangle {
        anchors.fill: parent
        radius: 4
        color: app.palette.bg
        Rectangle {  // the project's colour, faint enough for the text on it
            anchors.fill: parent
            radius: 4
            color: Qt.rgba(block.ink.r, block.ink.g, block.ink.b, block.dragging ? 0.42 : 0.26)
            border.width: block.b.running || block.dragging ? 1 : 0
            border.color: block.ink
        }
        Rectangle {
            width: 3
            height: parent.height
            radius: 2
            color: block.ink
        }
    }
    ColumnLayout {
        anchors.fill: parent
        anchors.leftMargin: 8
        anchors.rightMargin: 4
        anchors.topMargin: 2
        anchors.bottomMargin: 2
        spacing: 0
        clip: true
        RowLayout {
            Layout.fillWidth: true
            spacing: 4
            Label {
                Layout.fillWidth: true
                text: block.b.description
                textFormat: Text.PlainText
                elide: Text.ElideRight
                font.pixelSize: 12
                font.weight: Font.DemiBold
                color: app.palette.fg
            }
            Image {
                visible: block.b.exported
                source: "image://glyph/lock/" + app.palette.muted.toString().slice(1, 7)
                sourceSize.width: 12
                sourceSize.height: 12
            }
        }
        Label {
            visible: block.height > 34
            Layout.fillWidth: true
            text: block.b.project
            elide: Text.ElideRight
            font.pixelSize: 11
            color: app.palette.muted
        }
        Label {
            visible: block.height > 50
            Layout.fillWidth: true
            text: block.dragging ? block.hoursText() : block.b.hours + "  ·  " + block.b.time
            elide: Text.ElideRight
            font.pixelSize: 11
            color: app.palette.muted
        }
        Item { Layout.fillHeight: true }
    }

    function hhmm(minutes) {
        const m = Math.floor(minutes)
        return ("0" + Math.floor(m / 60)).slice(-2) + ":" + ("0" + m % 60).slice(-2)
    }
    function hoursText() { return hhmm(start) + " – " + hhmm(end) }

    MouseArea {
        id: mouse
        anchors.fill: parent
        hoverEnabled: true
        property string mode: ""  // "move" | "top" | "bottom"
        property point from: Qt.point(0, 0)  // in the grid
        property real fromStart: 0
        property real fromEnd: 0
        property int fromDay: 0
        readonly property string edgeUnder: block.locked || block.height < 24 ? "move"
                                          : mouseY < 6 ? "top" : mouseY > height - 6 ? "bottom" : "move"
        cursorShape: block.dragging ? (mode === "move" ? Qt.ClosedHandCursor : Qt.SizeVerCursor)
                   : block.locked ? Qt.PointingHandCursor
                   : edgeUnder === "move" ? Qt.OpenHandCursor : Qt.SizeVerCursor
        onPressed: function (event) {
            mode = edgeUnder
            from = mapToItem(block.canvas, event.x, event.y)
            fromStart = block.b.start
            fromEnd = block.b.end
            fromDay = block.b.day
        }
        onPositionChanged: function (event) {
            if (!pressed || block.locked)
                return
            const at = mapToItem(block.canvas, event.x, event.y)
            if (!block.dragging && Math.abs(at.y - from.y) < 4 && Math.abs(at.x - from.x) < 4)
                return  // still a click
            if (!block.dragging) {
                block.dragging = true
                app.calendarPage.setDragging(true)
            }
            const exact = (event.modifiers & Qt.AltModifier) !== 0
            const shift = (at.y - from.y) / block.canvas.minuteHeight
            const step = exact ? 1 : 15
            if (mode === "move") {
                const length = fromEnd - fromStart
                const start = Math.max(0, Math.min(1440 - length, app.calendarPage.snap(fromStart + shift, exact)))
                block.start = start
                block.end = start + length
                block.day = block.canvas.dayAt(at.x, fromDay)
            } else if (mode === "top") {
                block.start = Math.min(fromEnd - step, app.calendarPage.snap(fromStart + shift, exact))
            } else {
                block.end = Math.max(fromStart + step, app.calendarPage.snap(fromEnd + shift, exact))
            }
        }
        onReleased: {
            if (block.dragging) {
                block.dragging = false
                const moved = block.day !== block.b.day || block.start !== block.b.start || block.end !== block.b.end
                if (moved)
                    app.calendarPage.move(block.b.id, block.day, block.start, block.end)
                app.calendarPage.setDragging(false)
                block.day = Qt.binding(() => block.b.day)
                block.start = Qt.binding(() => block.b.start)
                block.end = Qt.binding(() => block.b.end)
            } else {
                block.opened(block.b, block)
            }
        }
        onCanceled: {
            block.dragging = false
            app.calendarPage.setDragging(false)
            block.day = Qt.binding(() => block.b.day)
            block.start = Qt.binding(() => block.b.start)
            block.end = Qt.binding(() => block.b.end)
        }
    }
}
