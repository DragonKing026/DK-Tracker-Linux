// A card of the summaries (Plan 6): a number tile, the chart, the breakdown. One step up from the
// page (`surface`), a quiet edge, radius 8. docs/architektura/wyglad-okna-glownego.md
import QtQuick

Rectangle {
    radius: 8
    color: app.palette.surface
    border.width: 1
    border.color: app.palette.divider
}
