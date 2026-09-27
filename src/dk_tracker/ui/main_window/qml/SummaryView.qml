// Summaries (Plan 6, spec 0.10 section 6): the period, the numbers, the bars, the breakdown.
// Everything shown is `app.summaryPage.data`, counted and worded in Python (core/summary.py).
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ScrollView {
    id: page
    objectName: "summaryView"
    readonly property var d: app.summaryPage.data
    readonly property bool dim: d.loading && d.loaded  // a refresh: the numbers stay, a little faded
    readonly property string none: "–"  // a new period still loading
    contentWidth: availableWidth
    clip: true
    background: Rectangle { color: app.palette.bg }
    ScrollBar.vertical: Scroller {
        parent: page
        x: page.width - width
        height: page.availableHeight
    }

    // The range's two days follow the period when it is moved with the arrows.
    Connections {
        target: app.summaryPage
        function onDataChanged() {
            rangeFirst.value = page.d.first
            rangeLast.value = page.d.last
        }
    }

    ColumnLayout {
        width: page.availableWidth - 32
        x: 16
        spacing: 12

        // -- the period ------------------------------------------------------------------
        Flow {
            Layout.fillWidth: true
            Layout.topMargin: 16
            spacing: 12

            Segmented {
                objectName: "summaryKind"
                current: page.d.kind || "week"
                options: [
                    { code: "week", label: app.texts.sumWeek || "" },
                    { code: "month", label: app.texts.sumMonth || "" },
                    { code: "year", label: app.texts.sumYear || "" },
                    { code: "range", label: app.texts.sumRange || "" },
                ]
                onChosen: function (code) { app.summaryPage.setPeriod(code) }
            }
            RowLayout {
                spacing: 4
                height: 34
                IconButton {
                    objectName: "summaryPrevious"
                    glyph: "chevron_left"
                    tip: app.texts.sumPrevious || ""
                    onClicked: app.summaryPage.step(-1)
                }
                Label {
                    objectName: "summaryLabel"
                    visible: page.d.kind !== "range"
                    Layout.minimumWidth: 150
                    horizontalAlignment: Text.AlignHCenter
                    text: page.d.label || ""
                    font.pixelSize: 15
                    font.weight: Font.DemiBold
                    color: app.palette.fg
                }
                DateField {
                    id: rangeFirst
                    objectName: "summaryRangeFirst"
                    visible: page.d.kind === "range"
                    implicitWidth: 176
                    value: page.d.first || ""
                    onEdited: app.summaryPage.setRange(value, rangeLast.value)
                }
                Label { visible: page.d.kind === "range"; text: "–"; color: app.palette.muted }
                DateField {
                    id: rangeLast
                    objectName: "summaryRangeLast"
                    visible: page.d.kind === "range"
                    implicitWidth: 176
                    value: page.d.last || ""
                    onEdited: app.summaryPage.setRange(rangeFirst.value, value)
                }
                IconButton {
                    objectName: "summaryNext"
                    glyph: "chevron_right"
                    tip: app.texts.sumNext || ""
                    onClicked: app.summaryPage.step(1)
                }
                Btn {
                    objectName: "summaryToday"
                    Layout.leftMargin: 4
                    text: app.texts.sumCurrent || ""
                    enabled: !page.d.isToday
                    onClicked: app.summaryPage.today()
                }
                Label {
                    objectName: "summaryLoading"
                    Layout.leftMargin: 8
                    visible: page.d.loading && page.d.loaded  // a new period says it in the chart
                    text: app.texts.loading || ""
                    color: app.palette.muted
                }
            }
        }

        // -- the numbers ---------------------------------------------------------------
        RowLayout {
            Layout.fillWidth: true
            spacing: 12
            opacity: page.dim ? 0.6 : 1

            Tile {
                objectName: "tileTotal"
                label: app.texts.sumTotal || ""
                value: page.d.loaded ? page.d.total : page.none
                note: page.d.daysWith || ""
            }
            Tile {
                objectName: "tilePaid"
                label: app.texts.sumPaid || ""
                value: page.d.loaded ? page.d.paid : page.none
                extra: page.d.paidPercent || ""
                note: page.d.unpaidLine || ""
                fraction: page.d.paidFraction || 0
                barColor: app.palette.start
                showBar: page.d.loaded === true
            }
            Tile {
                objectName: "tileAverage"
                label: app.texts.sumAvgDay || ""
                value: page.d.loaded ? page.d.avgDay : page.none
                note: page.d.normText || ""
                fraction: page.d.normFraction || 0
                barColor: app.palette.accent
                showBar: (page.d.normText || "") !== ""
            }
        }

        // -- the bars ------------------------------------------------------------------
        Card {
            Layout.fillWidth: true
            implicitHeight: chartColumn.implicitHeight + 32
            opacity: page.dim ? 0.6 : 1
            ColumnLayout {
                id: chartColumn
                x: 16
                y: 16
                width: parent.width - 32
                spacing: 8
                Label {
                    text: page.d.unit === "month" ? app.texts.sumChartMonths || "" : app.texts.sumChartDays || ""
                    font.pixelSize: 13
                    font.weight: Font.DemiBold
                    color: app.palette.muted
                }
                BarChart {
                    Layout.fillWidth: true
                    implicitHeight: 240
                    summary: page.d
                    Empty {
                        visible: !page.d.loaded || page.d.empty
                        text: page.d.loaded ? app.texts.sumEmpty || "" : app.texts.loading || ""
                    }
                }
            }
        }

        // -- the breakdown ---------------------------------------------------------------
        Card {
            Layout.fillWidth: true
            Layout.bottomMargin: 16
            implicitHeight: breakdown.implicitHeight + 32
            opacity: page.dim ? 0.6 : 1
            ColumnLayout {
                id: breakdown
                x: 16
                y: 16
                width: parent.width - 32
                spacing: 12
                RowLayout {
                    Layout.fillWidth: true
                    Label {
                        Layout.fillWidth: true
                        text: app.texts.sumBreakdown || ""
                        font.pixelSize: 13
                        font.weight: Font.DemiBold
                        color: app.palette.muted
                    }
                    Segmented {
                        objectName: "summaryGroup"
                        current: page.d.group || "project"
                        options: [
                            { code: "project", label: app.texts.sumByProject || "" },
                            { code: "customer", label: app.texts.sumByCustomer || "" },
                            { code: "activity", label: app.texts.sumByActivity || "" },
                        ]
                        onChosen: function (code) { app.summaryPage.setGroup(code) }
                    }
                }
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 24
                    DonutChart {
                        Layout.alignment: Qt.AlignTop
                        slices: page.d.slices || []
                        total: page.d.loaded ? page.d.total : page.none
                        caption: app.texts.sumTotal || ""
                    }
                    ColumnLayout {
                        objectName: "shareTable"
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignTop
                        spacing: 0
                        ShareRow {
                            header: true
                            name: page.d.group === "customer" ? app.texts.sumByCustomer || ""
                                : page.d.group === "activity" ? app.texts.sumByActivity || "" : app.texts.sumByProject || ""
                            time: app.texts.sumColTime || ""
                            percent: app.texts.sumColShare || ""
                            paid: app.texts.sumColPaid || ""
                        }
                        Repeater {
                            model: page.d.shares || []
                            delegate: ShareRow {
                                required property var modelData
                                color: modelData.color
                                name: modelData.name
                                detail: modelData.detail
                                time: modelData.time
                                percent: modelData.percent
                                paid: modelData.paid
                            }
                        }
                        Label {
                            visible: !page.d.loaded || page.d.empty
                            Layout.topMargin: 12
                            text: page.d.loaded ? app.texts.sumEmpty || "" : app.texts.loading || ""
                            color: app.palette.muted
                        }
                    }
                }
            }
        }
    }

    // A number: a label, the value large, a line under it and an optional thin bar.
    component Tile: Card {
        id: tile
        property string label: ""
        property string value: ""
        property string extra: ""
        property string note: ""
        property real fraction: 0
        property color barColor: app.palette.accent
        property bool showBar: false
        Layout.fillWidth: true
        Layout.fillHeight: true  // one height for the row, bar or no bar
        Layout.preferredWidth: 1  // equal widths, whatever the numbers
        implicitHeight: tileColumn.implicitHeight + 28
        ColumnLayout {
            id: tileColumn
            x: 14
            y: 14
            width: parent.width - 28
            spacing: 4
            Label {
                Layout.fillWidth: true
                text: tile.label
                font.pixelSize: 12
                color: app.palette.muted
                elide: Text.ElideRight
            }
            RowLayout {
                spacing: 6
                Label {
                    text: tile.value
                    font.pixelSize: 22
                    font.weight: Font.Bold
                    color: app.palette.fg
                }
                Label {
                    visible: tile.extra !== ""
                    Layout.alignment: Qt.AlignBaseline
                    text: tile.extra
                    font.pixelSize: 13
                    color: app.palette.muted
                }
            }
            Rectangle {  // e.g. billable against all, the daily average against the norm
                visible: tile.showBar
                Layout.fillWidth: true
                Layout.topMargin: 2
                implicitHeight: 4
                radius: 2
                color: app.palette.divider
                Rectangle {
                    width: parent.width * Math.min(1, tile.fraction)
                    height: parent.height
                    radius: 2
                    color: tile.barColor
                }
            }
            Label {
                Layout.fillWidth: true
                visible: tile.note !== ""
                text: tile.note
                font.pixelSize: 12
                color: app.palette.muted
                elide: Text.ElideRight
            }
        }
    }

    // A row of the breakdown table (or its header).
    component ShareRow: Item {
        id: share
        property bool header: false
        property string color: ""
        property string name: ""
        property string detail: ""
        property string time: ""
        property string percent: ""
        property string paid: ""
        Layout.fillWidth: true
        implicitHeight: header ? 28 : 34
        RowLayout {
            anchors.fill: parent
            spacing: 10
            Rectangle {
                visible: !share.header
                width: 10
                height: 10
                radius: 5
                color: share.color || app.palette.muted
            }
            Label {
                Layout.fillWidth: true
                elide: Text.ElideRight
                textFormat: Text.PlainText
                text: share.detail ? share.name + "  ·  " + share.detail : share.name
                font.pixelSize: share.header ? 12 : 14
                color: share.header ? app.palette.muted : app.palette.fg
            }
            Cell { text: share.time; strong: !share.header; header: share.header; width: 64 }
            Cell { text: share.percent; header: share.header; width: 56 }
            Cell { text: share.paid; header: share.header; width: 96 }
        }
        Rectangle {
            anchors.bottom: parent.bottom
            width: parent.width
            height: 1
            color: app.palette.divider
        }
    }
    component Cell: Label {
        property bool header: false
        property bool strong: false
        Layout.preferredWidth: width
        horizontalAlignment: Text.AlignRight
        font.pixelSize: header ? 12 : 14
        font.weight: strong ? Font.DemiBold : Font.Normal
        color: header || !strong ? app.palette.muted : app.palette.fg
        elide: Text.ElideLeft
    }
    component Empty: Label {
        anchors.centerIn: parent
        text: app.texts.sumEmpty || ""
        color: app.palette.muted
    }
}
