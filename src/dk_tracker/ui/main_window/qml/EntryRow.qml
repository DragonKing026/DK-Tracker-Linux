// One entry, edited in place (Toggl-style): the description, project · activity, $, the hours.
// Enter or leaving a field saves; Esc restores. An exported entry is locked.
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: row
    objectName: "entryRow"
    required property var entry
    readonly property bool locked: entry.exported
    enabled: !app.view.offline  // spec, section 9; the list still scrolls
    readonly property string rowError: app.rowErrors[String(entry.entryId)] || ""
    implicitHeight: content.implicitHeight + 12
    color: hover.hovered ? (app.palette.surface || "#1e2127") : "transparent"

    HoverHandler { id: hover }

    ColumnLayout {
        id: content
        anchors.fill: parent
        anchors.leftMargin: 16
        anchors.rightMargin: 8
        anchors.topMargin: 6
        spacing: 2

        RowLayout {
            spacing: 8
            Rectangle {
                width: 9; height: 9; radius: 5
                color: entry.projectColor || (app.palette.line || "#2f333c")
            }
            TextField {
                id: description
                objectName: "rowDescription"
                Layout.fillWidth: true
                text: entry.description
                readOnly: row.locked
                background: Rectangle {
                    color: "transparent"
                    border.width: description.activeFocus ? 1 : 0
                    border.color: app.palette.focus || "#7aa2ff"
                    radius: 4
                }
                Component.onCompleted: cursorPosition = 0  // a long text shows its beginning
                onActiveFocusChanged: { app.setEditing(activeFocus); if (!activeFocus) cursorPosition = 0 }
                onEditingFinished: if (text !== entry.description) app.editDescription(entry.entryId, text)
                Keys.onEscapePressed: { text = entry.description; focus = false }
            }
            Button {
                objectName: "rowWork"
                flat: true
                enabled: !row.locked
                text: entry.projectName + (entry.activityName ? " · " + entry.activityName : "")
                onClicked: { work.projectId = entry.projectId; work.open(); app.chooseProject(entry.projectId) }
            }
            ToolButton {
                objectName: "rowBillable"
                enabled: !row.locked && app.view.billableAllowed
                icon.source: "image://glyph/" + (entry.billable ? "money" : "money_off") + "/" + (entry.billable ? "16a34a" : "6b7280")
                onClicked: app.setBillable(entry.entryId, !entry.billable)
            }
            TextField {
                id: begin
                objectName: "rowBegin"
                Layout.preferredWidth: 58
                inputMask: "99:99"
                onActiveFocusChanged: app.setEditing(activeFocus)
                text: entry.begin
                readOnly: row.locked
                onEditingFinished: if (text !== entry.begin) app.editTimes(entry.entryId, text, "")
                Keys.onEscapePressed: { text = entry.begin; focus = false }
            }
            Label { text: "–"; color: app.palette.muted || "#9aa0ac" }
            TextField {
                id: end
                objectName: "rowEnd"
                Layout.preferredWidth: 58
                inputMask: "99:99"
                onActiveFocusChanged: app.setEditing(activeFocus)
                text: entry.end
                readOnly: row.locked
                onEditingFinished: if (text !== entry.end) app.editTimes(entry.entryId, "", text)
                Keys.onEscapePressed: { text = entry.end; focus = false }
            }
            Label {
                Layout.preferredWidth: 48
                horizontalAlignment: Text.AlignRight
                text: entry.total
                font.bold: true
                color: app.palette.fg || "#eceef2"
            }
            Image {
                visible: row.locked
                source: "image://glyph/lock/" + (app.palette.muted || "#9aa0ac").slice(1)
                sourceSize.width: 16; sourceSize.height: 16
            }
            ToolButton {
                objectName: "rowResume"
                icon.source: "image://glyph/play/" + (app.palette.muted || "#9aa0ac").slice(1)
                ToolTip.visible: hovered
                ToolTip.text: app.texts.resume || ""
                onClicked: app.resume(entry.entryId)
            }
            ToolButton {
                objectName: "rowMenu"
                icon.source: "image://glyph/dots/" + (app.palette.muted || "#9aa0ac").slice(1)
                onClicked: menu.popup()
                Menu {
                    id: menu
                    MenuItem { text: app.texts.duplicate || ""; onTriggered: app.duplicate(entry.entryId) }
                    MenuItem {
                        text: app.texts.deleteEntry || ""
                        enabled: !row.locked
                        onTriggered: app.deleteEntry(entry.entryId)
                    }
                }
            }
        }

        Label {
            objectName: "rowError"
            visible: row.rowError !== ""
            text: row.rowError
            color: app.palette.err_fg || "#ff9d9d"
            font.pixelSize: 12
            Layout.leftMargin: 17
        }
    }

    // Project and activity together: Kimai takes a project only with an activity it allows.
    Popup {
        id: work
        property int projectId: 0
        property int activityId: 0
        y: row.height
        x: row.width - width - 60
        padding: 10
        contentItem: ColumnLayout {
            spacing: 8
            ProjectPicker {
                projectId: work.projectId
                onChosen: function (id) { work.projectId = id; work.activityId = 0; app.chooseProject(id) }
            }
            ComboBox {
                Layout.fillWidth: true
                model: app.activityList
                textRole: "name"
                valueRole: "activityId"
                displayText: currentIndex < 0 ? (app.texts.chooseActivity || "") : currentText
                onActivated: work.activityId = currentValue
            }
            Button {
                text: app.texts.save || "OK"
                enabled: work.projectId > 0 && work.activityId > 0
                onClicked: { app.editWork(entry.entryId, work.projectId, work.activityId); work.close() }
            }
        }
    }

    Rectangle {
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        height: 1
        color: app.palette.line || "#2f333c"
    }
}
