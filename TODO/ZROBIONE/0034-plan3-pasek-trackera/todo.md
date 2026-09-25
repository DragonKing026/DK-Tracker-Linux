---
noteId: "0ec6a10be4da4a6c9a1214eedca53467"
tytul: "Plan 3 · Zadanie 6: Pasek trackera (`ui/form.py`)"
numer: "0034"
status: zrobione
priorytet: p1
tags: [todo, plan-3, ui]
zalezy_od: ["0033"]
utworzono: 2026-09-25 23:07
zaktualizowano: 2026-09-25 23:09
zamknieto: 2026-09-25 23:09
---

# 0034 — Plan 3 · Zadanie 6: Pasek trackera (`ui/form.py`)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 6** z [Planu 3: Interfejs Qt](../../../docs/plany/2026-09-25-plan-3-ui.md)
(sekcja „Task 6: Pasek trackera (`ui/form.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-3-ui.md](../../../docs/plany/2026-09-25-plan-3-ui.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md); decyzje UI:
  [0028](../0028-plan3-projekt-ui/todo.md).
- Pliki:
- Create: `src/kimai_tray/ui/form.py`
- Test: `tests/ui/test_form.py`

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] Wynik planu: 19 PASS, całość 278.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające)
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Zaimplementuj
- [x] Step 4: Uruchom — mają przejść
- [x] Step 5: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg: `278 passed, 12 deselected in 0.55s`

## Dziennik

### 2026-09-25

- **23:07** Utworzono zadanie z Planu 3.
- **23:09** Start wykonania.
- **23:09** Zamknięte: testy zielone (278 passed, 12 deselected in 0.55s), commity na main.

## Wynik

[form.py](../../../src/kimai_tray/ui/form.py): `TrackerForm`, `DescriptionEdit`, `dot`. Testy:
[test_form.py](../../../tests/ui/test_form.py) — 19 zielonych. Bez odchyleń od planu.
