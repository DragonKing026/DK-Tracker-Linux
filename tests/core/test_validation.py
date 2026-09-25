import pytest

from kimai_tray.core.validation import check_description


@pytest.mark.parametrize("text", ["poprawki", "Poprawki.", "  fixes!  ", "bug fixing", "Przegląd", "CALL"])
def test_generic_descriptions_are_rejected(text):
    result = check_description(text, 15)
    assert (result.ok, result.reason) == (False, "generic")
    assert result.word == text.strip()


def test_too_short():
    result = check_description("Formularz", 15)
    assert (result.ok, result.reason, result.word) == (False, "short", None)


def test_empty_is_short_not_generic():
    assert check_description("", 15).reason == "short"
    assert check_description(None, 15).reason == "short"


def test_length_boundary():
    assert check_description("x" * 14, 15).ok is False
    assert check_description("x" * 15, 15).ok is True


@pytest.mark.parametrize("text", ["#412", "PROJ-88", "https://trello.com/c/abc", "fix #9"])
def test_reference_passes_regardless_of_length(text):
    assert check_description(text, 15).ok is True


def test_reference_needs_three_characters():
    assert check_description("#1", 15).ok is False


def test_zero_minimum_turns_check_off():
    assert check_description("poprawki", 0).ok is True
    assert check_description("", 0).ok is True


def test_specific_description_passes():
    assert check_description("n8n: synchronizacja zamówień z ERP", 15).ok is True
