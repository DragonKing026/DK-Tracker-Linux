---
noteId: "ae53987a091d4a14b43418a68f7cf64a"
tytul: "Plan 3 · Zadanie 5: Stan aplikacji i ikona w tacce (`ui/state.py`, `ui/tray.py`)"
numer: "0033"
status: zrobione
priorytet: p1
tags: [todo, plan-3, ui]
zalezy_od: ["0032"]
utworzono: 2026-09-25 23:07
zaktualizowano: 2026-09-25 23:09
zamknieto: 2026-09-25 23:09
---

# 0033 — Plan 3 · Zadanie 5: Stan aplikacji i ikona w tacce (`ui/state.py`, `ui/tray.py`)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 5** z [Planu 3: Interfejs Qt](../../../docs/plany/2026-09-25-plan-3-ui.md)
(sekcja „Task 5: Stan aplikacji i ikona w tacce (`ui/state.py`, `ui/tray.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-3-ui.md](../../../docs/plany/2026-09-25-plan-3-ui.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md); decyzje UI: [0028](../0028-plan3-projekt-ui/todo.md).
- Pliki:
- Create: `src/kimai_tray/ui/state.py`, `src/kimai_tray/ui/tray.py`
- Test: `tests/ui/test_tray.py`
- Modify: `docs/integracje/statusnotifieritem.md` („Gdzie w kodzie”)

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] Wynik planu: 7 PASS, całość 259.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające)
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Zaimplementuj
- [x] Step 4: Uruchom — mają przejść
- [x] Step 5: Dokumentacja
- [x] Step 6: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg: `259 passed, 12 deselected in 0.36s`

## Dziennik

### 2026-09-25
- **23:07** Utworzono zadanie z Planu 3.
- **23:09** Start wykonania.
- **23:09** Zamknięte: testy zielone (259 passed, 12 deselected in 0.36s), commity na main.

## Wynik

[state.py](../../../src/kimai_tray/ui/state.py) (`AppState`), [tray.py](../../../src/kimai_tray/ui/tray.py) (`Tray`: ikona, tooltip, menu). Testy: [test_tray.py](../../../tests/ui/test_tray.py) — 7 zielonych. Dokumentacja: [StatusNotifierItem](../../../docs/integracje/statusnotifieritem.md). Bez odchyleń od planu.
