---
noteId: "7cb3ce12d7bb46f18e16d51aa4764890"
tytul: "Plan 1 · Zadanie 6: Grupowanie list i reguły billable (`grouping.py`, `billable.py`, F-06/F-08/F-09)"
numer: "0010"
status: zrobione
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0009"]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
zamknieto: 2026-09-25
---

# 0010 — Plan 1 · Zadanie 6: Grupowanie list i reguły billable (`grouping.py`, `billable.py`, F-06/F-08/F-09)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 6** z [Planu 1: Rdzeń](../../../docs/plany/2026-09-25-plan-1-rdzen.md)
(sekcja „Task 6: Grupowanie list i reguły billable (`grouping.py`, `billable.py`, F-06/F-08/F-09)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-1-rdzen.md](../../../docs/plany/2026-09-25-plan-1-rdzen.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Pliki:
- Create: `src/kimai_tray/core/grouping.py`, `src/kimai_tray/core/billable.py`
- Test: `tests/core/test_grouping.py`, `tests/core/test_billable.py`

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] `.venv/bin/pytest tests/core/test_grouping.py tests/core/test_billable.py -v` → 7 PASS.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające)
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Zaimplementuj `src/kimai_tray/core/grouping.py`
- [x] Step 4: Zaimplementuj `src/kimai_tray/core/billable.py`
- [x] Step 5: Uruchom — mają przejść
- [x] Step 6: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg: `64 passed in 0.06s`

## Dziennik

### 2026-09-25
- Utworzono zadanie z Planu 1.
- Start wykonania.
- Zamknięte: testy zielone, commity w gałęzi feat/plan-1-rdzen.

## Wynik

[grouping.py](../../../src/kimai_tray/core/grouping.py) (wpisy po dniach w strefie konta, projekty po klientach, sortowanie bez znaczenia wielkości liter i polskich znaków) i [billable.py](../../../src/kimai_tray/core/billable.py) (domyślne billable jak w Kimai, rozpoznanie 400 „extra fields”). Testy: 7 zielonych. Bez odchyleń.
