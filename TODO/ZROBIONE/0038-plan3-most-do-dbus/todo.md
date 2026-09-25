---
noteId: "b25d3cf758f94492b4b47a07133b756b"
tytul: "Plan 3 · Zadanie 10: Usługi pulpitu w wątkach UI (`ui/desktop_bridge.py`)"
numer: "0038"
status: zrobione
priorytet: p1
tags: [todo, plan-3, ui]
zalezy_od: ["0037"]
utworzono: 2026-09-25 23:07
zaktualizowano: 2026-09-25 23:10
zamknieto: 2026-09-25 23:10
---

# 0038 — Plan 3 · Zadanie 10: Usługi pulpitu w wątkach UI (`ui/desktop_bridge.py`)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 10** z [Planu 3: Interfejs Qt](../../../docs/plany/2026-09-25-plan-3-ui.md)
(sekcja „Task 10: Usługi pulpitu w wątkach UI (`ui/desktop_bridge.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-3-ui.md](../../../docs/plany/2026-09-25-plan-3-ui.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md); decyzje UI:
  [0028](../0028-plan3-projekt-ui/todo.md).
- Pliki:
- Create: `src/kimai_tray/ui/desktop_bridge.py`
- Test: `tests/ui/test_desktop_bridge.py`

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] Wynik planu: 3 PASS, całość 313.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające)
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Zaimplementuj
- [x] Step 4: Uruchom — mają przejść
- [x] Step 5: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg:
  `313 passed, 1 skipped, 12 deselected in 0.72s`

## Dziennik

### 2026-09-25

- **23:07** Utworzono zadanie z Planu 3.
- **23:10** Start wykonania.
- **23:10** Zamknięte: testy zielone (313 passed, 1 skipped, 12 deselected in 0.72s), commity na main.

## Wynik

[desktop_bridge.py](../../../src/kimai_tray/ui/desktop_bridge.py): `Desktop` (jedno połączenie w wątku „desktop”),
`ClickListener` (osobne połączenie). Testy: [test_desktop_bridge.py](../../../tests/ui/test_desktop_bridge.py) — 3
zielone. Bez odchyleń od planu.
