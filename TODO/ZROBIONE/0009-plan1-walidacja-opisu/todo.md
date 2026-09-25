---
noteId: "d1d1d4be207948e492553794c05d765a"
tytul: "Plan 1 · Zadanie 5: Walidacja opisu (`validation.py`, F-11)"
numer: "0009"
status: zrobione
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0008"]
utworzono: 2026-09-25 18:58
zaktualizowano: 2026-09-25 19:02
zamknieto: 2026-09-25 19:02
---

# 0009 — Plan 1 · Zadanie 5: Walidacja opisu (`validation.py`, F-11)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 5** z [Planu 1: Rdzeń](../../../docs/plany/2026-09-25-plan-1-rdzen.md)
(sekcja „Task 5: Walidacja opisu (`validation.py`, F-11)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-1-rdzen.md](../../../docs/plany/2026-09-25-plan-1-rdzen.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Pliki:
- Create: `src/kimai_tray/core/validation.py`
- Test: `tests/core/test_validation.py`

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] `.venv/bin/pytest tests/core/test_validation.py -v` → wszystkie PASS.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające)
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Zaimplementuj `src/kimai_tray/core/validation.py`
- [x] Step 4: Uruchom — mają przejść
- [x] Step 5: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg: `57 passed in 0.05s`

## Dziennik

### 2026-09-25
- Utworzono zadanie z Planu 1.
- Start wykonania.
- Zamknięte: testy zielone, commity w gałęzi feat/plan-1-rdzen.

## Wynik

[src/kimai_tray/core/validation.py](../../../src/kimai_tray/core/validation.py): lista ogólników PL/EN 1:1 z wtyczki, normalizacja, odwołania (#412, PROJ-88, linki). Testy: [tests/core/test_validation.py](../../../tests/core/test_validation.py) — 16 zielonych. Bez odchyleń.
