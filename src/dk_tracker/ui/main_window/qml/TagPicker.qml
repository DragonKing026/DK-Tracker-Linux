// Tags chosen from the list Kimai has (as in Kimai's own form): the chosen ones as chips in their
// colours (× removes), "+ tag" opens the list with a search; a name that is not there can be added —
// Kimai keeps it only for accounts that may create tags, and the app says when it did not.
// Outside it is a text "a, b" (Tracker.save_details), so the rest of the window stays the same.
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: picker
    property string text: ""
    property var chosen: []
    property bool syncing: false
    readonly property var options: app.tagOptions
    implicitHeight: Math.max(34, flow.implicitHeight + 8)
    radius: 4
    color: enabled ? app.palette.input : app.palette.panel
    border.width: 1
    border.color: app.palette.border

    function parse(text) { return text.split(",").map(t => t.trim()).filter(t => t !== "") }
    function publish() { syncing = true; text = chosen.join(", "); syncing = false }
    function add(name) { if (chosen.indexOf(name) < 0) { chosen = chosen.concat([name]); publish() } }
    function remove(name) { chosen = chosen.filter(t => t !== name); publish() }
    function colorOf(name) {
        for (let i = 0; i < options.length; i++) if (options[i].name === name) return options[i].color
        return app.palette.muted
    }
    onTextChanged: if (!syncing) chosen = parse(text)

    Flow {
        id: flow
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.verticalCenter: parent.verticalCenter
        anchors.margins: 4
        spacing: 4

        Repeater {
            model: picker.chosen
            delegate: Rectangle {
                required property string modelData
                implicitHeight: 26
                implicitWidth: chip.implicitWidth + 12
                radius: 4
                color: app.palette.control
                border.width: 1
                border.color: app.palette.border
                RowLayout {
                    id: chip
                    anchors.centerIn: parent
                    spacing: 6
                    Rectangle { implicitWidth: 8; implicitHeight: 8; radius: 4; color: picker.colorOf(modelData) }
                    Label { text: modelData; color: app.palette.fg; font.pixelSize: 13 }
                    IconButton {
                        visible: picker.enabled
                        implicitWidth: 20
                        implicitHeight: 20
                        icon.width: 12
                        icon.height: 12
                        glyph: "close"
                        danger: true
                        onClicked: picker.remove(modelData)
                    }
                }
            }
        }
        Btn {
            id: addButton
            objectName: "tagAdd"
            visible: picker.enabled
            variant: "flat"
            implicitHeight: 26
            leftPadding: 8
            rightPadding: 8
            glyph: "plus"
            text: app.texts.addTag || ""
            onClicked: { search.text = ""; popup.open(); search.forceActiveFocus() }
        }
        Label {
            visible: !picker.enabled && picker.chosen.length === 0
            height: 26
            verticalAlignment: Text.AlignVCenter
            leftPadding: 6
            text: "–"
            color: app.palette.muted
        }
    }

    Popup {
        id: popup
        y: picker.height + 4
        width: Math.max(picker.width, 280)
        height: Math.min(320, search.implicitHeight + list.contentHeight + 2 * padding + 6)
        padding: 6
        background: Panel {}
        contentItem: ColumnLayout {
            spacing: 6
            Field {
                id: search
                objectName: "tagSearch"
                Layout.fillWidth: true
                placeholderText: app.texts.searchTags || ""
                onAccepted: if (text.trim() !== "") { picker.add(text.trim()); popup.close() }
            }
            ListView {
                id: list
                objectName: "tagList"
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                ScrollBar.vertical: Scroller {}
                // Kimai's tags not chosen yet, matching the search; then "add …" for a new name.
                model: {
                    const term = search.text.trim().toLowerCase()
                    const rows = picker.options
                        .filter(t => picker.chosen.indexOf(t.name) < 0 && t.name.toLowerCase().indexOf(term) >= 0)
                        .map(t => ({ name: t.name, color: t.color, isNew: false }))
                    const exact = picker.options.some(t => t.name.toLowerCase() === term)
                    if (term !== "" && !exact && picker.chosen.indexOf(search.text.trim()) < 0)
                        rows.push({ name: search.text.trim(), color: app.palette.muted, isNew: true })
                    return rows
                }
                delegate: ItemDelegate {
                    id: row
                    required property var modelData
                    width: ListView.view.width
                    height: 32
                    HoverHandler { cursorShape: Qt.PointingHandCursor }
                    contentItem: RowLayout {
                        spacing: 8
                        Rectangle { implicitWidth: 9; implicitHeight: 9; radius: 5; color: row.modelData.color }
                        Label {
                            Layout.fillWidth: true
                            elide: Text.ElideRight
                            color: app.palette.fg
                            text: row.modelData.isNew ? (app.texts.addNewTag || "").replace("{name}", row.modelData.name)
                                                      : row.modelData.name
                        }
                    }
                    background: Rectangle {
                        radius: 4
                        color: row.hovered ? app.palette.control_hover : "transparent"
                    }
                    onClicked: { picker.add(row.modelData.name); popup.close() }
                }
            }
        }
    }
}
