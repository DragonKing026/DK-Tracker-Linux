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
    readonly property color projectColor: entry.projectColor || app.palette.muted
    implicitHeight: Math.max(44, content.implicitHeight + 12)
    color: hover.hovered ? app.palette.surface : app.palette.bg

    HoverHandler { id: hover; cursorShape: Qt.PointingHandCursor }
    TapHandler { onTapped: app.openEntry(entry.entryId) }  // every option in the edit window

    ColumnLayout {
        id: content
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.verticalCenter: parent.verticalCenter
        anchors.leftMargin: 16
        anchors.rightMargin: 8
        spacing: 2

        RowLayout {
            spacing: 10
            Rectangle {
                implicitWidth: 9; implicitHeight: 9; radius: 5
                color: row.projectColor
            }
            Label {
                objectName: "rowDescription"
                Layout.fillWidth: true
                Layout.minimumWidth: 150
                Layout.preferredWidth: 400
                text: entry.description
                color: app.palette.fg
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
                tint: entry.billable ? app.palette.start : app.palette.muted
                tip: entry.billable ? (app.texts.billableRowOn || "") : (app.texts.billableRowOff || "")
                onClicked: app.setBillable(entry.entryId, !entry.billable)
            }
            Label {
                objectName: "rowTimes"
                Layout.preferredWidth: 110
                horizontalAlignment: Text.AlignHCenter
                text: entry.begin + " – " + entry.end
                color: app.palette.muted
                font.features: { "tnum": 1 }
            }
            Label {
                Layout.preferredWidth: 48
                horizontalAlignment: Text.AlignRight
                text: entry.total
                font.weight: Font.Bold
                font.features: { "tnum": 1 }
                color: app.palette.fg
            }
            Item {  // the lock, or the same room when unlocked: the columns stay aligned
                implicitWidth: 20
                implicitHeight: 20
                Image {
                    anchors.centerIn: parent
                    visible: row.locked
                    source: "image://glyph/lock/" + app.palette.muted.toString().slice(1, 7)
                    sourceSize.width: 16; sourceSize.height: 16
                    ToolTip.visible: lockHover.hovered
                    ToolTip.text: app.texts.errExported || ""
                    HoverHandler { id: lockHover }
                }
            }
            IconButton {
                objectName: "rowResume"
                glyph: "play"
                tint: hovered ? app.palette.start : app.palette.muted
                tip: app.texts.resume || ""
                onClicked: app.resume(entry.entryId)
            }
            IconButton {
                objectName: "rowDelete"
                enabled: !row.locked
                glyph: "trash"
                danger: true
                tip: app.texts.deleteEntry || ""
                onClicked: app.deleteEntry(entry.entryId)
            }
        }

        Label {
            objectName: "rowError"
            visible: row.rowError !== ""
            text: row.rowError
            color: app.palette.danger
            font.pixelSize: 12
            Layout.leftMargin: 19
        }
    }

    Rectangle {
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        height: 1
        color: app.palette.divider
    }
}
