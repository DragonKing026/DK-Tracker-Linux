import re
from pathlib import Path
from string import Formatter

import pytest

from ws_tracker_tray.core.i18n import SUPPORTED, Translator, load_messages, resolve_language, system_locale

SRC = Path(__file__).resolve().parents[2] / "src" / "ws_tracker_tray"
# String literals shaped like message keys; every one used in code must exist in the locales.
KEY_LITERAL = re.compile(
    r"\"((?:err|warn|notif|action|opt|day|saved|billable|menu|tooltip|win|hint|secrets|status)[A-Z][A-Za-z]*)\""
)


def placeholders(text):
    return {name for _, name, _, _ in Formatter().parse(text) if name}


def test_locales_have_identical_keys_and_placeholders():
    pl, en = load_messages("pl"), load_messages("en")
    assert set(pl) == set(en)
    for key in en:
        assert placeholders(pl[key]) == placeholders(en[key]), key


def test_every_key_used_in_code_exists():
    known = set(load_messages("en"))
    used = {
        key for path in SRC.rglob("*.py") for key in KEY_LITERAL.findall(path.read_text(encoding="utf-8"))
    }
    assert used - known == set()


@pytest.mark.parametrize(
    ("setting", "system", "expected"),
    [
        ("pl", None, "pl"),
        ("en", "pl_PL.UTF-8", "en"),
        ("auto", "pl_PL.UTF-8", "pl"),
        ("auto", "de_DE.UTF-8", "en"),
        ("auto", None, "en"),
        ("xx", "pl", "pl"),
    ],
)
def test_resolve_language(setting, system, expected):
    assert resolve_language(setting, system) == expected


def test_system_locale_priority():
    assert system_locale({"LANG": "en_US.UTF-8", "LC_MESSAGES": "pl_PL.UTF-8"}) == "pl_PL.UTF-8"
    assert system_locale({"LC_ALL": "de_DE", "LANG": "pl_PL"}) == "de_DE"
    assert system_locale({}) is None


def test_translation_with_placeholders():
    t = Translator("pl")
    assert t.language == "pl"
    assert t("errDescShort", chars=15) == "Opis jest za krótki — napisz co najmniej 15 znaków."
    assert Translator("en")("todayTotal", time="1:05") == "Today 1:05"


def test_missing_key_and_missing_param():
    t = Translator("en")
    assert t("noSuchKey") == "noSuchKey"
    assert t("todayTotal") == "Today "


def test_supported():
    assert SUPPORTED == ("pl", "en")
