import pytest

from kimai_tray.core.i18n import Translator
from kimai_tray.core.settings import Settings
from kimai_tray.ui.settings_dialog import SettingsDialog

SAVED = Settings(
    url="https://kimai.test", language="pl", min_description=20, long_timer_hours=6.0, autostart=True
)


@pytest.fixture
def dialog(qtbot):
    widget = SettingsDialog(Translator("pl"))
    qtbot.addWidget(widget)
    widget.load(SAVED, has_token=True)
    return widget


def test_load_fills_the_fields(dialog):
    assert dialog.url.text() == "https://kimai.test"
    assert dialog.language.currentData() == "pl"
    assert dialog.min_description.value() == 20
    assert dialog.long_timer.value() == 6.0
    assert dialog.autostart.isChecked()
    assert dialog.token.text() == ""
    assert dialog.token.placeholderText().startswith("Token jest zapisany")


def test_save_keeps_the_stored_token_when_left_empty(dialog, qtbot):
    dialog.url.setText(" https://kimai.firma.pl/ ")
    dialog.language.setCurrentIndex(dialog.language.findData("en"))
    with qtbot.waitSignal(dialog.saveRequested) as signal:
        dialog.save_button.click()
    settings, token = signal.args
    assert settings.url == "https://kimai.firma.pl"
    assert settings.language == "en"
    assert settings.min_description == 20
    assert token is None


def test_save_sends_a_new_token(dialog, qtbot):
    dialog.token.setText("  abc123\n")
    with qtbot.waitSignal(dialog.saveRequested) as signal:
        dialog.save_button.click()
    assert signal.args[1] == "abc123"


def test_address_is_required(dialog, qtbot):
    dialog.url.setText("")
    with qtbot.assertNotEmitted(dialog.saveRequested):
        dialog.save_button.click()
    assert dialog.status.text() == "Podaj adres Kimai."


def test_token_is_required_the_first_time(qtbot):
    dialog = SettingsDialog(Translator("pl"))
    qtbot.addWidget(dialog)
    dialog.load(Settings(), has_token=False)
    dialog.url.setText("https://kimai.test")
    with qtbot.assertNotEmitted(dialog.saveRequested):
        dialog.save_button.click()
    assert dialog.status.text() == "Podaj token API."


def test_http_warning_while_typing(dialog):
    dialog.url.setText("http://kimai.test")
    assert "http://" in dialog.warning.text() and not dialog.warning.isHidden()
    dialog.url.setText("https://kimai.test")
    assert dialog.warning.isHidden()


def test_connection_test_uses_the_typed_values(dialog, qtbot):
    dialog.token.setText("xyz")
    with qtbot.waitSignal(dialog.testRequested) as signal:
        dialog.test_button.click()
    assert signal.args == ["https://kimai.test", "xyz"]
    assert dialog.status.text() == "Sprawdzam…"
    dialog.show_status("Połączono jako jan.", ok=True)
    assert dialog.status.property("ok") == "true"


def test_secrets_problem_is_explained(dialog):
    dialog.set_secrets_problem("secretsUnavailable")
    assert "Magazyn haseł" in dialog.warning.text()


def test_english(dialog):
    dialog.retranslate(Translator("en"))
    assert dialog.windowTitle() == "Kimai Tray settings"
    assert dialog.save_button.text() == "Save"


def test_wrapped_hints_get_the_height_they_need(dialog, qtbot):
    dialog.resize(480, 120)  # too small: the window must not squeeze the hints
    dialog.show()
    qtbot.waitExposed(dialog)
    for label in (dialog.token_hint, dialog.min_hint, dialog.long_hint):
        assert label.height() >= label.heightForWidth(label.width()), label.text()
        assert label.height() >= label.sizeHint().height(), label.text()
        assert label.width() >= label.sizeHint().width(), label.text()
