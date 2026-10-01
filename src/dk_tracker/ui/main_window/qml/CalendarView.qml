// The calendar (Plan 7, spec 0.10 section 8): a day or a week (5 or 7 days) of hours, entries as
// blocks in project colours. Dragging on an empty part makes a new entry; a block is moved or
// resized by dragging; a click opens its bubble. Everything shown is `app.calendarPage.data`.
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: view
    objectName: "calendarView"
    color: app.palette.bg
    readonly property var d: app.calendarPage.data
    readonly property int gutter: 56  // the hours on the left
    readonly property real hourHeight: app.calendarPage.hourHeight  // Ctrl + the wheel
    property bool scrolled: false  // to working hours once, when the view first shows days
    property bool wheeled: false  // the user scrolled: the window's size no longer moves the hours

    // From 8:00; later only when "now" would be out of sight.
    function scrollToWork() {
        const shown = flick.height / hourHeight
        let from = 8
        if (d.now >= 0 && d.now / 60 > from + shown - 1)
            from = d.now / 60 - shown + 2
        flick.contentY = Math.max(0, Math.min(flick.contentHeight - flick.height, from * hourHeight))
        scrolled = true
    }
    onVisibleChanged: if (visible && d.loaded) scrollToWork()
    Connections {
        target: app.calendarPage
        function onDataChanged() { if (!view.scrolled && view.d.loaded && view.visible) view.scrollToWork() }
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        // -- the period ------------------------------------------------------------------
        Flow {
            Layout.fillWidth: true
            Layout.margins: 16
            Layout.bottomMargin: 12
            spacing: 12
            Segmented {
                objectName: "calendarMode"
                current: view.d.mode || "week"
                options: [
                    { code: "day", label: app.texts.calDay || "" },
                    { code: "week", label: app.texts.calWeek || "" },
                ]
                onChosen: function (code) { app.calendarPage.setMode(code) }
            }
            Segmented {
                objectName: "calendarDays"
                visible: view.d.mode === "week"
                current: view.d.workweek ? "5" : "7"
                options: [
                    { code: "5", label: app.texts.calFiveDays || "" },
                    { code: "7", label: app.texts.calSevenDays || "" },
                ]
                onChosen: function (code) { app.calendarPage.setWorkweek(code === "5") }
            }
            RowLayout {
                spacing: 4
                height: 34
                IconButton {
                    objectName: "calendarPrevious"
                    glyph: "chevron_left"
                    tip: app.texts.sumPrevious || ""
                    onClicked: app.calendarPage.step(-1)
                }
                Label {
                    objectName: "calendarLabel"
                    Layout.minimumWidth: 150
                    horizontalAlignment: Text.AlignHCenter
                    text: view.d.label || ""
                    font.pixelSize: 15
                    font.weight: Font.DemiBold
                    color: app.palette.fg
                }
                IconButton {
                    objectName: "calendarNext"
                    glyph: "chevron_right"
                    tip: app.texts.sumNext || ""
                    onClicked: app.calendarPage.step(1)
                }
                Btn {
                    objectName: "calendarToday"
                    Layout.leftMargin: 4
                    text: app.texts.sumCurrent || ""
                    enabled: !view.d.isToday
                    onClicked: app.calendarPage.today()
                }
                Label {
                    Layout.leftMargin: 8
                    visible: view.d.loading
                    text: app.texts.loading || ""
                    color: app.palette.muted
                }
            }
        }

        // -- the days' heads ------------------------------------------------------------
        Rectangle {
            Layout.fillWidth: true
            implicitHeight: 44
            color: app.palette.surface
            Rectangle { anchors.bottom: parent.bottom; width: parent.width; height: 1; color: app.palette.divider }
            Repeater {
                model: view.d.days || []
                delegate: Column {
                    required property var modelData
                    required property int index
                    x: grid.dayX(index)
                    width: grid.columnWidth
                    anchors.verticalCenter: parent.verticalCenter
                    Label {
                        width: parent.width
                        horizontalAlignment: Text.AlignHCenter
                        text: modelData.label
                        font.pixelSize: 13
                        font.weight: modelData.today ? Font.Bold : Font.DemiBold
                        color: modelData.today ? app.palette.accent : app.palette.fg
                    }
                    Label {
                        width: parent.width
                        horizontalAlignment: Text.AlignHCenter
                        text: modelData.total || " "
                        font.pixelSize: 11
                        color: app.palette.muted
                    }
                }
            }
        }

        // -- the grid ------------------------------------------------------------------------
        Flickable {
            id: flick
            objectName: "calendarGrid"
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            contentWidth: width
            contentHeight: 24 * view.hourHeight + 16
            boundsBehavior: Flickable.StopAtBounds
            interactive: false  // the wheel scrolls; dragging makes and moves entries
            onHeightChanged: if (view.scrolled && !view.wheeled) view.scrollToWork()
            ScrollBar.vertical: Scroller { objectName: "calendarScroll" }
            function scrollTo(y) { contentY = Math.max(0, Math.min(contentHeight - height, y)) }
            WheelHandler {  // the wheel zooms; the hour under the pointer stays where it is
                onWheel: function (event) {
                    view.wheeled = true
                    const at = parent.mapToItem(flick, point.position.x, point.position.y).y
                    const minute = (flick.contentY + at - grid.y) / grid.minuteHeight
                    app.calendarPage.zoom(event.angleDelta.y / 120)
                    flick.scrollTo(minute * grid.minuteHeight + grid.y - at)
                }
            }

            Item {
                id: grid
                width: flick.width - 12
                height: 24 * view.hourHeight
                y: 8
                readonly property int count: (view.d.days || []).length || 1
                readonly property real columnWidth: (width - view.gutter) / count
                readonly property real minuteHeight: view.hourHeight / 60
                function dayX(i) { return view.gutter + i * columnWidth }
                function dayAt(x, fallback) {
                    const i = Math.floor((x - view.gutter) / columnWidth)
                    return i >= 0 && i < count ? i : fallback
                }

                MouseArea {  // the right button drags the hours up and down (the left one makes entries)
                    objectName: "calendarPan"
                    anchors.fill: parent
                    acceptedButtons: Qt.RightButton
                    cursorShape: pressed ? Qt.ClosedHandCursor : Qt.ArrowCursor
                    property real fromY: 0
                    property real fromContent: 0
                    onPressed: function (event) {
                        fromY = mapToItem(flick, event.x, event.y).y
                        fromContent = flick.contentY
                    }
                    onPositionChanged: function (event) {
                        view.wheeled = true
                        flick.scrollTo(fromContent - (mapToItem(flick, event.x, event.y).y - fromY))
                    }
                }
                Repeater {  // the hours
                    model: 25
                    delegate: Item {
                        required property int index
                        y: index * view.hourHeight
                        width: grid.width
                        Rectangle { x: view.gutter; width: grid.width - view.gutter; height: 1; color: app.palette.divider }
                        Rectangle {  // half past, once there is room for it
                            visible: view.hourHeight >= 72 && index < 24
                            x: view.gutter; y: view.hourHeight / 2
                            width: grid.width - view.gutter; height: 1
                            color: app.palette.divider; opacity: 0.4
                        }
                        Label {
                            visible: index > 0 && index < 24
                            width: view.gutter - 8
                            y: -height / 2
                            horizontalAlignment: Text.AlignRight
                            text: ("0" + index).slice(-2) + ":00"
                            font.pixelSize: 11
                            color: app.palette.muted
                        }
                    }
                }
                Repeater {  // the days: an edge each, today faintly marked, and where new entries are dragged
                    model: view.d.days || []
                    delegate: Item {
                        id: column
                        required property var modelData
                        required property int index
                        x: grid.dayX(index)
                        width: grid.columnWidth
                        height: grid.height
                        Rectangle { anchors.fill: parent; visible: column.modelData.today; color: app.palette.surface; opacity: 0.6 }
                        Rectangle { width: 1; height: parent.height; color: app.palette.divider }

                        MouseArea {
                            id: draw
                            anchors.fill: parent
                            enabled: !app.view.offline
                            cursorShape: Qt.CrossCursor
                            property int from: 0
                            onPressed: function (event) {
                                from = app.calendarPage.snap(event.y / grid.minuteHeight, (event.modifiers & Qt.AltModifier) !== 0)
                                ghost.day = column.index
                                ghost.start = from
                                ghost.end = from
                                ghost.visible = false
                            }
                            onPositionChanged: function (event) {
                                const exact = (event.modifiers & Qt.AltModifier) !== 0
                                const at = app.calendarPage.snap(event.y / grid.minuteHeight, exact)
                                const step = exact ? 1 : 15
                                ghost.start = Math.min(from, at)
                                ghost.end = Math.max(Math.max(from, at), Math.min(1440, ghost.start + step))
                                ghost.visible = true
                            }
                            onReleased: {
                                if (!ghost.visible)
                                    return  // a click on an empty spot makes nothing
                                popup.openNew(ghost, ghost.day, ghost.start, ghost.end, ghost.text())
                            }
                        }
                    }
                }

                Repeater {
                    model: view.d.blocks || []
                    delegate: CalendarBlock {
                        canvas: grid
                        onOpened: function (b, item) { popup.openEntry(item, b) }
                    }
                }

                Rectangle {  // a new entry being dragged out
                    id: ghost
                    objectName: "calendarGhost"
                    property color tone: app.palette.accent  // a colour, so it has .r .g .b
                    property int day: 0
                    property int start: 0
                    property int end: 0
                    function hhmm(m) { return ("0" + Math.floor(m / 60)).slice(-2) + ":" + ("0" + m % 60).slice(-2) }
                    function text() { return hhmm(start) + " – " + hhmm(end) }
                    visible: false
                    z: 6
                    x: grid.dayX(day) + 2
                    width: grid.columnWidth - 4
                    y: start * grid.minuteHeight + 1
                    height: Math.max(14, (end - start) * grid.minuteHeight - 2)
                    radius: 4
                    color: Qt.rgba(tone.r, tone.g, tone.b, 0.22)
                    border.width: 1
                    border.color: app.palette.accent
                    Label {
                        x: 8
                        y: 2
                        text: ghost.text()
                        font.pixelSize: 11
                        font.weight: Font.DemiBold
                        color: app.palette.fg
                    }
                }

                Item {  // now: a line across today with a dot at its start
                    objectName: "calendarNow"
                    readonly property int today: (view.d.days || []).findIndex(day => day.today)
                    visible: view.d.now >= 0 && today >= 0
                    z: 7
                    x: grid.dayX(Math.max(0, today)) - 4
                    y: view.d.now * grid.minuteHeight - 4
                    width: grid.columnWidth + 4
                    height: 8
                    Rectangle { width: 8; height: 8; radius: 4; color: app.palette.danger }
                    Rectangle { x: 4; y: 3; width: parent.width - 4; height: 2; color: app.palette.danger }
                }
            }
        }
    }

    CalendarPopup {
        id: popup
        onDismissed: ghost.visible = false
    }
}
