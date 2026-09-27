// The breakdown's tooltip (live test of 0.10.3, as in Toggl): what a ring slice or a table row holds —
// its descriptions with their time, biggest first. In the window's overlay, so the scrolled page
// does not cut it; placed beside the pointer, never under it (it would take the hover away).
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Popup {
    id: tip
    objectName: "shareTip"
    property var share: null  // {name, detail, color, time, percent, entries, more}
    parent: Overlay.overlay
    width: 340
    padding: 12
    closePolicy: Popup.NoAutoClose
    focus: false
    background: Panel {}

    property point pointer: Qt.point(0, 0)  // in the overlay

    // Beside the pointer (`item` coordinates); to the left or above when the window ends.
    function follow(item, x, y) {
        pointer = item.mapToItem(parent, x, y)
        if (!opened)
            open()
        place()
    }
    function place() {
        if (!parent)
            return  // not in the overlay yet
        const right = pointer.x + 18
        x = right + width <= parent.width - 8 ? right : Math.max(8, pointer.x - 18 - width)
        const below = pointer.y + 18
        y = below + height <= parent.height - 8 ? below : Math.max(8, pointer.y - 18 - height)
    }
    onHeightChanged: place()  // the list is laid out after opening: a first guess would run off the window

    contentItem: ColumnLayout {
        spacing: 6
        RowLayout {
            Layout.fillWidth: true
            spacing: 8
            Rectangle {
                Layout.alignment: Qt.AlignTop
                Layout.topMargin: 5
                width: 10
                height: 10
                radius: 5
                color: tip.share && tip.share.color ? tip.share.color : app.palette.muted
            }
            Label {
                Layout.fillWidth: true
                text: tip.share ? tip.share.name : ""
                textFormat: Text.PlainText
                font.weight: Font.DemiBold
                wrapMode: Text.Wrap
                color: app.palette.fg
            }
            Label {
                Layout.alignment: Qt.AlignTop
                text: tip.share ? tip.share.time + "  ·  " + tip.share.percent : ""
                font.weight: Font.DemiBold
                color: app.palette.fg
            }
        }
        Label {
            visible: text !== ""
            Layout.fillWidth: true
            text: tip.share && tip.share.detail ? tip.share.detail : ""
            font.pixelSize: 12
            elide: Text.ElideRight
            color: app.palette.muted
        }
        Rectangle { Layout.fillWidth: true; implicitHeight: 1; color: app.palette.divider }
        Repeater {
            model: tip.share ? tip.share.entries : []
            delegate: RowLayout {
                required property var modelData
                Layout.fillWidth: true
                spacing: 12
                Label {
                    Layout.fillWidth: true
                    text: modelData.text
                    textFormat: Text.PlainText
                    elide: Text.ElideRight
                    font.pixelSize: 13
                    color: app.palette.fg
                }
                Label { text: modelData.time; font.pixelSize: 13; color: app.palette.muted }
            }
        }
        Label {
            visible: text !== ""
            text: tip.share ? tip.share.more : ""
            font.pixelSize: 12
            color: app.palette.muted
        }
    }
}
