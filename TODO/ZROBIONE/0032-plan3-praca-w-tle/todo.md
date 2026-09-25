---
noteId: "76fbf4538b6541f0a3c62a789906aa1c"
tytul: "Plan 3 · Zadanie 4: Praca w tle (`ui/worker.py`)"
numer: "0032"
status: zrobione
priorytet: p1
tags: [todo, plan-3, ui]
zalezy_od: ["0031"]
utworzono: 2026-09-25 23:07
zaktualizowano: 2026-09-25 23:09
zamknieto: 2026-09-25 23:09
---

# 0032 — Plan 3 · Zadanie 4: Praca w tle (`ui/worker.py`)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 4** z [Planu 3: Interfejs Qt](../../../docs/plany/2026-09-25-plan-3-ui.md)
(sekcja „Task 4: Praca w tle (`ui/worker.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-3-ui.md](../../../docs/plany/2026-09-25-plan-3-ui.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md); decyzje UI: [0028](../0028-plan3-projekt-ui/todo.md).
- Pliki:
- Create: `src/kimai_tray/ui/worker.py`
- Test: `tests/ui/test_worker.py`

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] Wynik planu: 6 PASS, całość 252.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające)
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Zaimplementuj
- [x] Step 4: Uruchom — mają przejść
- [x] Step 5: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg: `252 passed, 12 deselected in 0.34s`

## Dziennik

### 2026-09-25
- **23:07** Utworzono zadanie z Planu 3.
- **23:08** Start wykonania.
- **23:09** Zamknięte: testy zielone (252 passed, 12 deselected in 0.34s), commity na main.

## Wynik

[worker.py](../../../src/kimai_tray/ui/worker.py): `Worker` (jeden wątek, klucze, `busy`). Testy: [test_worker.py](../../../tests/ui/test_worker.py) — 6 zielonych. Bez odchyleń od planu.
