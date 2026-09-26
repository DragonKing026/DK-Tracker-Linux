// One entry: the description (two lines), project · activity, $, the hours. A click opens the edit
// window with every option of the entry; $, ▶ and the bin act at once. An exported entry is locked.
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

    HoverHandler { id: hover; cursorShape: Qt.PointingHandCursor }
    TapHandler { onTapped: app.openEntry(entry.entryId) }  // every option in the edit window

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
            Label {
                objectName: "rowDescription"
                Layout.fillWidth: true
                Layout.minimumWidth: 150
                Layout.preferredWidth: 400
                text: entry.description
                color: app.palette.fg || "#eceef2"
                wrapMode: Text.Wrap
                maximumLineCount: 2  // the whole text in the edit window
                elide: Text.ElideRight
            }
            Label {
                objectName: "rowWork"
                Layout.fillWidth: true
                Layout.minimumWidth: 60
                Layout.maximumWidth: 280
                text: entry.projectName + (entry.activityName ? " · " + entry.activityName : "")
                color: row.projectColor
                elide: Text.ElideRight
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
            Label {
                objectName: "rowTimes"
                Layout.preferredWidth: 110
                horizontalAlignment: Text.AlignHCenter
                text: entry.begin + " – " + entry.end
                color: app.palette.fg || "#eceef2"
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

    Rectangle {
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        height: 1
        color: app.palette.line || "#2f333c"
    }
}
