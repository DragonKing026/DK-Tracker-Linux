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
            ShapePath {
                strokeColor: modelData.color || app.palette.muted
                strokeWidth: ring.thickness
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
