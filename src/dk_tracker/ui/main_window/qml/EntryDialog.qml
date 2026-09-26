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
        radius: 12
        color: app.palette.surface || "#1e2127"
        border.color: app.palette.line || "#2f333c"
    }

    // The fields take the entry's values when it opens; typing does not come back through `editor`.
    function fill() {
        const e = editor
        day.text = e.day
        begin.text = e.begin
        end.text = e.end
        duration.text = e.duration
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
            day: day.text, begin: begin.text, end: end.text, projectId: projectId, activityId: activityId,
            description: description.text, tags: tags.text, billable: billable,
            fixedRate: fixedRate.text, hourlyRate: hourlyRate.text, meta: fields
        }
    }
    function minutes(text) {
        const m = /^(\d{1,2}):?(\d{2})$/.exec(text.trim())
        return m ? Number(m[1]) * 60 + Number(m[2]) : -1
    }
    function clock(total) {
        const m = ((total % 1440) + 1440) % 1440
        return Math.floor(m / 60).toString().padStart(2, "0") + ":" + (m % 60).toString().padStart(2, "0")
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

            // Day, from, to, duration: the duration moves the end, the end changes the duration.
            GridLayout {
                Layout.fillWidth: true
                columns: 4
                columnSpacing: 8
                rowSpacing: 4
                Caption { text: app.texts.editDay || "" }
                Caption { text: app.texts.fromLabel || "" }
                Caption { text: app.texts.toLabel || "" }
                Caption { text: app.texts.editDuration || "" }
                Field {
                    id: day
                    objectName: "editDay"
                    Layout.fillWidth: true
                    placeholderText: "RRRR-MM-DD"
                    validator: RegularExpressionValidator { regularExpression: /^[\d-]{0,10}$/ }
                    onAccepted: dialog.save()
                }
                Field {
                    id: begin
                    objectName: "editBegin"
                    Layout.preferredWidth: 90
                    horizontalAlignment: Text.AlignHCenter
                    validator: RegularExpressionValidator { regularExpression: /^\d{0,2}:?\d{0,2}$/ }
                    onTextEdited: {
                        const a = dialog.minutes(text), b = dialog.minutes(end.text)
                        if (a >= 0 && b >= 0) duration.text = dialog.clock(b - a).replace(/^0/, "")
                    }
                    onAccepted: dialog.save()
                }
                Field {
                    id: end
                    objectName: "editEnd"
                    Layout.preferredWidth: 90
                    horizontalAlignment: Text.AlignHCenter
                    validator: RegularExpressionValidator { regularExpression: /^\d{0,2}:?\d{0,2}$/ }
                    onTextEdited: {
                        const a = dialog.minutes(begin.text), b = dialog.minutes(text)
                        if (a >= 0 && b >= 0) duration.text = dialog.clock(b - a).replace(/^0/, "")
                    }
                    onAccepted: dialog.save()
                }
                Field {
                    id: duration
                    objectName: "editDuration"
                    Layout.preferredWidth: 90
                    horizontalAlignment: Text.AlignHCenter
                    validator: RegularExpressionValidator { regularExpression: /^\d{0,2}:?\d{0,2}$/ }
                    onTextEdited: {
                        const a = dialog.minutes(begin.text), d = dialog.minutes(text)
                        if (a >= 0 && d >= 0) end.text = dialog.clock(a + d)
                    }
                    onAccepted: dialog.save()
                }
            }

            Caption { text: app.texts.editWork || "" }
            RowLayout {
                Layout.fillWidth: true
                spacing: 8
                ProjectPicker {
                    objectName: "editProject"
                    Layout.fillWidth: true
                    Layout.maximumWidth: 100000
                    projectId: dialog.projectId
                    onChosen: function (id) { dialog.projectId = id; dialog.activityId = 0; app.chooseRowProject(id) }
                }
                Combo {
                    id: activity
                    objectName: "editActivity"
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

            Caption { text: app.texts.editDescription || "" }
            DescriptionArea {
                id: description
                objectName: "editDescription"
                Layout.fillWidth: true
                maxLines: 8
                placeholderText: app.texts.descriptionPlaceholder || ""
                onAccepted: dialog.save()
            }

            Caption { text: app.texts.editTags || "" }
            Field {
                id: tags
                objectName: "editTags"
                Layout.fillWidth: true
                placeholderText: app.texts.editTagsHint || ""
                onAccepted: dialog.save()
            }

            Caption { text: app.texts.editBillable || "" }
            Combo {
                objectName: "editBillable"
                Layout.preferredWidth: 200
                enabled: app.view.billableAllowed
                model: [{ label: app.texts.yes || "Tak", value: true }, { label: app.texts.no || "Nie", value: false }]
                textRole: "label"
                valueRole: "value"
                currentIndex: dialog.billable ? 0 : 1
                onActivated: dialog.billable = currentValue
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
                    Layout.fillWidth: true
                    onAccepted: dialog.save()
                }
                Field {
                    id: hourlyRate
                    objectName: "editHourlyRate"
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
