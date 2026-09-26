---
noteId: "c4042ac8ba424af58ad7fb0013d79cfb"
tytul: "Plan 1 · Zadanie 8: Ustawienia i pamięć aplikacji (`settings.py`)"
numer: "0012"
status: zrobione
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0011"]
utworzono: 2026-09-25 18:58
zaktualizowano: 2026-09-25 19:02
zamknieto: 2026-09-25 19:02
---

# 0012 — Plan 1 · Zadanie 8: Ustawienia i pamięć aplikacji (`settings.py`)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 8** z [Planu 1: Rdzeń](../../../docs/plany/2026-09-25-plan-1-rdzen.md)
(sekcja „Task 8: Ustawienia i pamięć aplikacji (`settings.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-1-rdzen.md](../../../docs/plany/2026-09-25-plan-1-rdzen.md) — kod, testy i komendy każdego
  kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Pliki:
- Create: `src/kimai_tray/core/settings.py`
- Test: `tests/core/test_settings.py`

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] `.venv/bin/pytest tests/core/test_settings.py -v` → 8 PASS.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające)
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Zaimplementuj `src/kimai_tray/core/settings.py`
- [x] Step 4: Uruchom — mają przejść
- [x] Step 5: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg: `84 passed in 0.08s`

## Dziennik

### 2026-09-25

- Utworzono zadanie z Planu 1.
- Start wykonania.
- Zamknięte: testy zielone, commity w gałęzi feat/plan-1-rdzen.

## Wynik

[src/kimai_tray/core/settings.py](../../../src/ws_tracker/core/settings.py): `Settings` (normalizacja, ostrzeżenie
http://), `Memory`, ścieżki XDG, zapis atomowy, odporność na uszkodzony plik; token nigdy w pliku. Testy:
[tests/core/test_settings.py](../../../tests/core/test_settings.py) — 8 zielonych. Bez odchyleń.
