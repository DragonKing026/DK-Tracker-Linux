// A drop-down list with the SelectButton look; its list is a Panel.
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ComboBox {
    id: combo
    implicitHeight: 34
    leftPadding: 10
    rightPadding: 10
    HoverHandler { cursorShape: combo.enabled ? Qt.PointingHandCursor : Qt.ArrowCursor }
    indicator: Image {
        x: combo.width - width - 10
        y: (combo.height - height) / 2
        source: "image://glyph/chevron_down/" + app.palette.muted.toString().slice(1, 7)
        sourceSize.width: 14
        sourceSize.height: 14
    }
    contentItem: Label {
        leftPadding: 0
        rightPadding: combo.indicator.width + 8
        text: combo.displayText
        elide: Text.ElideRight
        verticalAlignment: Text.AlignVCenter
        color: !combo.enabled ? app.palette.muted : combo.currentIndex < 0 ? app.palette.placeholder : app.palette.fg
    }
    background: Rectangle {
        radius: 4
        readonly property bool over: combo.enabled && combo.hovered
        color: !combo.enabled ? app.palette.panel : combo.down ? app.palette.control_down
             : over ? app.palette.control_hover : app.palette.control
        border.width: 1
        border.color: combo.activeFocus || combo.popup.visible ? app.palette.accent
                    : over ? app.palette.border_hover : app.palette.border
    }
    popup.background: Panel {}
    popup.padding: 4
    popup.contentItem: ListView {
        clip: true
        implicitHeight: Math.min(contentHeight, 320)
        model: combo.popup.visible ? combo.delegateModel : null
        currentIndex: combo.highlightedIndex
        ScrollBar.vertical: Scroller {}
    }
    delegate: ItemDelegate {
        required property var model
        required property int index
        width: ListView.view ? ListView.view.width : combo.width
        highlighted: combo.highlightedIndex === index
        HoverHandler { cursorShape: Qt.PointingHandCursor }
        contentItem: Label {
            text: model[combo.textRole]
            elide: Text.ElideRight
            color: app.palette.fg
            font.weight: index === combo.currentIndex ? Font.DemiBold : Font.Normal
        }
        background: Rectangle {
            radius: 4
            color: parent.highlighted || parent.hovered ? app.palette.control_hover : "transparent"
        }
    }
}
