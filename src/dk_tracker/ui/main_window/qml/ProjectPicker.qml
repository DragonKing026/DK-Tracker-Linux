// The project: a choice (SelectButton) that opens a searchable list grouped by customer, as the
// quick window's picker (F-06).
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

SelectButton {
    id: picker
    property int projectId: 0
    signal chosen(int id)

    implicitWidth: 200
    empty: projectId === 0
    // projectsVersion: the name is read again once the projects arrive
    text: projectId ? (app.projectsVersion, app.projectName(projectId)) : (app.texts.chooseProject || "")
    onClicked: { search.text = ""; app.filterProjects(""); popup.open(); search.forceActiveFocus() }

    Popup {
        id: popup
        y: picker.height + 4
        width: Math.max(picker.width, 320)
        height: Math.min(380, search.implicitHeight + projects.contentHeight + 2 * padding + 6)
        padding: 6
        background: Panel {}
        contentItem: ColumnLayout {
            spacing: 6
            Field {
                id: search
                objectName: "projectSearch"
                Layout.fillWidth: true
                placeholderText: app.texts.searchProjects || ""
                onTextChanged: app.filterProjects(text)
            }
            ListView {
                id: projects
                objectName: "projectList"
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                model: app.projectList
                delegate: ItemDelegate {
                    id: item
                    required property string kind
                    required property int projectId
                    required property string name
                    required property string color
                    width: ListView.view.width
                    height: kind === "header" ? 28 : 34
                    enabled: kind === "project"
                    HoverHandler { cursorShape: item.enabled ? Qt.PointingHandCursor : Qt.ArrowCursor }
                    contentItem: RowLayout {
                        spacing: 8
                        Rectangle {
                            visible: item.kind === "project"
                            implicitWidth: 9; implicitHeight: 9; radius: 5
                            color: item.color || app.palette.muted
                        }
                        Label {
                            Layout.fillWidth: true
                            text: item.name
                            elide: Text.ElideRight
                            font.pixelSize: item.kind === "header" ? 12 : 14
                            font.weight: item.kind === "header" ? Font.DemiBold : (item.projectId === picker.projectId ? Font.DemiBold : Font.Normal)
                            color: item.kind === "header" ? app.palette.muted : app.palette.fg
                        }
                    }
                    background: Rectangle {
                        radius: 4
                        color: item.hovered && item.enabled ? app.palette.control_hover : "transparent"
                    }
                    onClicked: { popup.close(); picker.chosen(projectId) }
                }
            }
        }
    }
}
