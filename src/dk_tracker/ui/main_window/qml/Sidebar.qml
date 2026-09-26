// Views on the left (Toggl-style). 0.10.0 has "Entries" only; summaries and the calendar come next.
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    objectName: "sidebar"
    implicitWidth: 180
    color: app.palette.surface || "#1e2127"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 8
        spacing: 4

        RowLayout {
            Layout.margins: 8
            spacing: 8
            Image { source: "image://icons/mark"; sourceSize.width: 24; sourceSize.height: 24 }
            Label {
                text: app.texts.appName || "DK Tracker"
                font.bold: true
                color: app.palette.fg || "#eceef2"
            }
        }

        SideButton {
            objectName: "viewEntries"
            icon.source: "image://glyph/list/" + (app.palette.fg || "#eceef2").slice(1)
            text: app.texts.viewEntries || ""
            enabled: app.view.configured
            active: app.view.page === "entries"
            onClicked: app.showPage("entries")
        }

        Item { Layout.fillHeight: true }

        SideButton {
            objectName: "viewSettings"
            icon.source: "image://glyph/gear/" + (app.palette.fg || "#eceef2").slice(1)
            text: app.texts.navSettings || ""
            active: app.view.page === "settings"
            onClicked: app.openSettings()
        }
    }

    component SideButton: ItemDelegate {
        Layout.fillWidth: true
        HoverHandler { cursorShape: parent.enabled ? Qt.PointingHandCursor : Qt.ArrowCursor }
        property bool active: false
        icon.width: 18
        icon.height: 18
        icon.color: "transparent"
        contentItem: RowLayout {
            spacing: 10
            Image { source: parent.parent.icon.source; sourceSize.width: 18; sourceSize.height: 18 }
            Label { text: parent.parent.text; color: app.palette.fg || "#eceef2"; Layout.fillWidth: true }
        }
        background: Rectangle {
            radius: 6
            color: parent.active ? (app.palette.surface2 || "#272b33") : (parent.hovered ? (app.palette.line || "#2f333c") : "transparent")
        }
    }
}
