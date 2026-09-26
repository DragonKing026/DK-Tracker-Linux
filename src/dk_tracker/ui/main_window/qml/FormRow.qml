// One line of a form: the label on the left (fixed width, so the fields line up), the control(s)
// on the right. Used by the edit window and the settings page.
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RowLayout {
    id: row
    property alias label: caption.text
    property int labelWidth: 130
    default property alias content: holder.data
    Layout.fillWidth: true
    spacing: 12

    Label {
        id: caption
        Layout.preferredWidth: row.labelWidth
        Layout.alignment: Qt.AlignTop
        Layout.topMargin: 8
        font.pixelSize: 13
        font.weight: Font.DemiBold
        color: app.palette.muted
        wrapMode: Text.Wrap  // a long label takes two lines rather than losing its end
    }
    RowLayout {
        id: holder
        Layout.fillWidth: true
        spacing: 8
    }
}
