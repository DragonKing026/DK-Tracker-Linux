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
    color: app.palette.bg || "#16181d"
    font.pixelSize: 14
    onClosing: app.closeWindow()

    // The Basic style draws its controls from this palette: our theme, light or dark.
    palette.window: app.palette.bg || "#16181d"
    palette.windowText: app.palette.fg || "#eceef2"
    palette.base: app.palette.surface || "#1e2127"
    palette.alternateBase: app.palette.surface2 || "#272b33"
    palette.text: app.palette.fg || "#eceef2"
    palette.button: app.palette.surface2 || "#272b33"
    palette.buttonText: app.palette.fg || "#eceef2"
    palette.highlight: app.palette.accent || "#6f9bff"
    palette.highlightedText: "#ffffff"
    palette.placeholderText: app.palette.muted || "#9aa0ac"
    palette.mid: app.palette.line || "#2f333c"
    palette.midlight: app.palette.line || "#2f333c"
    palette.dark: app.palette.line || "#2f333c"
    palette.light: app.palette.surface2 || "#272b33"

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
                color: app.palette.err_bg || "#3a1a1a"
                Label {
                    id: errorText
                    anchors.fill: parent
                    anchors.margins: 8
                    text: app.view.error
                    color: app.palette.err_fg || "#ff9d9d"
                    wrapMode: Text.Wrap
                }
            }

            ColumnLayout {
                objectName: "unconfigured"
                visible: !app.view.configured
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.margins: 24
                spacing: 16
                Item { Layout.fillHeight: true }
                Label {
                    Layout.alignment: Qt.AlignHCenter
                    text: app.texts.notConfigured || ""
                    color: app.palette.muted || "#9aa0ac"
                }
                Button {
                    objectName: "openSettings"
                    Layout.alignment: Qt.AlignHCenter
                    text: app.texts.openSettings || ""
                    onClicked: app.openSettings()
                }
                Item { Layout.fillHeight: true }
            }

            EntriesView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                visible: app.view.configured
            }
        }
    }

    UndoBar {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 16
    }

    Connections {
        target: app
        function onPrefill(values) { timerBar.fillManual(values) }
    }
}
