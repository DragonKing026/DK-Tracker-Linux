// A project button that opens a searchable list grouped by customer (as the popup's picker, F-06).
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Button {
    id: picker
    property int projectId: 0
    signal chosen(int id)

    Layout.preferredWidth: 200
    text: projectId ? app.projectName(projectId) : (app.texts.chooseProject || "")
    onClicked: { search.text = ""; app.filterProjects(""); popup.open(); search.forceActiveFocus() }

    Popup {
        id: popup
        y: picker.height
        width: 320
        height: 360
        padding: 6
        contentItem: ColumnLayout {
            spacing: 6
            TextField {
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
