"""Polish and English texts (F-13). The language is picked in the settings, not only
inherited from the system, and can change without a restart (a new Translator)."""

from __future__ import annotations

import json
import os
from collections.abc import Mapping
from importlib import resources

SUPPORTED = ("pl", "en")
FALLBACK = "en"


class _Blank(dict):
    """A missing placeholder renders empty instead of raising."""

    def __missing__(self, key: str) -> str:
        return ""


def system_locale(env: Mapping[str, str] | None = None) -> str | None:
    env = os.environ if env is None else env
    for variable in ("LC_ALL", "LC_MESSAGES", "LANG"):
        if env.get(variable):
            return env[variable]
    return None


def resolve_language(setting: str, system: str | None) -> str:
    if setting in SUPPORTED:
        return setting
    base = (system or FALLBACK).split(".")[0].split("_")[0].split("-")[0].lower()
    return base if base in SUPPORTED else FALLBACK


def load_messages(language: str) -> dict[str, str]:
    text = resources.files("ws_tracker.core").joinpath("locales", f"{language}.json").read_text("utf-8")
    return json.loads(text)


class Translator:
    def __init__(self, language: str) -> None:
        self.language = language if language in SUPPORTED else FALLBACK
        messages = load_messages(FALLBACK)
        if self.language != FALLBACK:
            # A gap in a translation shows the English text rather than a raw key.
            messages = {**messages, **load_messages(self.language)}
        self._messages = messages

    def __call__(self, key: str, **params: object) -> str:
        text = self._messages.get(key)
        if text is None:
            return key
        return text.format_map(_Blank(params))
