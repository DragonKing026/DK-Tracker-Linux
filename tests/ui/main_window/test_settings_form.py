"""Settings as a page of the main window (live test of 0.10.0): the form's logic, without QML."""

from dataclasses import replace

import pytest

from dk_tracker.core.i18n import Translator
from dk_tracker.core.settings import Settings
from dk_tracker.ui.main_window.settings_form import SettingsForm

SAVED = Settings(
    url="https://kimai.test", language="pl", min_description=20, long_timer_hours=6.0, autostart=True
)


def values(**changes):
    base = {
        "url": "https://kimai.test",
        "language": "pl",
        "minDescription": 20,
        "longTimer": 6.0,
        "notifyConnection": True,
        "notifyMenu": True,
        "autostart": True,
        "showTray": True,
    }
    return {**base, **changes}


@pytest.fixture
def form(qapp):
    made = SettingsForm(Translator("pl"))
    made.load(SAVED, has_token=True)
    return made


def test_load_fills_the_fields(form):
    shown = form.form
    assert (shown["url"], shown["language"], shown["minDescription"], shown["longTimer"]) == (
        "https://kimai.test", "pl", 20, 6.0,
    )  # fmt: skip
    assert shown["autostart"] is True and shown["showTray"] is True
    assert shown["tokenPlaceholder"].startswith("Token jest zapisany")


def test_save_keeps_the_stored_token_when_left_empty(form, qtbot):
    with qtbot.waitSignal(form.saveRequested) as signal:
        form.save(values(url=" https://kimai.firma.pl/ ", language="en"), "")
    settings, token = signal.args
    assert (settings.url, settings.language, settings.min_description, token) == (
        "https://kimai.firma.pl", "en", 20, None,
    )  # fmt: skip


def test_save_sends_a_new_token(form, qtbot):
    with qtbot.waitSignal(form.saveRequested) as signal:
        form.save(values(), "  abc123\n")
    assert signal.args[1] == "abc123"


def test_address_is_required(form, qtbot):
    with qtbot.assertNotEmitted(form.saveRequested):
        form.save(values(url=""), "")
    assert (form.form["status"], form.form["okStatus"]) == ("Podaj adres Kimai.", False)


def test_token_is_required_the_first_time(qapp, qtbot):
    made = SettingsForm(Translator("pl"))
    made.load(Settings(), has_token=False)
    with qtbot.assertNotEmitted(made.saveRequested):
        made.save(values(), "")
    assert made.form["status"] == "Podaj token API."


def test_http_warning_while_typing(form):
    form.urlEdited("http://kimai.test")
    assert "http://" in form.form["warning"]
    form.urlEdited("https://kimai.test")
    assert form.form["warning"] == ""


def test_connection_test_uses_the_typed_values(form, qtbot):
    with qtbot.waitSignal(form.testRequested) as signal:
        form.test(" https://kimai.test/ ", " xyz ")
    assert signal.args == ["https://kimai.test", "xyz"]
    assert form.form["status"] == "Sprawdzam…"
    form.show_status("Połączono jako jan.", ok=True)
    assert (form.form["status"], form.form["okStatus"]) == ("Połączono jako jan.", True)


def test_secrets_problem_is_explained(form):
    form.set_secrets_problem("secretsUnavailable")
    assert "Magazyn haseł" in form.form["warning"]


def test_english(form):
    form.retranslate(Translator("en"))
    assert form.form["tokenPlaceholder"].startswith("A token is saved")


def test_tray_icon_can_be_turned_off(form, qtbot):
    with qtbot.waitSignal(form.saveRequested) as signal:
        form.save(values(showTray=False), "")
    assert signal.args[0].show_tray is False
    form.load(replace(SAVED, show_tray=False), has_token=True)
    assert form.form["showTray"] is False


def test_busy_and_a_denied_autostart(form):
    form.set_busy(True)
    assert form.form["busy"] is True
    form.set_autostart(False)
    assert form.form["autostart"] is False
