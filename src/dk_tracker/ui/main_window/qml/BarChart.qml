// The summaries' bar chart (Plan 6): a bar a day (or a month), in layers of project colours, the
// norm as a dashed line (daily bars) or a mark over each bar (monthly bars), a tooltip with the
// split. Every number and text comes ready from core/summary.py.
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Shapes

Item {
    id: chart
    objectName: "barChart"
    property var summary: ({})
    readonly property var bars: summary.bars || []
    readonly property int scaleTop: summary.scaleTop || 3600
    readonly property int axisWidth: 44
    readonly property int labelHeight: 22
    readonly property real plotX: axisWidth + 4
    readonly property real plotWidth: Math.max(0, width - plotX)
    readonly property real plotHeight: Math.max(0, height - labelHeight - 8)
    readonly property real slot: bars.length ? plotWidth / bars.length : 0
    readonly property real barWidth: Math.max(2, Math.min(slot * 0.62, 44))
    property int hovered: -1
    implicitHeight: 240

    function yOf(seconds) { return 8 + plotHeight - seconds / scaleTop * plotHeight }

    // The hour lines and their labels.
    Repeater {
        model: chart.summary.ticks || []
        delegate: Item {
            required property var modelData
            Rectangle {
                x: chart.plotX
                y: chart.yOf(modelData.seconds)
                width: chart.plotWidth
                height: 1
                color: app.palette.divider
            }
            Label {
                width: chart.axisWidth - 6
                y: chart.yOf(modelData.seconds) - height / 2
                horizontalAlignment: Text.AlignRight
                text: modelData.label
                font.pixelSize: 11
                color: app.palette.muted
            }
        }
    }

    // The bars.
    Repeater {
        model: chart.bars
        delegate: Item {
            id: column
            required property var modelData
            required property int index
            readonly property var bar: modelData
            x: chart.plotX + index * chart.slot
            width: chart.slot
            height: chart.height

            Rectangle {  // under the pointer: the whole column lights up, so thin bars are easy to hit
                visible: chart.hovered === column.index && column.bar.seconds > 0
                x: (parent.width - Math.min(parent.width - 2, chart.barWidth + 12)) / 2
                y: 4
                width: Math.min(parent.width - 2, chart.barWidth + 12)
                height: chart.plotHeight + 6
                radius: 4
                color: app.palette.control
            }
            Repeater {
                model: column.bar.parts
                delegate: Rectangle {
                    required property var modelData
                    required property int index
                    readonly property bool last: index === column.bar.parts.length - 1
                    x: (column.width - chart.barWidth) / 2
                    width: chart.barWidth
                    y: chart.yOf(modelData.below + modelData.seconds)
                    // A 1 px seam between two layers; the top layer has its corners rounded.
                    height: Math.max(1, modelData.seconds / chart.scaleTop * chart.plotHeight - (index > 0 ? 1 : 0))
                    topLeftRadius: last ? 3 : 0
                    topRightRadius: last ? 3 : 0
                    color: modelData.color || app.palette.muted
                }
            }
            Rectangle {  // monthly bars: the norm for the days worked, over each bar
                visible: chart.summary.unit === "month" && column.bar.norm > 0
                x: (column.width - chart.barWidth) / 2 - 3
                width: chart.barWidth + 6
                y: chart.yOf(column.bar.norm) - 1
                height: 2
                radius: 1
                color: app.palette.fg
                opacity: 0.55
            }
            Label {
                anchors.horizontalCenter: parent.horizontalCenter
                y: chart.height - chart.labelHeight + 4
                text: column.bar.label
                font.pixelSize: 11
                font.weight: column.bar.today ? Font.Bold : Font.Normal
                color: column.bar.today ? app.palette.accent : app.palette.muted
            }
            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                acceptedButtons: Qt.NoButton
                onPositionChanged: function (mouse) {
                    chart.hovered = column.index
                    if (column.bar.seconds > 0)
                        tip.follow(this, mouse.x, mouse.y)
                    else
                        tip.close()
                }
                onExited: {
                    if (chart.hovered === column.index)
                        chart.hovered = -1
                    tip.close()
                }
            }
        }
    }

    // Daily bars: the norm as one dashed line.
    Shape {
        objectName: "normLine"
        visible: (chart.summary.normLine || 0) > 0
        anchors.fill: parent
        ShapePath {
            strokeColor: app.palette.fg
            strokeWidth: 1.5
            strokeStyle: ShapePath.DashLine
            dashPattern: [4, 3]
            fillColor: "transparent"
            startX: chart.plotX
            startY: chart.yOf(chart.summary.normLine || 0)
            PathLine { x: chart.width; y: chart.yOf(chart.summary.normLine || 0) }
        }
        opacity: 0.55
    }

    // The tooltip: the day or month, its total, each project with its entries (live test of 0.10.3),
    // the norm. In the window's overlay, beside the pointer, as the breakdown's.
    Popup {
        id: tip
        objectName: "barTip"
        readonly property var bar: chart.hovered >= 0 && chart.hovered < chart.bars.length ? chart.bars[chart.hovered] : null
        property point pointer: Qt.point(0, 0)
        parent: Overlay.overlay
        width: 320
        padding: 12
        closePolicy: Popup.NoAutoClose
        focus: false
        background: Panel {}

        function follow(item, x, y) {
            pointer = item.mapToItem(parent, x, y)
            if (!opened)
                open()
            place()
        }
        function place() {
            if (!parent)
                return
            const right = pointer.x + 18
            x = right + width <= parent.width - 8 ? right : Math.max(8, pointer.x - 18 - width)
            const below = pointer.y + 18
            y = below + height <= parent.height - 8 ? below : Math.max(8, pointer.y - 18 - height)
        }
        onHeightChanged: place()

        contentItem: ColumnLayout {
            spacing: 4
            RowLayout {
                Layout.fillWidth: true
                Label {
                    Layout.fillWidth: true
                    text: tip.bar ? tip.bar.title : ""
                    font.weight: Font.DemiBold
                    color: app.palette.fg
                    elide: Text.ElideRight
                }
                Label {
                    text: tip.bar ? tip.bar.total : ""
                    font.weight: Font.DemiBold
                    color: app.palette.fg
                }
            }
            Repeater {
                // The biggest of this bar first (the layers keep the period's order).
                model: tip.bar ? tip.bar.parts.slice().sort((a, b) => b.seconds - a.seconds) : []
                delegate: ColumnLayout {
                    id: project
                    required property var modelData
                    Layout.fillWidth: true
                    Layout.topMargin: 4
                    spacing: 2
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 6
                        Rectangle { width: 8; height: 8; radius: 4; color: project.modelData.color || app.palette.muted }
                        Label {
                            Layout.fillWidth: true
                            text: project.modelData.name
                            elide: Text.ElideRight
                            font.pixelSize: 13
                            font.weight: Font.DemiBold
                            color: app.palette.fg
                        }
                        Label { text: project.modelData.time; font.pixelSize: 13; color: app.palette.fg }
                    }
                    Repeater {
                        model: project.modelData.entries
                        delegate: RowLayout {
                            required property var modelData
                            Layout.fillWidth: true
                            Layout.leftMargin: 14
                            spacing: 12
                            Label {
                                Layout.fillWidth: true
                                text: modelData.text
                                textFormat: Text.PlainText
                                elide: Text.ElideRight
                                font.pixelSize: 12
                                color: app.palette.fg
                            }
                            Label { text: modelData.time; font.pixelSize: 12; color: app.palette.muted }
                        }
                    }
                    Label {
                        visible: text !== ""
                        Layout.leftMargin: 14
                        text: project.modelData.more
                        font.pixelSize: 12
                        color: app.palette.muted
                    }
                }
            }
            Label {
                visible: text !== ""
                Layout.topMargin: 4
                text: tip.bar ? tip.bar.normText : ""
                font.pixelSize: 12
                color: app.palette.muted
            }
        }
    }
}
