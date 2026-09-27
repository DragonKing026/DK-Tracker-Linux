// The main window (Plan 5): sidebar, timer bar, the entry list. Logic lives in Python (`app`).
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: root
    objectName: "mainWindow"
    minimumWidth: 800
    minimumHeight: 560
    title: app.texts.appName || "DK Tracker"
    color: app.palette.bg
    font.pixelSize: 14
    onClosing: app.closeWindow()

    // The Basic style's own parts (scroll bars, tool tips, text selection) in our colours.
    palette.window: app.palette.bg
    palette.windowText: app.palette.fg
    palette.base: app.palette.input
    palette.alternateBase: app.palette.surface
    palette.text: app.palette.fg
    palette.button: app.palette.control
    palette.buttonText: app.palette.fg
    palette.highlight: app.palette.accent
    palette.highlightedText: "#ffffff"
    palette.placeholderText: app.palette.placeholder
    palette.toolTipBase: app.palette.panel
    palette.toolTipText: app.palette.fg
    palette.mid: app.palette.border
    palette.midlight: app.palette.control_hover
    palette.dark: app.palette.border_hover
    palette.light: app.palette.control

    RowLayout {
        anchors.fill: parent
        spacing: 0

        Sidebar {
            Layout.fillHeight: true
        }

        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 0

            TimerBar {
                id: timerBar
                enabled: !app.view.offline  // spec, section 9: no edits without Kimai
                Layout.fillWidth: true
                visible: app.view.configured
            }

            Rectangle {
                objectName: "errorBar"
                Layout.fillWidth: true
                visible: app.view.error !== ""
                implicitHeight: errorText.implicitHeight + 16
                color: app.palette.danger_bg
                Rectangle {
                    anchors.left: parent.left
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    width: 3
                    color: app.palette.danger
                }
                Label {
                    id: errorText
                    anchors.fill: parent
                    anchors.margins: 8
                    anchors.leftMargin: 16
                    text: app.view.error
                    color: app.palette.fg
                    wrapMode: Text.Wrap
                }
            }

            EntriesView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                visible: app.view.configured && app.view.page === "entries"
            }

            SummaryView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                visible: app.view.configured && app.view.page === "summary"
            }

            SettingsView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                visible: app.view.page === "settings"
            }
        }
    }

    EntryDialog {}

    UndoBar {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 16
    }

}
