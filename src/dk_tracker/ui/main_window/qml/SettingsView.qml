// Settings as a page of the main window: the Kimai address and token, language, description rule,
// the long-timer reminder, notifications, autostart and the tray. The same form layout as the edit
// window. The logic is in Python (`app.settingsForm`); the fields take its values when it loads them.
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ScrollView {
    id: page
    objectName: "settingsView"
    readonly property var form: app.settingsForm.form
    readonly property int labelWidth: 230  // the settings' labels are longer than the edit window's
    contentWidth: availableWidth
    clip: true
    background: Rectangle { color: app.palette.bg }
    ScrollBar.vertical: Scroller {
        parent: page
        x: page.width - width
        height: page.availableHeight
    }

    function fill() {
        url.text = form.url
        token.text = ""
        language.currentIndex = Math.max(0, language.indexOfValue(form.language))
        theme.currentIndex = Math.max(0, theme.indexOfValue(form.theme))
        minDescription.value = form.minDescription
        longTimer.value = Math.round(form.longTimer * 10)
        notifyConnection.checked = form.notifyConnection
        notifyMenu.checked = form.notifyMenu
        autostart.checked = form.autostart
        showTray.checked = form.showTray
    }
    function values() {
        return {
            url: url.text, language: language.currentValue, theme: theme.currentValue, minDescription: minDescription.value,
            longTimer: longTimer.value / 10, notifyConnection: notifyConnection.checked,
            notifyMenu: notifyMenu.checked, autostart: autostart.checked, showTray: showTray.checked
        }
    }
    Component.onCompleted: fill()
    Connections {
        target: app.settingsForm
        function onLoaded() { page.fill() }
    }

    ColumnLayout {
        width: Math.min(page.availableWidth - 48, 680)
        x: 24
        spacing: 12

        Label {
            Layout.topMargin: 20
            text: app.texts.optTitle || ""
            font.pixelSize: 20
            font.weight: Font.Bold
            color: app.palette.fg
        }
        Label {
            objectName: "settingsNotConfigured"
            visible: !app.view.configured
            Layout.fillWidth: true
            wrapMode: Text.Wrap
            text: app.texts.notConfigured || ""
            color: app.palette.muted
        }

        component Hint: Label {
            Layout.fillWidth: true
            Layout.leftMargin: page.labelWidth + 12  // under the field, past the label column
            Layout.topMargin: -6
            wrapMode: Text.Wrap
            font.pixelSize: 12
            color: app.palette.muted
        }

        FormRow {
            labelWidth: page.labelWidth
            label: app.texts.optUrl || ""
            Field {
                id: url
                objectName: "settingsUrl"
                Layout.fillWidth: true
                placeholderText: app.texts.optUrlHint || ""
                onTextEdited: app.settingsForm.urlEdited(text)
            }
        }
        FormRow {
            labelWidth: page.labelWidth
            label: app.texts.optToken || ""
            Field {
                id: token
                objectName: "settingsToken"
                Layout.fillWidth: true
                echoMode: TextInput.Password
                placeholderText: ""  // the hint under the field says where to get one
                // A stored token shows as a fixed mask — never the token, never its length (the
                // token does not come back from the wallet). Typing a new one replaces it.
                Row {
                    objectName: "settingsTokenMask"
                    visible: page.form.hasToken && token.text === "" && !token.activeFocus
                    anchors.left: parent.left
                    anchors.leftMargin: token.leftPadding
                    anchors.verticalCenter: parent.verticalCenter
                    spacing: 10
                    Label { text: "••••••••••••••••"; color: app.palette.fg }
                    Label { text: app.texts.optTokenStored || ""; color: app.palette.muted; font.pixelSize: 12 }
                }
            }
        }
        Hint { text: app.texts.optTokenHint || "" }
        FormRow {
            labelWidth: page.labelWidth
            label: app.texts.optLang || ""
            Combo {
                id: language
                objectName: "settingsLanguage"
                Layout.preferredWidth: 240
                model: page.form.languages
                textRole: "label"
                valueRole: "code"
            }
            Item { Layout.fillWidth: true }
        }
        FormRow {
            labelWidth: page.labelWidth
            label: app.texts.optTheme || ""
            Combo {
                id: theme
                objectName: "settingsTheme"
                Layout.preferredWidth: 240
                model: page.form.themes
                textRole: "label"
                valueRole: "code"
            }
            Item { Layout.fillWidth: true }
        }
        FormRow {
            labelWidth: page.labelWidth
            label: app.texts.optMinDesc || ""
            Spin {
                id: minDescription
                objectName: "settingsMinDescription"
                from: 0
                to: 200
            }
            Item { Layout.fillWidth: true }
        }
        Hint { text: app.texts.optMinDescHint || "" }
        FormRow {
            labelWidth: page.labelWidth
            label: app.texts.optLongTimer || ""
            Spin {  // tenths of an hour: 0.0–24.0 in steps of 0.5
                id: longTimer
                objectName: "settingsLongTimer"
                from: 0
                to: 240
                stepSize: 5
                textFromValue: function (value, locale) { return Number(value / 10).toLocaleString(locale, "f", 1) }
                valueFromText: function (text, locale) { return Math.round(Number.fromLocaleString(locale, text) * 10) }
            }
            Item { Layout.fillWidth: true }
        }
        Hint { text: app.texts.optLongTimerHint || "" }

        ColumnLayout {
            Layout.leftMargin: page.labelWidth + 12
            Layout.topMargin: 4
            spacing: 6
            Check { id: notifyConnection; objectName: "settingsNotifyConnection"; text: app.texts.optNotifyConnection || "" }
            Check { id: notifyMenu; objectName: "settingsNotifyMenu"; text: app.texts.optNotifyMenu || "" }
            Check { id: autostart; objectName: "settingsAutostart"; text: app.texts.optAutostart || "" }
            Check { id: showTray; objectName: "settingsShowTray"; text: app.texts.optShowTray || "" }
        }

        Label {
            objectName: "settingsWarning"
            visible: page.form.warning !== ""
            Layout.fillWidth: true
            wrapMode: Text.Wrap
            text: page.form.warning
            color: app.palette.danger
        }
        Label {
            objectName: "settingsStatus"
            visible: page.form.status !== ""
            Layout.fillWidth: true
            wrapMode: Text.Wrap
            text: page.form.status
            color: page.form.okStatus ? app.palette.start : app.palette.danger
        }

        Rectangle { Layout.fillWidth: true; Layout.topMargin: 4; implicitHeight: 1; color: app.palette.divider }

        RowLayout {
            Layout.bottomMargin: 24
            spacing: 8
            Btn {
                objectName: "settingsTest"
                text: app.texts.optTest || ""
                enabled: !page.form.busy
                onClicked: app.settingsForm.test(url.text, token.text)
            }
            Item { Layout.fillWidth: true }
            Btn {
                objectName: "settingsSave"
                variant: "primary"
                text: app.texts.optSave || ""
                enabled: !page.form.busy
                onClicked: app.settingsForm.save(page.values(), token.text)
            }
        }
    }
}
