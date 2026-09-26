// "Entry deleted · Undo": the delete reaches Kimai only when this goes away (Python's timer).
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    objectName: "undoBar"
    visible: app.view.undo !== ""
    implicitWidth: undoRow.implicitWidth + 24
    implicitHeight: 44
    radius: 5
    color: app.palette.surface2 || "#272b33"
    border.color: (app.palette.border || "#6b7486")

    RowLayout {
        id: undoRow
        anchors.centerIn: parent
        spacing: 16
        Label { text: app.view.undo; color: app.palette.fg || "#eceef2" }
        Btn {
            objectName: "undo"
            flat: true
            text: app.texts.undo || ""
            onClicked: app.undoDelete()
        }
    }
}
