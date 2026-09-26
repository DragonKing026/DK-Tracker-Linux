---
noteId: "4dec5afaac8647d1b61c56595efd9848"
tytul: "Plan 1 · Zadanie 4: Czas i strefy (`timefmt.py`)"
numer: "0008"
status: zrobione
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0007"]
utworzono: 2026-09-25 19:01
zaktualizowano: 2026-09-25 19:02
zamknieto: 2026-09-25 19:02
---

# 0008 — Plan 1 · Zadanie 4: Czas i strefy (`timefmt.py`)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 4** z [Planu 1: Rdzeń](../../../docs/plany/2026-09-25-plan-1-rdzen.md)
(sekcja „Task 4: Czas i strefy (`timefmt.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-1-rdzen.md](../../../docs/plany/2026-09-25-plan-1-rdzen.md) — kod, testy i komendy każdego
  kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Pliki:
- Create: `src/kimai_tray/core/timefmt.py`
- Test: `tests/core/test_timefmt.py`

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] `.venv/bin/pytest tests/core/test_timefmt.py -v` → wszystkie PASS (19 przypadków z parametryzacją).
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające)
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Zaimplementuj `src/kimai_tray/core/timefmt.py`
- [x] Step 4: Uruchom — mają przejść
- [x] Step 5: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg: `41 passed in 0.05s`

## Dziennik

### 2026-09-25

- Utworzono zadanie z Planu 1.
- Start wykonania.
- Zamknięte: testy zielone, commity w gałęzi feat/plan-1-rdzen.

## Wynik

[src/kimai_tray/core/timefmt.py](../../../src/dk_tracker/core/timefmt.py): `zone` (z bezpiecznym brakiem strefy),
stemple Kimai w strefie konta, formaty `h:mm`/`47m`, tydzień od poniedziałku (także przy zmianie czasu), walidacja
HH:MM. Testy: [tests/core/test_timefmt.py](../../../tests/core/test_timefmt.py) — 18 zielonych. Ruling: plan podawał 19
przypadków — błąd liczenia.
