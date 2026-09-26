// Settings as a page of the main window (live test of 0.10.0): the Kimai address and token,
// language, description rule, the long-timer reminder, notifications, autostart and the tray.
// The logic is in Python (`app.settingsForm`); the fields take its values when it loads them.
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ScrollView {
    id: page
    objectName: "settingsView"
    readonly property var form: app.settingsForm.form
    contentWidth: availableWidth
    clip: true

    function fill() {
        url.text = form.url
        token.text = ""
        language.currentIndex = Math.max(0, language.indexOfValue(form.language))
        minDescription.value = form.minDescription
        longTimer.value = Math.round(form.longTimer * 10)
        notifyConnection.checked = form.notifyConnection
        notifyMenu.checked = form.notifyMenu
        autostart.checked = form.autostart
        showTray.checked = form.showTray
    }
    function values() {
        return {
            url: url.text, language: language.currentValue, minDescription: minDescription.value,
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
        width: Math.min(page.availableWidth - 48, 620)
        x: 24
        spacing: 6

        Label {
            Layout.topMargin: 20
            text: app.texts.optTitle || ""
            font.pixelSize: 20
            font.bold: true
            color: app.palette.fg || "#eceef2"
        }
        Label {
            objectName: "settingsNotConfigured"
            visible: !app.view.configured
            Layout.fillWidth: true
            wrapMode: Text.Wrap
            text: app.texts.notConfigured || ""
            color: app.palette.muted || "#9aa0ac"
        }

        component Caption: Label {
            Layout.topMargin: 12
            font.bold: true
            color: app.palette.fg || "#eceef2"
        }
        component Hint: Label {
            Layout.fillWidth: true
            wrapMode: Text.Wrap
            font.pixelSize: 12
            color: app.palette.muted || "#9aa0ac"
        }

        Caption { text: app.texts.optUrl || "" }
        TextField {
            id: url
            objectName: "settingsUrl"
            Layout.fillWidth: true
            placeholderText: app.texts.optUrlHint || ""
            onTextEdited: app.settingsForm.urlEdited(text)
        }

        Caption { text: app.texts.optToken || "" }
        TextField {
            id: token
            objectName: "settingsToken"
            Layout.fillWidth: true
            echoMode: TextInput.Password
            placeholderText: page.form.tokenPlaceholder
        }
        Hint { text: app.texts.optTokenHint || "" }

        Caption { text: app.texts.optLang || "" }
        ComboBox {
            id: language
            objectName: "settingsLanguage"
            Layout.preferredWidth: 260
            model: page.form.languages
            textRole: "label"
            valueRole: "code"
        }

        Caption { text: app.texts.optMinDesc || "" }
        SpinBox {
            id: minDescription
            objectName: "settingsMinDescription"
            from: 0
            to: 200
            editable: true
        }
        Hint { text: app.texts.optMinDescHint || "" }

        Caption { text: app.texts.optLongTimer || "" }
        SpinBox {  // tenths of an hour: 0.0–24.0 in steps of 0.5
            id: longTimer
            objectName: "settingsLongTimer"
            from: 0
            to: 240
            stepSize: 5
            editable: true
            textFromValue: function (value, locale) { return Number(value / 10).toLocaleString(locale, "f", 1) }
            valueFromText: function (text, locale) { return Math.round(Number.fromLocaleString(locale, text) * 10) }
        }
        Hint { text: app.texts.optLongTimerHint || "" }

        CheckBox { id: notifyConnection; objectName: "settingsNotifyConnection"; Layout.topMargin: 12; text: app.texts.optNotifyConnection || "" }
        CheckBox { id: notifyMenu; objectName: "settingsNotifyMenu"; text: app.texts.optNotifyMenu || "" }
        CheckBox { id: autostart; objectName: "settingsAutostart"; text: app.texts.optAutostart || "" }
        CheckBox { id: showTray; objectName: "settingsShowTray"; text: app.texts.optShowTray || "" }

        Label {
            objectName: "settingsWarning"
            visible: page.form.warning !== ""
            Layout.fillWidth: true
            Layout.topMargin: 8
            wrapMode: Text.Wrap
            text: page.form.warning
            color: app.palette.err_fg || "#ff9d9d"
        }
        Label {
            objectName: "settingsStatus"
            visible: page.form.status !== ""
            Layout.fillWidth: true
            wrapMode: Text.Wrap
            text: page.form.status
            color: page.form.okStatus ? (app.palette.ok_fg || "#6ee7a0") : (app.palette.err_fg || "#ff9d9d")
        }

        RowLayout {
            Layout.topMargin: 12
            Layout.bottomMargin: 24
            spacing: 8
            Button {
                objectName: "settingsTest"
                text: app.texts.optTest || ""
                enabled: !page.form.busy
                onClicked: app.settingsForm.test(url.text, token.text)
            }
            Item { Layout.fillWidth: true }
            Button {
                objectName: "settingsSave"
                text: app.texts.optSave || ""
                enabled: !page.form.busy
                highlighted: true
                onClicked: app.settingsForm.save(page.values(), token.text)
            }
        }
    }
}
