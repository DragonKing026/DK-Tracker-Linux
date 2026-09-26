// The timer bar (Toggl-style): what, project, activity, $ and start/stop. The pencil switches to a
// manual entry: a day and hours instead of the timer. While an entry runs its fields edit it.
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: bar
    objectName: "timerBar"
    implicitHeight: layout.implicitHeight + 24
    color: app.palette.surface || "#1e2127"

    property bool manual: false
    property int projectId: 0
    property int activityId: 0
    property var billableTouched: null  // null: Kimai decides, as at a start from the popup
    readonly property bool running: app.view.running

    function fillManual(values) {
        manual = true
        description.text = values.description
        projectId = values.projectId
        activityId = values.activityId
        billableTouched = values.billable
        app.chooseProject(projectId)
    }

    function submit() {
        if (running) { app.stop(); return }
        if (manual)
            app.addManual(day.text, from.text, to.text, description.text, projectId, activityId, billableTouched)
        else
            app.start(description.text, projectId, activityId, billableTouched)
    }

    // The running entry fills the bar; the fields stay free to type in when nothing runs.
    // Only what Kimai changed is copied in: `view` is replaced every second (the clock), and
    // copying on every change undid a project being picked or a start time being typed.
    property var synced: ({})
    function sync() {
        if (!bar.running) {
            if (synced.id !== undefined) { from.text = ""; synced = ({}) }
            return
        }
        const v = app.view
        const fresh = synced.id !== v.entryId
        if ((fresh || v.description !== synced.description) && !description.activeFocus) {
            description.text = v.description
            description.cursorPosition = 0
        }
        if ((fresh || v.begin !== synced.begin) && !from.activeFocus)
            from.text = v.begin
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

    RowLayout {
        id: layout
        anchors.fill: parent
        anchors.margins: 12
        spacing: 8

        ToolButton {
            objectName: "modeSwitch"
            visible: !bar.running
            checkable: true
            checked: bar.manual
            icon.source: "image://glyph/" + (bar.manual ? "pencil" : "timer") + "/" + (app.palette.muted || "#9aa0ac").slice(1)
            ToolTip.visible: hovered
            ToolTip.text: bar.manual ? (app.texts.manualMode || "") : (app.texts.timerMode || "")
            onToggled: bar.manual = checked
        }

        TextField {
            id: description
            objectName: "description"
            Layout.fillWidth: true
            placeholderText: app.texts.descriptionPlaceholder || ""
            onAccepted: bar.running ? app.runningDescription(text) : bar.submit()
            onEditingFinished: if (bar.running && text !== app.view.description) app.runningDescription(text)
        }

        ProjectPicker {
            objectName: "project"
            projectId: bar.projectId
            onChosen: function (id) {
                bar.projectId = id
                bar.activityId = 0
                app.chooseProject(id)
            }
        }

        ComboBox {
            id: activity
            objectName: "activity"
            Layout.preferredWidth: 170
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

        ToolButton {
            objectName: "billable"
            enabled: app.view.billableAllowed
            readonly property bool on: bar.running ? app.view.billable : (bar.billableTouched === null ? true : bar.billableTouched)
            icon.source: "image://glyph/" + (on ? "money" : "money_off") + "/" + (on ? "16a34a" : "6b7280")
            onClicked: bar.running ? app.runningBillable(!on) : (bar.billableTouched = !on)
        }

        TextField {
            id: day
            objectName: "day"
            visible: bar.manual && !bar.running
            Layout.preferredWidth: 110
            inputMask: "9999-99-99"
            text: Qt.formatDate(new Date(), "yyyy-MM-dd")
        }
        TextField {
            id: from
            objectName: "from"
            visible: bar.manual || bar.running
            Layout.preferredWidth: 64
            inputMask: "99:99"
            placeholderText: app.texts.fromLabel || ""
            onEditingFinished: if (bar.running && text !== app.view.begin) app.runningBegin(text)
        }
        TextField {
            id: to
            objectName: "to"
            visible: bar.manual && !bar.running
            Layout.preferredWidth: 64
            inputMask: "99:99"
            placeholderText: app.texts.toLabel || ""
        }

        Label {
            objectName: "clock"
            visible: bar.running
            text: app.view.clock
            font.bold: true
            font.pixelSize: 18
            color: app.palette.fg || "#eceef2"
        }

        RoundButton {
            objectName: "submit"
            implicitWidth: 40
            implicitHeight: 40
            icon.source: "image://glyph/" + (bar.running ? "stop" : (bar.manual ? "plus" : "play")) + "/ffffff"
            ToolTip.visible: hovered
            ToolTip.text: bar.running ? (app.texts.stop || "") : (bar.manual ? (app.texts.addEntry || "") : (app.texts.start || ""))
            background: Rectangle {
                radius: 20
                color: bar.running ? (app.palette.stop || "#e02f2f") : (bar.manual ? (app.palette.accent || "#6f9bff") : (app.palette.start || "#16a34a"))
            }
            onClicked: bar.submit()
        }
    }
}
