---
noteId: "92f810bf2c074addb88111bf902c06af"
tytul: "Weryfikacja Planu 3 (kod z planu uruchomiony)"
tags: [todo, plan-3, testy, weryfikacja]
utworzono: 2026-09-25 22:58
zaktualizowano: 2026-09-25 22:58
---

# Weryfikacja Planu 3

Plan: [2026-09-25-plan-3-ui.md](../../../../docs/plany/2026-09-25-plan-3-ui.md) · zadanie: [0028](../todo.md)

## Jak sprawdzone

1. Kod napisany metodą TDD w kopii repozytorium (scratchpad), zadanie po zadaniu; po każdym zadaniu pełny `pytest` i `ruff`.
2. Plan wygenerowany z tych plików 1:1, potem **sam kod z planu** wklejony do świeżej kopii `main` (`015bd36`) według kroków planu.
3. Wynik: `334 passed, 1 skipped` (dwa przebiegi pod rząd), `ruff format --check` i `ruff check` bez uwag. Pominięty test: symbol layer-shell przy Qt z pip (opis w planie).
4. Liczby testów po zadaniach: 227 → 237 → 246 → 252 → 259 → 278 → 285 → 301 → 310 → 313 → 328 → 334.

## Na żywo (KDE Plasma 6.7.5, Wayland, Kimai 2.67.0 w Dockerze)

Aplikacja uruchomiona systemowym Pythonem (`PYTHONPATH=src python3 -m kimai_tray`), tryb okna: `layer`.
Test ręczny z użytkownikiem (2026-09-25 22:58): lista projektów rozwija się i okno nie znika, wybór czynności,
start Enterem (ikona zielona `0m`), chowanie po kliknięciu obok, powrót przez ikonę, „Zatrzymaj timer” z menu
z powiadomieniem „Stop: …” — **wszystkie 6 punktów działa**.

Błędy znalezione na żywo i poprawione przed zapisem planu (z testem):

| Błąd | Poprawka | Test |
|---|---|---|
| Okno otwarte przed odpowiedzią portfela nie ładowało projektów | `_on_token` ładuje katalog, gdy okno jest widoczne | `test_window_open_before_the_token_arrives_still_gets_projects` |
| Pasek przewijania w jednolinijkowym opisie | pasek tylko powyżej 96 px | `test_short_description_has_no_scroll_bar` |
| Ostrzeżenie bez tła (reguła QSS `#popup QLabel` silniejsza) | selektory `#popup QLabel#warning` itd. | — (wygląd) |
| Nieudana akcja nie zostawiała śladu w logu (w logu był PATCH 400 bez opisu) | log po angielsku, bez tokenu | `test_failed_actions_are_logged_without_the_token` |
| Podpowiedź o braku tacki znikała po milisekundach | widoczna przez pierwszą sesję, flaga zapisana raz | `test_without_a_tray_the_window_explains_it_for_this_session_only` |
| Segfault przy sprzątaniu `SingleInstance` (lambda na `readyRead`) | sygnał na samo połączenie | `test_second_instance_asks_the_first_to_show_its_window` |

Po teście: token testowy usunięty z portfela, Kimai w Dockerze wyłączony. Zrzuty z testu nie są zapisane — widać na nich pulpit użytkownika.
