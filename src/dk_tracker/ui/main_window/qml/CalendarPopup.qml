// The calendar's bubble (Plan 7): beside a span just dragged (a new entry: "Add") or a block
// clicked (description, project, activity and billable to change; "Delete", "Resume", "More…" for
// the full edit window). A running entry: its fields change at once, as in the timer bar, and
// "Stop". Esc or a click beside it closes it.
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Popup {
    id: bubble
    objectName: "calendarPopup"
    property string kind: "new"  // "new" | "entry" | "running"
    property int entryId: 0
    property int day: 0
    property int start: 0
    property int end: 0
    property string hours: ""
    property int projectId: 0
    property int activityId: 0
    property bool billable: true
    property bool exported: false
    signal dismissed()

    parent: Overlay.overlay
    width: 380
    padding: 14
    modal: false
    focus: true
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
    background: Panel {}
    onClosed: dismissed()

    // Opens beside `item` (the block or the dragged span), inside the window.
    function showBeside(item) {
        const at = item.mapToItem(parent, 0, 0)
        const right = at.x + item.width + 8
        x = right + width <= parent.width - 8 ? right : Math.max(8, at.x - 8 - width)
        y = Math.max(8, Math.min(at.y, parent.height - implicitHeight - 8))
        open()
        description.area.forceActiveFocus()
    }
    function openNew(item, dayIndex, from, to, text) {
        kind = "new"; entryId = 0; day = dayIndex; start = from; end = to; exported = false
        hours = text
        description.text = ""
        projectId = app.view.projectId || 0
        activityId = 0
        billable = true
        if (projectId) app.chooseRowProject(projectId)
        showBeside(item)
    }
    function openEntry(item, b) {
        kind = b.running ? "running" : "entry"
        entryId = b.id; day = b.day; start = b.start; end = b.end; exported = b.exported
        hours = b.hours + (b.running ? "" : "  ·  " + b.time)
        description.text = b.description
        projectId = b.projectId
        activityId = b.activityId
        billable = b.billable
        app.chooseRowProject(projectId)
        showBeside(item)
    }
    function save() {
        if (kind === "new")
            app.calendarPage.create(day, start, end, description.text, projectId, activityId, billable)
        else if (kind === "entry")
            app.editFields(entryId, description.text, projectId, activityId, billable)
        else {
            app.runningDescription(description.text)
            if (projectId && activityId) app.runningWork(projectId, activityId)
        }
        close()
    }

    contentItem: ColumnLayout {
        spacing: 10
        RowLayout {
            Layout.fillWidth: true
            Image {
                source: "image://glyph/clock/" + app.palette.muted.toString().slice(1, 7)
                sourceSize.width: 15
                sourceSize.height: 15
            }
            Label {
                objectName: "calendarPopupHours"
                Layout.fillWidth: true
                text: bubble.hours
                font.weight: Font.DemiBold
                color: app.palette.fg
            }
            Image {
                visible: bubble.exported
                source: "image://glyph/lock/" + app.palette.muted.toString().slice(1, 7)
                sourceSize.width: 15
                sourceSize.height: 15
            }
            IconButton {
                glyph: "close"
                danger: true
                tip: app.texts.cancel || ""
                onClicked: bubble.close()
            }
        }
        DescriptionArea {
            id: description
            objectName: "calendarPopupDescription"
            Layout.fillWidth: true
            enabled: !bubble.exported
            maxLines: 5
            placeholderText: app.texts.descriptionPlaceholder || ""
            onAccepted: bubble.save()
        }
        ProjectPicker {
            objectName: "calendarPopupProject"
            Layout.fillWidth: true
            enabled: !bubble.exported
            projectId: bubble.projectId
            onChosen: function (id) { bubble.projectId = id; bubble.activityId = 0; app.chooseRowProject(id) }
        }
        RowLayout {
            Layout.fillWidth: true
            spacing: 8
            Combo {
                id: activity
                objectName: "calendarPopupActivity"
                Layout.fillWidth: true
                enabled: !bubble.exported
                model: app.rowActivityList
                textRole: "name"
                valueRole: "activityId"
                displayText: currentIndex < 0 ? (app.texts.chooseActivity || "") : currentText
                onCountChanged: currentIndex = indexOfValue(bubble.activityId)
                Connections {
                    target: bubble
                    function onActivityIdChanged() { activity.currentIndex = activity.indexOfValue(bubble.activityId) }
                }
                onActivated: bubble.activityId = currentValue
            }
            IconButton {  // the same $ as everywhere
                objectName: "calendarPopupBillable"
                enabled: app.view.billableAllowed && !bubble.exported
                glyph: bubble.billable ? "money" : "money_off"
                tint: bubble.billable ? app.palette.start : app.palette.muted
                tip: bubble.billable ? (app.texts.billableRowOn || "") : (app.texts.billableRowOff || "")
                onClicked: {
                    bubble.billable = !bubble.billable
                    if (bubble.kind === "running") app.runningBillable(bubble.billable)
                }
            }
        }
        Rectangle { Layout.fillWidth: true; implicitHeight: 1; color: app.palette.divider }
        RowLayout {
            Layout.fillWidth: true
            spacing: 6
            Btn {
                objectName: "calendarPopupDelete"
                visible: bubble.kind === "entry"
                enabled: !bubble.exported
                variant: "danger"
                glyph: "trash"
                text: app.texts.deleteEntry || ""
                onClicked: { app.deleteEntry(bubble.entryId); bubble.close() }
            }
            Btn {
                objectName: "calendarPopupStop"
                visible: bubble.kind === "running"
                variant: "danger"
                glyph: "stop"
                text: app.texts.stop || ""
                onClicked: { app.stop(); bubble.close() }
            }
            IconButton {
                objectName: "calendarPopupResume"
                visible: bubble.kind === "entry"
                glyph: "play"
                tint: app.palette.start
                tip: app.texts.resume || ""
                onClicked: { app.resume(bubble.entryId); bubble.close() }
            }
            IconButton {
                objectName: "calendarPopupMore"
                visible: bubble.kind === "entry"
                glyph: "pencil"
                tip: app.texts.calMore || ""
                onClicked: { app.openEntry(bubble.entryId); bubble.close() }
            }
            Item { Layout.fillWidth: true }
            Btn {
                objectName: "calendarPopupSave"
                variant: "primary"
                enabled: !bubble.exported
                text: bubble.kind === "new" ? (app.texts.addEntry || "") : (app.texts.save || "")
                onClicked: bubble.save()
            }
        }
    }
}
