// The timer bar (Toggl-style): what, project, activity, $ and start/stop. The pencil switches to a
// manual entry: a day and hours on a second line. While an entry runs its fields edit it.
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: bar
    objectName: "timerBar"
    implicitHeight: layout.implicitHeight + 24
    color: app.palette.surface

    property bool manual: false
    property int projectId: 0
    property int activityId: 0
    property var billableTouched: null  // null: Kimai decides, as at a start from the popup
    readonly property bool running: app.view.running
    readonly property bool billableOn: running ? app.view.billable : (billableTouched === null ? true : billableTouched)

    function submit() {
        if (running) { app.stop(); return }
        if (manual)
            app.addManual(day.value, manualFrom.value, manualTo.value, description.text, projectId, activityId,
                          billableTouched)
        else
            app.start(description.text, projectId, activityId, billableTouched)
    }

    // The running entry fills the bar; the fields stay free to type in when nothing runs.
    // Only what Kimai changed is copied in: `view` is replaced every second (the clock), and
    // copying on every change undid a project being picked or a start time being chosen.
    property var synced: ({})
    function sync() {
        if (!bar.running) {
            if (synced.id !== undefined) { from.value = ""; synced = ({}) }
            return
        }
        const v = app.view
        const fresh = synced.id !== v.entryId
        if ((fresh || v.description !== synced.description) && !description.area.activeFocus) {
            description.text = v.description
            description.area.cursorPosition = 0
        }
        if (fresh || v.begin !== synced.begin)
            from.value = v.begin
        if (fresh || v.projectId !== synced.projectId || v.activityId !== synced.activityId) {
            bar.projectId = v.projectId
            bar.activityId = v.activityId
            app.chooseProject(bar.projectId)
        }
        synced = { id: v.entryId, description: v.description, begin: v.begin,
                   projectId: v.projectId, activityId: v.activityId }
    }
    Component.onCompleted: sync()
    Connections {
        target: app
        function onViewChanged() { bar.sync() }
    }

    Rectangle {  // the line under the bar
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        height: 1
        color: app.palette.divider
    }

    ColumnLayout {
        id: layout
        anchors.fill: parent
        anchors.margins: 12
        spacing: 8

        RowLayout {
            Layout.fillWidth: true
            spacing: 8

            IconButton {
                objectName: "modeSwitch"
                visible: !bar.running
                glyph: bar.manual ? "pencil" : "timer"
                tint: app.palette.accent
                tip: bar.manual ? (app.texts.manualMode || "") : (app.texts.timerMode || "")
                onClicked: bar.manual = !bar.manual
            }
            DescriptionArea {
                id: description
                objectName: "description"
                Layout.fillWidth: true
                Layout.minimumWidth: 140
                Layout.preferredWidth: 280
                maxLines: 3
                placeholderText: app.texts.descriptionPlaceholder || ""
                onAccepted: bar.running ? app.runningDescription(text) : bar.submit()
                onEditingFinished: if (bar.running && text !== app.view.description) app.runningDescription(text)
            }
            ProjectPicker {
                objectName: "project"
                Layout.fillWidth: true
                Layout.minimumWidth: 110
                Layout.maximumWidth: 210
                projectId: bar.projectId
                onChosen: function (id) {
                    bar.projectId = id
                    bar.activityId = 0
                    app.chooseProject(id)
                }
            }
            Combo {
                id: activity
                objectName: "activity"
                Layout.fillWidth: true
                Layout.minimumWidth: 110
                Layout.maximumWidth: 190
                model: app.activityList
                textRole: "name"
                valueRole: "activityId"
                displayText: currentIndex < 0 ? (app.texts.chooseActivity || "") : currentText
                Component.onCompleted: currentIndex = indexOfValue(bar.activityId)
                onCountChanged: currentIndex = indexOfValue(bar.activityId)  // the list came after the choice
                Connections {
                    target: bar
                    function onActivityIdChanged() { activity.currentIndex = activity.indexOfValue(bar.activityId) }
                }
                onActivated: {
                    bar.activityId = currentValue
                    if (bar.running) app.runningWork(bar.projectId, bar.activityId)
                }
            }
            IconButton {
                objectName: "billable"
                enabled: app.view.billableAllowed
                glyph: bar.billableOn ? "money" : "money_off"
                tint: bar.billableOn ? app.palette.start : app.palette.muted
                tip: bar.billableOn ? (app.texts.billableOn || "") : (app.texts.billableOff || "")
                onClicked: bar.running ? app.runningBillable(!bar.billableOn) : (bar.billableTouched = !bar.billableOn)
            }
            TimeField {
                id: from
                objectName: "from"
                visible: bar.running
                placeholderText: app.texts.fromLabel || ""
                onEdited: if (bar.running && value !== app.view.begin) app.runningBegin(value)
            }
            Label {
                objectName: "clock"
                visible: bar.running
                text: app.view.clock
                font.bold: true
                font.pixelSize: 18
                font.features: { "tnum": 1 }
                color: app.palette.fg
            }
            RoundButton {
                objectName: "submit"
                implicitWidth: 40
                implicitHeight: 40
                icon.source: "image://glyph/" + (bar.running ? "stop" : (bar.manual ? "plus" : "play")) + "/ffffff"
                icon.color: "transparent"
                HoverHandler { cursorShape: Qt.PointingHandCursor }
                ToolTip.visible: hovered
                ToolTip.text: bar.running ? (app.texts.stop || "") : (bar.manual ? (app.texts.addEntry || "") : (app.texts.start || ""))
                background: Rectangle {
                    radius: 20
                    color: bar.running ? app.palette.danger : (bar.manual ? app.palette.accent : app.palette.start)
                    opacity: parent.hovered ? 0.88 : 1
                }
                onClicked: bar.submit()
            }
        }

        // Manual entry: the day and the hours, on a line of their own.
        RowLayout {
            objectName: "manualRow"
            visible: bar.manual && !bar.running
            Layout.fillWidth: true
            spacing: 8
            Item { implicitWidth: 32 }  // under the mode switch
            DateField {
                id: day
                objectName: "day"
                value: Qt.formatDate(new Date(), "yyyy-MM-dd")
            }
            TimeField {
                id: manualFrom
                objectName: "manualFrom"
                placeholderText: app.texts.fromLabel || ""
            }
            Label { text: "–"; color: app.palette.muted }
            TimeField {
                id: manualTo
                objectName: "manualTo"
                placeholderText: app.texts.toLabel || ""
            }
            Item { Layout.fillWidth: true }
        }
    }
}
