// Weeks, days and entries; scrolling to the bottom loads the week before (endless, as in Toggl).
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: view
    objectName: "entriesView"
    spacing: 0

    Field {
        objectName: "search"
        Layout.fillWidth: true
        Layout.margins: 12
        placeholderText: app.texts.searchEntries || ""
        onTextChanged: app.search(text)
    }

    ListView {
        id: list
        objectName: "entriesList"
        Layout.fillWidth: true
        Layout.fillHeight: true
        clip: true
        model: app.entryList
        ScrollBar.vertical: ScrollBar {}
        onAtYEndChanged: if (atYEnd && !app.view.loading) app.loadMore()
        onCountChanged: if (count > 0 && contentHeight <= height && !app.view.loading) app.loadMore()
        footer: Label {
            width: list.width
            horizontalAlignment: Text.AlignHCenter
            padding: 12
            visible: app.view.loading
            text: app.texts.loading || ""
            color: app.palette.muted || "#9aa0ac"
        }
        delegate: Loader {
            required property var model
            required property string kind
            width: ListView.view.width
            sourceComponent: kind === "entry" ? entryRow : header
            property var row: model

            Component {
                id: header
                Rectangle {
                    implicitHeight: kind === "week" ? 40 : 30
                    color: kind === "week" ? "transparent" : (app.palette.surface || "#1e2127")
                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: 16
                        anchors.rightMargin: 16
                        Label {
                            text: row.label
                            font.bold: true
                            font.pixelSize: kind === "week" ? 15 : 12
                            color: kind === "week" ? (app.palette.fg || "#eceef2") : (app.palette.muted || "#9aa0ac")
                            Layout.fillWidth: true
                        }
                        Label {
                            text: row.total
                            font.bold: true
                            color: kind === "week" ? (app.palette.fg || "#eceef2") : (app.palette.muted || "#9aa0ac")
                        }
                    }
                }
            }
            Component {
                id: entryRow
                EntryRow { entry: row }
            }
        }
    }
}
