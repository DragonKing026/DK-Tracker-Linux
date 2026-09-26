// Views on the left (Toggl-style). 0.10.0 has "Entries" and "Settings"; summaries and the calendar
// come next.
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    objectName: "sidebar"
    implicitWidth: 184
    color: app.palette.surface

    Rectangle {  // the edge towards the content
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        width: 1
        color: app.palette.divider
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 8
        spacing: 4

        RowLayout {
            Layout.margins: 8
            Layout.bottomMargin: 12
            spacing: 8
            Image {
                source: "image://icons/mark/" + app.palette.fg.toString().slice(1, 7)
                sourceSize.width: 26
                sourceSize.height: 26
            }
            Label {
                text: app.texts.appName || "DK Tracker"
                font.weight: Font.Bold
                font.pixelSize: 15
                color: app.palette.fg
            }
        }

        SideButton {
            objectName: "viewEntries"
            glyph: "list"
            text: app.texts.viewEntries || ""
            enabled: app.view.configured
            active: app.view.page === "entries"
            onClicked: app.showPage("entries")
        }

        Item { Layout.fillHeight: true }

        SideButton {
            objectName: "viewSettings"
            glyph: "gear"
            text: app.texts.navSettings || ""
            active: app.view.page === "settings"
            onClicked: app.openSettings()
        }
    }

    // A view: 36 px; the active one on a control-coloured background with an accent bar on the left.
    component SideButton: ItemDelegate {
        id: side
        property bool active: false
        property string glyph: ""
        Layout.fillWidth: true
        implicitHeight: 36
        HoverHandler { cursorShape: side.enabled ? Qt.PointingHandCursor : Qt.ArrowCursor }
        contentItem: RowLayout {
            spacing: 10
            Image {
                source: "image://glyph/" + side.glyph + "/" + (side.active ? app.palette.fg : app.palette.muted).toString().slice(1, 7)
                sourceSize.width: 18
                sourceSize.height: 18
            }
            Label {
                Layout.fillWidth: true
                text: side.text
                font.weight: side.active ? Font.DemiBold : Font.Normal
                color: side.enabled ? app.palette.fg : app.palette.placeholder
            }
        }
        background: Rectangle {
            radius: 4
            color: side.active ? app.palette.control : side.hovered && side.enabled ? app.palette.control_hover : "transparent"
            Rectangle {
                visible: side.active
                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
                width: 3
                height: parent.height - 12
                radius: 2
                color: app.palette.accent
            }
        }
    }
}
