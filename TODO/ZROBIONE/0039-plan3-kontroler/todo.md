---
noteId: "c6c96eb07ed54d74bec84e16bde6aba1"
tytul: "Plan 3 · Zadanie 11: Kontroler aplikacji (`ui/app.py`)"
numer: "0039"
status: zrobione
priorytet: p1
tags: [todo, plan-3, ui]
zalezy_od: ["0038"]
utworzono: 2026-09-25 23:07
zaktualizowano: 2026-09-25 23:10
zamknieto: 2026-09-25 23:10
---

# 0039 — Plan 3 · Zadanie 11: Kontroler aplikacji (`ui/app.py`)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 11** z [Planu 3: Interfejs Qt](../../../docs/plany/2026-09-25-plan-3-ui.md)
(sekcja „Task 11: Kontroler aplikacji (`ui/app.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-3-ui.md](../../../docs/plany/2026-09-25-plan-3-ui.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md); decyzje UI:
  [0028](../0028-plan3-projekt-ui/todo.md).
- Pliki:
- Modify: `src/kimai_tray/core/settings.py` (`Memory.tray_hint_shown`), `src/kimai_tray/core/tracker.py`
  (`Tracker.remember`)
- Modify: `tests/core/test_tracker_refresh.py`
- Create: `src/kimai_tray/ui/app.py`
- Test: `tests/ui/test_app.py`

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] Wynik planu: 14 PASS, całość 328.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz test rdzenia (padający)
- [x] Step 2: Rdzeń
- [x] Step 3: Napisz testy kontrolera (padające)
- [x] Step 4: Uruchom — mają paść
- [x] Step 5: Zaimplementuj
- [x] Step 6: Uruchom — mają przejść
- [x] Step 7: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg:
  `328 passed, 1 skipped, 12 deselected in 1.04s`

## Dziennik

### 2026-09-25

- **23:07** Utworzono zadanie z Planu 3.
- **23:10** Start wykonania.
- **23:10** Zamknięte: testy zielone (328 passed, 1 skipped, 12 deselected in 1.04s), commity na main.

## Wynik

[app.py](../../../src/ws_tracker_tray/ui/app.py): `Controller`; w rdzeniu `Memory.tray_hint_shown` i `Tracker.remember`.
Testy: [test_app.py](../../../tests/ui/test_app.py) — 14 zielonych,
[test_tracker_refresh.py](../../../tests/core/test_tracker_refresh.py) +1. Bez odchyleń od planu.
