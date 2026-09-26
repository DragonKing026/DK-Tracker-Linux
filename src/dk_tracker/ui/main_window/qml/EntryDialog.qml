// The edit window of one entry (live test of 0.10.0): every option Kimai gave for it — day and
// hours, duration, project and activity, the description in several lines, tags, billable, rates
// (for accounts that see them), break, and the server's own custom fields. Enter saves,
// Shift+Enter adds a line to the description.
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Popup {
    id: dialog
    objectName: "entryDialog"
    readonly property var editor: app.editor
    property int projectId: 0
    property int activityId: 0
    property bool billable: true
    readonly property bool locked: editor.exported === true  // invoiced: shown, not changed

    parent: Overlay.overlay
    anchors.centerIn: parent
    width: Math.min(parent ? parent.width - 48 : 640, 640)
    height: Math.min(parent ? parent.height - 48 : 720, content.implicitHeight + 40)
    modal: true
    focus: true
    padding: 20
    closePolicy: Popup.CloseOnEscape
    onClosed: if (app.editor.open) app.closeEditor()

    Overlay.modal: Rectangle { color: "#80000000" }
    background: Rectangle {
        radius: 6
        color: (app.palette.panel || "#262b35")
        border.color: (app.palette.border || "#6b7486")
    }

    // The fields take the entry's values when it opens; typing does not come back through `editor`.
    function fill() {
        const e = editor
        day.value = e.day
        begin.value = e.begin
        end.value = e.end
        projectId = e.projectId
        activityId = e.activityId
        billable = e.billable
        description.text = e.description
        tags.text = e.tags
        fixedRate.text = e.fixedRate
        hourlyRate.text = e.hourlyRate
        meta.model = e.meta
        app.chooseRowProject(projectId)
    }
    function values() {
        const fields = []
        for (let i = 0; i < meta.count; i++) {
            const item = meta.itemAt(i)
            fields.push({ name: item.name, value: item.value })
        }
        return {
            day: day.value, begin: begin.value, end: end.value, projectId: projectId, activityId: activityId,
            description: description.text, tags: tags.text, billable: billable,
            fixedRate: fixedRate.text, hourlyRate: hourlyRate.text, meta: fields
        }
    }
    function minutes(text) {
        const m = /^(\d{1,2}):?(\d{2})$/.exec(text.trim())
        return m ? Number(m[1]) * 60 + Number(m[2]) : -1
    }
    function save() { if (!editor.busy) app.saveEntry(values()) }

    Connections {
        target: app
        function onEditorChanged() {
            if (app.editor.open && !dialog.opened && !dialog.visible) { dialog.fill(); dialog.open() }
            else if (!app.editor.open && dialog.visible) dialog.close()
        }
    }

    contentItem: ScrollView {
        clip: true
        contentWidth: availableWidth
        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

        ColumnLayout {
            id: content
            width: parent.width
            spacing: 6

            RowLayout {
                Layout.fillWidth: true
                Label {
                    text: app.texts.editEntry || ""
                    font.pixelSize: 18
                    font.bold: true
                    color: app.palette.fg || "#eceef2"
                    Layout.fillWidth: true
                }
                Image {
                    visible: dialog.editor.exported === true
                    source: "image://glyph/lock/" + (app.palette.muted || "#9aa0ac").slice(1)
                    sourceSize.width: 18; sourceSize.height: 18
                }
                IconButton { glyph: "close"; tip: app.texts.cancel || ""; onClicked: app.closeEditor() }
            }
            Label {
                visible: dialog.editor.exported === true
                Layout.fillWidth: true
                wrapMode: Text.Wrap
                text: app.texts.errExported || ""
                color: app.palette.muted || "#9aa0ac"
            }

            component Caption: Label {
                Layout.topMargin: 8
                font.bold: true
                color: app.palette.fg || "#eceef2"
            }

            // Day, from, to on one line, each chosen from a list; the duration follows from them.
            RowLayout {
                Layout.fillWidth: true
                Layout.topMargin: 4
                spacing: 8
                component Inline: Label {
                    font.bold: true
                    color: app.palette.fg || "#eceef2"
                }
                Inline { text: app.texts.editDay || "" }
                DateField {
                    id: day
                    objectName: "editDay"
                    enabled: !dialog.locked
                }
                Item { implicitWidth: 6 }
                Inline { text: app.texts.fromLabel || "" }
                TimeField {
                    id: begin
                    objectName: "editBegin"
                    enabled: !dialog.locked
                }
                Label { text: "–"; color: app.palette.muted || "#9aa0ac" }
                Inline { text: app.texts.toLabel || "" }
                TimeField {
                    id: end
                    objectName: "editEnd"
                    enabled: !dialog.locked
                }
                Item { Layout.fillWidth: true }
                Label {
                    objectName: "editDuration"
                    font.bold: true
                    color: app.palette.fg || "#eceef2"
                    ToolTip.visible: durationHover.hovered
                    ToolTip.text: app.texts.editDuration || ""
                    HoverHandler { id: durationHover }
                    text: {
                        const a = dialog.minutes(begin.value), b = dialog.minutes(end.value)
                        if (a < 0 || b < 0) return ""
                        const d = b - a
                        return d <= 0 ? "–" : Math.floor(d / 60) + ":" + ("0" + d % 60).slice(-2)
                    }
                }
            }

            Caption { text: app.texts.editWork || "" }
            RowLayout {
                Layout.fillWidth: true
                spacing: 8
                ProjectPicker {
                    objectName: "editProject"
                    enabled: !dialog.locked
                    Layout.fillWidth: true
                    Layout.maximumWidth: 100000
                    projectId: dialog.projectId
                    onChosen: function (id) { dialog.projectId = id; dialog.activityId = 0; app.chooseRowProject(id) }
                }
                Combo {
                    id: activity
                    objectName: "editActivity"
                    enabled: !dialog.locked
                    Layout.fillWidth: true
                    model: app.rowActivityList
                    textRole: "name"
                    valueRole: "activityId"
                    displayText: currentIndex < 0 ? (app.texts.chooseActivity || "") : currentText
                    onCountChanged: currentIndex = indexOfValue(dialog.activityId)
                    Connections {
                        target: dialog
                        function onActivityIdChanged() { activity.currentIndex = activity.indexOfValue(dialog.activityId) }
                    }
                    onActivated: dialog.activityId = currentValue
                }
                IconButton {  // billable: the same $ as in the rows and the timer bar
                    objectName: "editBillable"
                    enabled: app.view.billableAllowed && !dialog.locked
                    glyph: dialog.billable ? "money" : "money_off"
                    tint: dialog.billable ? (app.palette.start || "#16a34a") : (app.palette.muted || "#9aa0ac")
                    tip: dialog.billable ? (app.texts.billableRowOn || "") : (app.texts.billableRowOff || "")
                    onClicked: dialog.billable = !dialog.billable
                }
            }

            Caption { text: app.texts.editDescription || "" }
            DescriptionArea {
                id: description
                objectName: "editDescription"
                enabled: !dialog.locked
                Layout.fillWidth: true
                maxLines: 8
                placeholderText: app.texts.descriptionPlaceholder || ""
                onAccepted: dialog.save()
            }

            Caption { text: app.texts.editTags || "" }
            Field {
                id: tags
                objectName: "editTags"
                enabled: !dialog.locked
                Layout.fillWidth: true
                placeholderText: app.texts.editTagsHint || ""
                onAccepted: dialog.save()
            }

            GridLayout {
                visible: dialog.editor.ratesVisible === true
                Layout.fillWidth: true
                columns: 2
                columnSpacing: 8
                rowSpacing: 4
                Caption { text: app.texts.editFixedRate || "" }
                Caption { text: app.texts.editHourlyRate || "" }
                Field {
                    id: fixedRate
                    objectName: "editFixedRate"
                    enabled: !dialog.locked
                    Layout.fillWidth: true
                    onAccepted: dialog.save()
                }
                Field {
                    id: hourlyRate
                    objectName: "editHourlyRate"
                    enabled: !dialog.locked
                    visible: dialog.editor.ratesVisible === true
                    Layout.fillWidth: true
                    onAccepted: dialog.save()
                }
            }

            Label {
                visible: (dialog.editor.breakTime || "") !== ""
                Layout.topMargin: 8
                text: (app.texts.editBreak || "") + ": " + (dialog.editor.breakTime || "")
                color: app.palette.muted || "#9aa0ac"
            }

            // The server's own custom fields, whatever they are called.
            ColumnLayout {
                objectName: "editMeta"
                Layout.fillWidth: true
                spacing: 4
                Repeater {
                    id: meta
                    delegate: ColumnLayout {
                        required property var modelData
                        readonly property string name: modelData.name
                        property alias value: metaField.text
                        Layout.fillWidth: true
                        Caption { text: modelData.name }
                        Field {
                            id: metaField
                            enabled: !dialog.locked
                            Layout.fillWidth: true
                            text: modelData.value
                            onAccepted: dialog.save()
                        }
                    }
                }
            }

            Label {
                objectName: "editError"
                visible: (dialog.editor.error || "") !== ""
                Layout.fillWidth: true
                Layout.topMargin: 8
                wrapMode: Text.Wrap
                text: dialog.editor.error || ""
                color: app.palette.err_fg || "#ff9d9d"
            }

            RowLayout {
                Layout.fillWidth: true
                Layout.topMargin: 12
                spacing: 8
                Btn {
                    objectName: "editDelete"
                    enabled: dialog.editor.exported !== true
                    text: app.texts.deleteEntry || ""
                    onClicked: app.deleteFromEditor()
                }
                Item { Layout.fillWidth: true }
                Btn {
                    objectName: "editCancel"
                    text: app.texts.cancel || ""
                    onClicked: app.closeEditor()
                }
                Btn {
                    objectName: "editSave"
                    highlighted: true
                    enabled: dialog.editor.exported !== true && !dialog.editor.busy
                    text: app.texts.save || ""
                    onClicked: dialog.save()
                }
            }
        }
    }
}
