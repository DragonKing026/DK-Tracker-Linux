// The scroll bar of every list and page: a rounded 6 px handle in the theme's edge colour, always
// shown while there is more to scroll (a long project list gave no sign of it — live test).
import QtQuick
import QtQuick.Controls

ScrollBar {
    id: bar
    policy: size < 1 ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
    padding: 2
    contentItem: Rectangle {
        implicitWidth: 6
        implicitHeight: 6
        radius: 3
        color: bar.pressed ? app.palette.muted : bar.hovered ? app.palette.border_hover : app.palette.border
    }
    background: Item {}
}
