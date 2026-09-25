---
noteId: "ca9fa6d8ee7b40dcb9d4047a17fddb99"
tytul: "Plan 2 · Zadanie 1: Szyna D-Bus (`desktop/bus.py`)"
numer: "0022"
status: zrobione
priorytet: p1
tags: [todo, plan-2, desktop]
zalezy_od: []
utworzono: 2026-09-25 20:59
zaktualizowano: 2026-09-25 21:00
zamknieto: 2026-09-25 21:00
---

# 0022 — Plan 2 · Zadanie 1: Szyna D-Bus (`desktop/bus.py`)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 1** z [Planu 2: Integracje desktopowe](../../../docs/plany/2026-09-25-plan-2-desktop.md)
(sekcja „Task 1: Szyna D-Bus (`desktop/bus.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-2-desktop.md](../../../docs/plany/2026-09-25-plan-2-desktop.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Rozpoznanie API: [rozpoznanie.md](../../W-TRAKCIE/0021-plan2-rozpoznanie-api-desktop/notatki/rozpoznanie.md).
- Pliki:
- Modify: `pyproject.toml` (zależność `jeepney`)
- Create: `src/kimai_tray/desktop/__init__.py`, `src/kimai_tray/desktop/bus.py`
- Create: `tests/desktop/__init__.py`, `tests/desktop/fakes.py`, `tests/desktop/test_bus.py`

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] Wynik planu: 5 PASS w `test_bus.py`.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Dodaj zależność
- [x] Step 2: Utwórz pusty `tests/desktop/__init__.py`, a potem fałszywą szynę `tests/desktop/fakes.py`:
- [x] Step 3: Napisz testy (padające) `tests/desktop/test_bus.py`
- [x] Step 4: Uruchom — mają paść
- [x] Step 5: Zaimplementuj `src/kimai_tray/desktop/__init__.py` i `src/kimai_tray/desktop/bus.py`
- [x] Step 6: Uruchom — mają przejść
- [x] Step 7: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg: `180 passed, 9 deselected in 0.14s`

## Dziennik

### 2026-09-25
- **20:59** Utworzono zadanie z Planu 2.
- **21:00** Start wykonania (Native, na main).
- **21:00** Zamknięte: testy zielone (180 passed, 9 deselected in 0.14s), commity na main.

## Wynik

[src/kimai_tray/desktop/bus.py](../../../src/kimai_tray/desktop/bus.py): `SessionBus` (jeepney), `DBusCallError`, `PortalError`, protokoły `Bus`/`Expectation`, `portal_request` (subskrypcja Response przed wywołaniem). Fałszywa szyna: [tests/desktop/fakes.py](../../../tests/desktop/fakes.py). Testy: [tests/desktop/test_bus.py](../../../tests/desktop/test_bus.py) — 5 zielonych. Bez odchyleń od planu.
