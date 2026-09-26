---
noteId: "25016b5e44f445f1af8c316a85eddd34"
tytul: "Plan 1 · Zadanie 9: Tłumaczenia PL/EN (`i18n.py`, `locales/`, F-13)"
numer: "0013"
status: zrobione
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0012"]
utworzono: 2026-09-25 18:58
zaktualizowano: 2026-09-25 19:03
zamknieto: 2026-09-25 19:03
---

# 0013 — Plan 1 · Zadanie 9: Tłumaczenia PL/EN (`i18n.py`, `locales/`, F-13)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 9** z [Planu 1: Rdzeń](../../../docs/plany/2026-09-25-plan-1-rdzen.md)
(sekcja „Task 9: Tłumaczenia PL/EN (`i18n.py`, `locales/`, F-13)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-1-rdzen.md](../../../docs/plany/2026-09-25-plan-1-rdzen.md) — kod, testy i komendy każdego
  kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Pliki:
- Create: `src/kimai_tray/core/i18n.py`, `src/kimai_tray/core/locales/en.json`, `src/kimai_tray/core/locales/pl.json`
- Test: `tests/core/test_i18n.py`

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] `.venv/bin/pytest tests/core/test_i18n.py -v` → wszystkie PASS. Jeśli `test_every_key_used_in_code_exists` pokaże
      brakujący klucz z wcześniejszych modułów — dopisz go do obu plików JSON.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające)
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Utwórz `src/kimai_tray/core/locales/en.json`
- [x] Step 4: Utwórz `src/kimai_tray/core/locales/pl.json`
- [x] Step 5: Zaimplementuj `src/kimai_tray/core/i18n.py`
- [x] Step 6: Uruchom — mają przejść
- [x] Step 7: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg: `96 passed in 0.08s`

## Dziennik

### 2026-09-25

- Utworzono zadanie z Planu 1.
- Start wykonania.
- Zamknięte: testy zielone, commity w gałęzi feat/plan-1-rdzen.

## Wynik

[src/kimai_tray/core/i18n.py](../../../src/ws_tracker/core/i18n.py) i
[locales/](../../../src/ws_tracker/core/locales/)
(PL/EN, klucze z wtyczki + nowe: strefa czasowa, TLS, powiadomienia). Test pilnuje identycznych kluczy i placeholderów
oraz istnienia każdego klucza użytego w kodzie. 12 testów zielonych. Bez odchyleń.
