---
noteId: "9e586034af2c47ada619f573c96e4dc8"
tytul: "Plan 3 · Zadanie 7: Ostatnie wpisy (`ui/recent.py`)"
numer: "0035"
status: zrobione
priorytet: p1
tags: [todo, plan-3, ui]
zalezy_od: ["0034"]
utworzono: 2026-09-25 23:07
zaktualizowano: 2026-09-25 23:09
zamknieto: 2026-09-25 23:09
---

# 0035 — Plan 3 · Zadanie 7: Ostatnie wpisy (`ui/recent.py`)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 7** z [Planu 3: Interfejs Qt](../../../docs/plany/2026-09-25-plan-3-ui.md)
(sekcja „Task 7: Ostatnie wpisy (`ui/recent.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-3-ui.md](../../../docs/plany/2026-09-25-plan-3-ui.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md); decyzje UI: [0028](../0028-plan3-projekt-ui/todo.md).
- Pliki:
- Create: `src/kimai_tray/ui/recent.py`
- Test: `tests/ui/test_recent.py`

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] Wynik planu: 7 PASS, całość 285.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające)
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Zaimplementuj
- [x] Step 4: Uruchom — mają przejść
- [x] Step 5: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg: `285 passed, 12 deselected in 0.57s`

## Dziennik

### 2026-09-25
- **23:07** Utworzono zadanie z Planu 3.
- **23:09** Start wykonania.
- **23:09** Zamknięte: testy zielone (285 passed, 12 deselected in 0.57s), commity na main.

## Wynik

[recent.py](../../../src/kimai_tray/ui/recent.py): `RecentList`, `EntryRow`. Testy: [test_recent.py](../../../tests/ui/test_recent.py) — 7 zielonych. Bez odchyleń od planu.
