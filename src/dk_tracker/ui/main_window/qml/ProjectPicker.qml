// A project button that opens a searchable list grouped by customer (as the popup's picker, F-06).
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Btn {
    id: picker
    property int projectId: 0
    signal chosen(int id)

    Layout.preferredWidth: 180
    contentItem: Label {
        text: picker.text
        color: picker.projectId ? (app.palette.fg || "#eceef2") : (app.palette.muted || "#9aa0ac")
        elide: Text.ElideRight
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
    // projectsVersion: the name is read again once the projects arrive
    text: projectId ? (app.projectsVersion, app.projectName(projectId)) : (app.texts.chooseProject || "")
    onClicked: { search.text = ""; app.filterProjects(""); popup.open(); search.forceActiveFocus() }

    Popup {
        id: popup
        y: picker.height
        width: 320
        height: 360
        padding: 6
        background: Rectangle {
            radius: 4
            color: app.palette.surface || "#1e2127"
            border.color: (app.palette.border || "#5a6270")
        }
        contentItem: ColumnLayout {
            spacing: 6
            Field {
                id: search
                objectName: "projectSearch"
                Layout.fillWidth: true
                onTextChanged: app.filterProjects(text)
            }
            ListView {
                objectName: "projectList"
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                model: app.projectList
                delegate: ItemDelegate {
                    required property string kind
                    required property int projectId
                    required property string name
                    required property string color
                    width: ListView.view.width
                    enabled: kind === "project"
                    HoverHandler { cursorShape: parent.enabled ? Qt.PointingHandCursor : Qt.ArrowCursor }
                    background: Rectangle {
                        radius: 4
                        color: parent.hovered && parent.enabled ? (app.palette.surface2 || "#272b33") : "transparent"
                    }
                    contentItem: RowLayout {
                        spacing: 8
                        Rectangle {
                            visible: kind === "project"
                            width: 9; height: 9; radius: 5
                            color: parent.parent.color || (app.palette.line || "#2f333c")
                        }
                        Label {
                            text: name
                            font.bold: kind === "header"
                            color: kind === "header" ? (app.palette.muted || "#9aa0ac") : (app.palette.fg || "#eceef2")
                            Layout.fillWidth: true
                        }
                    }
                    onClicked: { popup.close(); picker.chosen(projectId) }
                }
            }
        }
    }
}
