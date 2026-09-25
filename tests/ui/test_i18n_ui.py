from kimai_tray.core.i18n import Translator, load_messages

UI_KEYS = {
    "menuStop",
    "menuResumeLast",
    "menuOpen",
    "menuOpenKimai",
    "menuQuit",
    "tooltipIdle",
    "tooltipMoreRunning",
    "winClose",
    "hintNoTray",
    "secretsUnavailable",
    "secretsLocked",
    "optLongTimer",
    "optLongTimerHint",
    "optNotifyConnection",
    "optNotifyMenu",
    "optAutostart",
    "optAutostartReason",
    "optAutostartDenied",
    "optUrlRequired",
    "optTokenRequired",
    "optTesting",
    "optTokenKeep",
    "statusRunning",
    "weekdaysShort",
    "monthsShort",
    "dayOther",
}


def test_ui_texts_exist_in_both_languages():
    for language in ("pl", "en"):
        assert UI_KEYS <= set(load_messages(language)), language


def test_weekday_and_month_lists_have_the_right_length():
    for language in ("pl", "en"):
        t = Translator(language)
        assert len(t("weekdaysShort").split(",")) == 7
        assert len(t("monthsShort").split(",")) == 12
