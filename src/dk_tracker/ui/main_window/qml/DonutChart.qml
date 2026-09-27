// The breakdown's ring (Plan 6): one arc a slice, clockwise from twelve o'clock, a thin gap between
// slices; the period's total in the middle. Slices and their starts come ready from core/summary.py.
import QtQuick
import QtQuick.Controls
import QtQuick.Shapes

Item {
    id: ring
    objectName: "donutChart"
    property var slices: []
    property string total: ""
    property string caption: ""
    property int hot: -1  // the slice under the pointer (or of the table row under it): drawn wider
    signal hovered(int slice, real x, real y)
    signal unhovered()
    readonly property real thickness: 24
    readonly property real ringRadius: (Math.min(width, height) - thickness) / 2
    readonly property real gap: slices.length > 1 ? 1.2 : 0  // degrees
    implicitWidth: 176
    implicitHeight: 176

    Shape {  // the track, seen when there is nothing to split
        anchors.fill: parent
        preferredRendererType: Shape.CurveRenderer
        ShapePath {
            strokeColor: app.palette.divider
            strokeWidth: ring.thickness
            fillColor: "transparent"
            PathAngleArc {
                centerX: ring.width / 2
                centerY: ring.height / 2
                radiusX: ring.ringRadius
                radiusY: ring.ringRadius
                startAngle: 0
                sweepAngle: 360
            }
        }
    }
    Repeater {
        model: ring.slices
        delegate: Shape {
            required property var modelData
            anchors.fill: parent
            preferredRendererType: Shape.CurveRenderer
            required property int index
            opacity: ring.hot < 0 || ring.hot === index ? 1 : 0.4
            ShapePath {
                strokeColor: modelData.color || app.palette.muted
                strokeWidth: ring.hot === index ? ring.thickness + 8 : ring.thickness
                capStyle: ShapePath.FlatCap
                fillColor: "transparent"
                PathAngleArc {
                    centerX: ring.width / 2
                    centerY: ring.height / 2
                    radiusX: ring.ringRadius
                    radiusY: ring.ringRadius
                    startAngle: -90 + 360 * modelData.start + ring.gap / 2
                    sweepAngle: Math.max(0.6, 360 * modelData.fraction - ring.gap)
                }
            }
        }
    }
    MouseArea {  // which slice: the angle from twelve o'clock, clockwise, on the ring only
        anchors.fill: parent
        hoverEnabled: true
        acceptedButtons: Qt.NoButton
        onPositionChanged: function (mouse) {
            const dx = mouse.x - ring.width / 2, dy = mouse.y - ring.height / 2
            const distance = Math.sqrt(dx * dx + dy * dy)
            if (Math.abs(distance - ring.ringRadius) > ring.thickness / 2 + 4) {
                ring.unhovered()
                return
            }
            const turn = ((Math.atan2(dy, dx) * 180 / Math.PI + 90 + 360) % 360) / 360
            for (let i = 0; i < ring.slices.length; i++) {
                const slice = ring.slices[i]
                if (turn >= slice.start && turn < slice.start + slice.fraction) {
                    ring.hovered(i, mouse.x, mouse.y)
                    return
                }
            }
            ring.unhovered()
        }
        onExited: ring.unhovered()
    }
    Column {
        anchors.centerIn: parent
        Label {
            anchors.horizontalCenter: parent.horizontalCenter
            text: ring.total
            font.pixelSize: 20
            font.weight: Font.Bold
            color: app.palette.fg
        }
        Label {
            anchors.horizontalCenter: parent.horizontalCenter
            text: ring.caption
            font.pixelSize: 12
            color: app.palette.muted
        }
    }
}
