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


def test_the_theme_is_chosen_in_the_settings(form, qtbot):
    assert form.form["theme"] == "auto"
    assert [option["code"] for option in form.form["themes"]] == ["auto", "light", "dark"]
    with qtbot.waitSignal(form.saveRequested) as signal:
        form.save(values(theme="dark"), "")
    assert signal.args[0].theme == "dark"


def test_a_stored_token_is_shown_as_a_mask_never_as_itself(form):
    """Live test: the token field should show that a token is there. Only a fixed mask — the token
    never comes back from the wallet into the window (spec 1.0, section 8)."""
    assert form.form["hasToken"] is True
    assert "token" not in {key.lower() for key in form.form} - {"hastoken", "tokenplaceholder"}


def test_the_daily_norm_is_shown_and_saved(form, qtbot):
    form.load(replace(SAVED, daily_norm_hours=7.5), has_token=True)
    assert form.form["dailyNorm"] == 7.5
    with qtbot.waitSignal(form.saveRequested) as sent:
        form.save(values(dailyNorm=0.0), "")
    assert sent.args[0].daily_norm_hours == 0.0


def test_the_about_section_has_the_version_and_the_project_page(form):
    """0.10.4: the user asked for "about" and the version in the settings."""
    from dk_tracker import __version__

    assert form.form["version"] == __version__
    assert form.form["homepage"] == "https://github.com/DragonKing026/DK-Tracker-Linux"


# -- the holiday country (task 0088) ---------------------------------------------------------


def test_the_country_list_starts_with_none_then_goes_by_name(form):
    countries = form.form["holidayCountries"]
    assert countries[0] == {"code": "", "label": "brak"}
    labels = [country["label"] for country in countries[1:]]
    assert len(labels) == 204 and labels == sorted(labels, key=str.casefold)
    assert {"code": "PL", "label": "Poland"} in countries


def test_the_country_is_saved_with_the_rest(form, qtbot):
    assert form.form["holidayCountry"] == ""
    with qtbot.waitSignal(form.saveRequested) as signal:
        form.save(values(holidayCountry="pl"), "")
    assert signal.args[0].holiday_country == "PL"
    with qtbot.waitSignal(form.saveRequested) as signal:
        form.save(values(holidayCountry="ZZ"), "")  # unknown: none
    assert signal.args[0].holiday_country == ""


def test_a_save_without_the_field_keeps_the_saved_country(qtbot):
    made = SettingsForm(Translator("pl"))
    made.load(replace(SAVED, holiday_country="DE"), has_token=True)
    with qtbot.waitSignal(made.saveRequested) as signal:
        made.save(values(), "")
    assert signal.args[0].holiday_country == "DE"


def test_the_sync_button_and_the_status(form, qtbot):
    with qtbot.waitSignal(form.syncHolidaysRequested):
        form.syncHolidays()
    form.show_holiday_status("Synchronizacja…", ok=True, busy=True)
    assert (form.form["holidayStatus"], form.form["holidayOk"], form.form["holidayBusy"]) == (
        "Synchronizacja…", True, True,
    )  # fmt: skip
    form.load(SAVED, has_token=True)  # loading the fields does not wipe the fetch's state
    assert form.form["holidayBusy"] is True
