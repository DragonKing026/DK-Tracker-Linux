// The edit window of one entry: every option Kimai gave for it — day and hours, project and
// activity, billable, the description in several lines, tags, break, and the server's own custom
// fields — what Kimai's own edit form offers (rates only with edit_rate, which the API does not
// tell). A form: labels on the left, controls on the right (docs/architektura/wyglad-okna-glownego.md). Enter saves, Shift+Enter adds a line to the
// description; Esc or a click beside it cancels.
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
    width: Math.min(parent ? parent.width - 48 : 600, 600)
    height: Math.min(parent ? parent.height - 48 : 720, frame.implicitHeight + 2 * padding)
    modal: true
    focus: true
    padding: 20
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
    onClosed: if (app.editor.open) app.closeEditor()

    Overlay.modal: Rectangle { color: Qt.rgba(0, 0, 0, 0.45) }
    background: Panel {}

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
            description: description.text, tags: tags.text, billable: billable, meta: fields
        }
    }
    function minutes(text) {
        const m = /^(\d{1,2}):?(\d{2})$/.exec(text.trim())
        return m ? Number(m[1]) * 60 + Number(m[2]) : -1
    }
    function save() { if (!editor.busy && !locked) app.saveEntry(values()) }

    Connections {
        target: app
        function onEditorChanged() {
            if (app.editor.open && !dialog.opened && !dialog.visible) { dialog.fill(); dialog.open() }
            else if (!app.editor.open && dialog.visible) dialog.close()
        }
    }

    contentItem: ColumnLayout {
        id: frame
        spacing: 14

        // Title and close
        RowLayout {
            Layout.fillWidth: true
            spacing: 8
            Label {
                Layout.fillWidth: true
                text: app.texts.editEntry || ""
                font.pixelSize: 18
                font.weight: Font.Bold
                color: app.palette.fg
            }
            IconButton {
                objectName: "editClose"
                glyph: "close"
                danger: true
                tip: app.texts.cancel || ""
                onClicked: app.closeEditor()
            }
        }

        // Invoiced: said once, above the form, which is shown but cannot be changed.
        Rectangle {
            visible: dialog.locked
            Layout.fillWidth: true
            implicitHeight: lockRow.implicitHeight + 16
            radius: 4
            color: app.palette.surface
            border.width: 1
            border.color: app.palette.border
            RowLayout {
                id: lockRow
                anchors.fill: parent
                anchors.margins: 8
                spacing: 8
                Image {
                    source: "image://glyph/lock/" + app.palette.muted.toString().slice(1, 7)
                    sourceSize.width: 16
                    sourceSize.height: 16
                }
                Label {
                    Layout.fillWidth: true
                    wrapMode: Text.Wrap
                    text: app.texts.errExported || ""
                    color: app.palette.muted
                }
            }
        }

        ScrollView {
            id: formScroll
            Layout.fillWidth: true
            Layout.fillHeight: true
            implicitHeight: form.implicitHeight
            contentWidth: availableWidth
            clip: true
            ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
            ScrollBar.vertical: Scroller {
                parent: formScroll
                x: formScroll.width - width
                height: formScroll.availableHeight
            }

            ColumnLayout {
                id: form
                width: parent.width
                spacing: 10

                FormRow {
                    label: app.texts.editDay || ""
                    DateField {
                        id: day
                        objectName: "editDay"
                        enabled: !dialog.locked
                    }
                    Item { Layout.fillWidth: true }
                }
                FormRow {
                    label: app.texts.editHours || ""
                    TimeField {
                        id: begin
                        objectName: "editBegin"
                        enabled: !dialog.locked
                    }
                    Label { text: "–"; color: app.palette.muted }
                    TimeField {
                        id: end
                        objectName: "editEnd"
                        enabled: !dialog.locked
                    }
                    Label {
                        Layout.leftMargin: 8
                        text: app.texts.editDuration || ""
                        color: app.palette.muted
                    }
                    Label {
                        objectName: "editDuration"
                        font.weight: Font.DemiBold
                        color: app.palette.fg
                        text: {
                            const a = dialog.minutes(begin.value), b = dialog.minutes(end.value)
                            if (a < 0 || b < 0) return "–"
                            const d = b - a
                            return d <= 0 ? "–" : Math.floor(d / 60) + ":" + ("0" + d % 60).slice(-2)
                        }
                    }
                    Item { Layout.fillWidth: true }
                }
                FormRow {
                    label: app.texts.editProject || ""
                    ProjectPicker {
                        objectName: "editProject"
                        enabled: !dialog.locked
                        Layout.fillWidth: true
                        projectId: dialog.projectId
                        onChosen: function (id) { dialog.projectId = id; dialog.activityId = 0; app.chooseRowProject(id) }
                    }
                }
                FormRow {
                    label: app.texts.editActivity || ""
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
                }
                FormRow {
                    label: app.texts.editBillable || ""
                    IconButton {  // the same $ as in the rows and the timer bar
                        objectName: "editBillable"
                        enabled: app.view.billableAllowed && !dialog.locked
                        glyph: dialog.billable ? "money" : "money_off"
                        tint: dialog.billable ? app.palette.start : app.palette.muted
                        tip: dialog.billable ? (app.texts.billableRowOn || "") : (app.texts.billableRowOff || "")
                        onClicked: dialog.billable = !dialog.billable
                    }
                    Label {
                        text: dialog.billable ? (app.texts.billableYes || "") : (app.texts.billableNo || "")
                        color: app.palette.muted
                    }
                    Item { Layout.fillWidth: true }
                }
                FormRow {
                    label: app.texts.editDescription || ""
                    DescriptionArea {
                        id: description
                        objectName: "editDescription"
                        enabled: !dialog.locked
                        readOnly: dialog.locked
                        Layout.fillWidth: true
                        maxLines: 8
                        placeholderText: app.texts.descriptionPlaceholder || ""
                        onAccepted: dialog.save()
                    }
                }
                FormRow {
                    label: app.texts.editTags || ""
                    TagPicker {
                        id: tags
                        objectName: "editTags"
                        enabled: !dialog.locked
                        Layout.fillWidth: true
                    }
                }
                FormRow {
                    visible: (dialog.editor.breakTime || "") !== ""
                    label: app.texts.editBreak || ""
                    Label {
                        Layout.topMargin: 8
                        text: dialog.editor.breakTime || ""
                        color: app.palette.fg
                    }
                }
                // The server's own custom fields, whatever they are called.
                ColumnLayout {
                    objectName: "editMeta"
                    Layout.fillWidth: true
                    spacing: 10
                    Repeater {
                        id: meta
                        delegate: FormRow {
                            required property var modelData
                            readonly property string name: modelData.name
                            property alias value: metaField.text
                            label: modelData.name
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
            }
        }

        Label {
            objectName: "editError"
            visible: (dialog.editor.error || "") !== ""
            Layout.fillWidth: true
            wrapMode: Text.Wrap
            text: dialog.editor.error || ""
            color: app.palette.danger
        }

        Rectangle { Layout.fillWidth: true; implicitHeight: 1; color: app.palette.divider }

        RowLayout {
            Layout.fillWidth: true
            spacing: 8
            Btn {
                objectName: "editDelete"
                variant: "danger"
                glyph: "trash"
                enabled: !dialog.locked
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
                variant: "primary"
                enabled: !dialog.locked && !dialog.editor.busy
                text: app.texts.save || ""
                onClicked: dialog.save()
            }
        }
    }
}
