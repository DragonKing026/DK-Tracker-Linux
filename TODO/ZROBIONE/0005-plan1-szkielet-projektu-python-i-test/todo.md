---
noteId: "ced057af55a84b4f97cf2f7d2e83df13"
tytul: "Plan 1 · Zadanie 1: Szkielet projektu Python i test architektury"
numer: "0005"
status: zrobione
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0002"]
utworzono: 2026-09-25 18:58
zaktualizowano: 2026-09-25 19:01
zamknieto: 2026-09-25 19:01
---

# 0005 — Plan 1 · Zadanie 1: Szkielet projektu Python i test architektury

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 1** z [Planu 1: Rdzeń](../../../docs/plany/2026-09-25-plan-1-rdzen.md)
(sekcja „Task 1: Szkielet projektu Python i test architektury”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-1-rdzen.md](../../../docs/plany/2026-09-25-plan-1-rdzen.md) — kod, testy i komendy każdego
  kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Pliki:
- Create: `pyproject.toml`
- Create: `src/kimai_tray/__init__.py`, `src/kimai_tray/core/__init__.py`
- Create: `tests/__init__.py`, `tests/core/__init__.py`, `tests/test_architektura.py`, `tests/core/test_package.py`
- Modify: `.gitignore`

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający

- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Utwórz `pyproject.toml`
- [x] Step 2: Dopisz do `.gitignore`
- [x] Step 3: Napisz testy (padające)
- [x] Step 4: Utwórz środowisko i uruchom testy — mają paść
- [x] Step 5: Utwórz pakiet
- [x] Step 6: Zainstaluj i uruchom testy — mają przejść
- [x] Step 7: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg: `3 passed in 0.01s`

## Dziennik

### 2026-09-25

- Utworzono zadanie z Planu 1.
- Start wykonania (Native, gałąź feat/plan-1-rdzen).
- Zamknięte: testy zielone, commity w gałęzi feat/plan-1-rdzen.

## Wynik

Powstał pakiet `kimai_tray` (0668c20): [pyproject.toml](../../../pyproject.toml),
[src/kimai_tray/](../../../src/kimai_tray/), [tests/test_architektura.py](../../../tests/test_architektura.py).
Środowisko `.venv` z pytest, ruff, httpx. Rulings: ruff ograniczony do kodu produktu (extend-exclude .claude, TODO,
docs); poprawka końcowego / w linki.py.
