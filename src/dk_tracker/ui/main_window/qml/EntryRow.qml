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
    readonly property string projectColor: entry.projectColor || (app.palette.muted || "#9aa0ac")
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
            spacing: 6
            Rectangle {
                width: 9; height: 9; radius: 5
                color: row.projectColor
            }
            InlineField {
                objectName: "rowDescription"
                Layout.fillWidth: true
                Layout.minimumWidth: 150
                Layout.preferredWidth: 400
                shown: entry.description
                readOnly: row.locked
                onEditingFinished: if (text !== entry.description) app.editDescription(entry.entryId, text)
            }
            // Project · activity in the project's colour; a click opens both lists.
            ToolButton {
                id: workButton
                objectName: "rowWork"
                enabled: !row.locked
                Layout.fillWidth: true
                Layout.minimumWidth: 60
                Layout.maximumWidth: 280
                contentItem: Label {
                    text: entry.projectName + (entry.activityName ? " · " + entry.activityName : "")
                    color: row.projectColor
                    elide: Text.ElideRight
                    verticalAlignment: Text.AlignVCenter
                }
                background: Rectangle {
                    radius: 6
                    color: workButton.hovered && workButton.enabled ? (app.palette.surface2 || "#272b33") : "transparent"
                }
                onClicked: { work.projectId = entry.projectId; work.open(); app.chooseRowProject(entry.projectId) }
            }
            IconButton {
                objectName: "rowBillable"
                enabled: !row.locked && app.view.billableAllowed
                glyph: entry.billable ? "money" : "money_off"
                tint: entry.billable ? (app.palette.start || "#16a34a") : (app.palette.muted || "#9aa0ac")
                opacity: entry.billable ? 1 : 0.6
                tip: entry.billable ? (app.texts.billableRowOn || "") : (app.texts.billableRowOff || "")
                onClicked: app.setBillable(entry.entryId, !entry.billable)
            }
            InlineField {
                objectName: "rowBegin"
                Layout.preferredWidth: 60
                horizontalAlignment: Text.AlignHCenter
                shown: entry.begin
                readOnly: row.locked
                validator: RegularExpressionValidator { regularExpression: /^\d{0,2}:?\d{0,2}$/ }
                onEditingFinished: if (text !== entry.begin) app.editTimes(entry.entryId, text, "")
            }
            Label { text: "–"; color: app.palette.muted || "#9aa0ac" }
            InlineField {
                objectName: "rowEnd"
                Layout.preferredWidth: 60
                horizontalAlignment: Text.AlignHCenter
                shown: entry.end
                readOnly: row.locked
                validator: RegularExpressionValidator { regularExpression: /^\d{0,2}:?\d{0,2}$/ }
                onEditingFinished: if (text !== entry.end) app.editTimes(entry.entryId, "", text)
            }
            Label {
                Layout.preferredWidth: 48
                horizontalAlignment: Text.AlignRight
                text: entry.total
                font.bold: true
                color: app.palette.fg || "#eceef2"
            }
            Item {  // the lock, or the same room when unlocked: the columns stay aligned
                implicitWidth: 20
                implicitHeight: 20
                Image {
                    anchors.centerIn: parent
                    visible: row.locked
                    source: "image://glyph/lock/" + (app.palette.muted || "#9aa0ac").slice(1)
                    sourceSize.width: 16; sourceSize.height: 16
                    ToolTip.visible: lockHover.hovered
                    ToolTip.text: app.texts.errExported || ""
                    HoverHandler { id: lockHover }
                }
            }
            IconButton {
                objectName: "rowResume"
                glyph: "play"
                tint: hovered ? (app.palette.start || "#16a34a") : (app.palette.muted || "#9aa0ac")
                tip: app.texts.resume || ""
                onClicked: app.resume(entry.entryId)
            }
            IconButton {
                objectName: "rowDelete"
                enabled: !row.locked
                glyph: "trash"
                tint: hovered ? (app.palette.stop || "#e02f2f") : (app.palette.muted || "#9aa0ac")
                tip: app.texts.deleteEntry || ""
                onClicked: app.deleteEntry(entry.entryId)
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
        x: Math.max(0, row.width - width - 200)
        padding: 10
        background: Rectangle {
            radius: 8
            color: app.palette.surface || "#1e2127"
            border.color: app.palette.line || "#2f333c"
        }
        contentItem: ColumnLayout {
            spacing: 8
            ProjectPicker {
                projectId: work.projectId
                onChosen: function (id) { work.projectId = id; work.activityId = 0; app.chooseRowProject(id) }
            }
            ComboBox {
                Layout.fillWidth: true
                model: app.rowActivityList  // its own: the timer bar keeps its activities
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
