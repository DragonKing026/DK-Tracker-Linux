// The look of every choice (drop-down list, project, day, time): a button with the text on the
// left, an optional icon before it (calendar, clock) and an arrow after it (lists).
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Button {
    id: select
    property string glyph: ""
    property bool chevron: true
    property bool empty: false  // placeholder text: drawn fainter
    implicitHeight: 34
    leftPadding: 10
    rightPadding: 10
    HoverHandler { cursorShape: select.enabled ? Qt.PointingHandCursor : Qt.ArrowCursor }
    contentItem: RowLayout {
        spacing: 8
        Image {
            visible: select.glyph !== ""
            source: select.glyph ? "image://glyph/" + select.glyph + "/" + app.palette.muted.toString().slice(1, 7) : ""
            sourceSize.width: 15
            sourceSize.height: 15
        }
        Label {
            Layout.fillWidth: true
            text: select.text
            elide: Text.ElideRight
            color: !select.enabled ? app.palette.muted : select.empty ? app.palette.placeholder : app.palette.fg
        }
        Image {
            visible: select.chevron
            source: "image://glyph/chevron_down/" + app.palette.muted.toString().slice(1, 7)
            sourceSize.width: 14
            sourceSize.height: 14
        }
    }
    background: Rectangle {
        radius: 4
        readonly property bool over: select.enabled && (select.hovered || select.down)
        color: !select.enabled ? app.palette.panel : select.down ? app.palette.control_down
             : over ? app.palette.control_hover : app.palette.control
        border.width: 1
        border.color: select.activeFocus ? app.palette.accent
                    : over ? app.palette.border_hover : app.palette.border
    }
}
