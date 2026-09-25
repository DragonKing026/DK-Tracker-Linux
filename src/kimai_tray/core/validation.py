"""Description quality check (F-11), ported from WS Tracker's lib/validate.js.

Kimai treats the description as optional, but clients read these reports, so a timer
is not started on an empty, too short or generic one ("poprawki", "call", "n8n").
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

GENERIC = frozenset(
    {
        # Polish
        "poprawki",
        "poprawka",
        "poprawianie",
        "praca",
        "prace",
        "prace biurowe",
        "robota",
        "zmiany",
        "zmiana",
        "testy",
        "test",
        "analiza",
        "spotkanie",
        "narada",
        "narady",
        "rozmowa",
        "rozmowy",
        "konfiguracja",
        "aktualizacja",
        "sprawdzenie",
        "sprawdzanie",
        "przeglad",
        "przegladanie",
        "dokonczenie",
        "kontynuacja",
        "papiery",
        "inne",
        "rozne",
        "zadania",
        "zadanie",
        "pomoc",
        "administracja",
        "organizacja",
        "planowanie",
        "programowanie",
        "kodowanie",
        "wdrozenie",
        "przerwa",
        "maile",
        "mail",
        "poczta",
        # English
        "work",
        "working",
        "fix",
        "fixes",
        "fixing",
        "bug",
        "bugs",
        "bugfix",
        "bug fixing",
        "debug",
        "debugging",
        "meeting",
        "call",
        "daily",
        "standup",
        "daily standup",
        "setup",
        "update",
        "updates",
        "testing",
        "research",
        "review",
        "code review",
        "deploy",
        "deployment",
        "refactor",
        "refactoring",
        "development",
        "dev",
        "misc",
        "other",
        "todo",
        "task",
        "tasks",
        "support",
        "admin",
        "demo",
        "changes",
        "stuff",
        "break",
        "lunch",
        "dinner break",
        "discussion",
        "migration",
        "maintenance",
    }
)

_COMBINING = re.compile(r"[̀-ͯ]")
_EDGE_PUNCTUATION = re.compile(r"^[\s.,;:!-]+|[\s.,;:!-]+$")
_REFERENCE = re.compile(r"https?://|#\d+|\b[A-Z]{2,}-\d+\b")


@dataclass(frozen=True)
class DescriptionCheck:
    ok: bool
    reason: str | None = None  # "short" | "generic"
    word: str | None = None


def _normalize(text: str) -> str:
    """ "Poprawki." and "poprawki" compare equal; diacritics and edge punctuation go."""
    text = _COMBINING.sub("", unicodedata.normalize("NFD", text.lower()))
    text = re.sub(r"\s+", " ", text).strip()
    return _EDGE_PUNCTUATION.sub("", text)


def check_description(raw: str | None, min_length: int) -> DescriptionCheck:
    text = (raw or "").strip()
    if min_length <= 0:
        return DescriptionCheck(ok=True)
    # A link or an issue reference is specific enough on its own, however short.
    if _REFERENCE.search(text) and len(text) >= 3:
        return DescriptionCheck(ok=True)
    if _normalize(text) in GENERIC:
        return DescriptionCheck(ok=False, reason="generic", word=text)
    if len(text) < min_length:
        return DescriptionCheck(ok=False, reason="short")
    return DescriptionCheck(ok=True)
