// "Entry deleted · Undo": the delete reaches Kimai only when this goes away (Python's timer).
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Panel {
    objectName: "undoBar"
    visible: app.view.undo !== ""
    implicitWidth: undoRow.implicitWidth + 24
    implicitHeight: 48

    RowLayout {
        id: undoRow
        anchors.centerIn: parent
        spacing: 16
        Label { text: app.view.undo; color: app.palette.fg }
        Btn {
            objectName: "undo"
            variant: "primary"
            text: app.texts.undo || ""
            onClicked: app.undoDelete()
        }
    }
}
