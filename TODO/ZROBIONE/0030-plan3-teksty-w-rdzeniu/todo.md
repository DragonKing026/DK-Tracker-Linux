---
noteId: "c19411043b0d4fe6bf7c0441143dbbbc"
tytul: "Plan 3 · Zadanie 2: Teksty tacki i listy w rdzeniu (`core/presentation.py`)"
numer: "0030"
status: zrobione
priorytet: p1
tags: [todo, plan-3, ui]
zalezy_od: ["0029"]
utworzono: 2026-09-25 23:07
zaktualizowano: 2026-09-25 23:08
zamknieto: 2026-09-25 23:08
---

# 0030 — Plan 3 · Zadanie 2: Teksty tacki i listy w rdzeniu (`core/presentation.py`)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 2** z [Planu 3: Interfejs Qt](../../../docs/plany/2026-09-25-plan-3-ui.md)
(sekcja „Task 2: Teksty tacki i listy w rdzeniu (`core/presentation.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-3-ui.md](../../../docs/plany/2026-09-25-plan-3-ui.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md); decyzje UI:
  [0028](../0028-plan3-projekt-ui/todo.md).
- Pliki:
- Create: `src/kimai_tray/core/presentation.py`
- Test: `tests/core/test_presentation.py`

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] Wynik planu: 10 PASS, całość 237.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające)
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Zaimplementuj
- [x] Step 4: Uruchom — mają przejść
- [x] Step 5: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg: `237 passed, 12 deselected in 0.19s`

## Dziennik

### 2026-09-25

- **23:07** Utworzono zadanie z Planu 3.
- **23:08** Start wykonania.
- **23:08** Zamknięte: testy zielone (237 passed, 12 deselected in 0.19s), commity na main.

## Wynik

[presentation.py](../../../src/ws_tracker_tray/core/presentation.py): `tray_status`, `display_zone`, `day_label`,
`entry_row`. Testy: [test_presentation.py](../../../tests/core/test_presentation.py) — 10 zielonych. Bez odchyleń od
planu.
