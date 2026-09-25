---
noteId: "e69841fb57c64eb7abda7346719a1806"
tytul: "Plan 1 · Zadanie 11: Tracker — akcje (`tracker.py` część 2, F-04…F-10)"
numer: "0015"
status: zrobione
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0014"]
utworzono: 2026-09-25 19:03
zaktualizowano: 2026-09-25 19:03
zamknieto: 2026-09-25 19:03
---

# 0015 — Plan 1 · Zadanie 11: Tracker — akcje (`tracker.py` część 2, F-04…F-10)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 11** z [Planu 1: Rdzeń](../../../docs/plany/2026-09-25-plan-1-rdzen.md)
(sekcja „Task 11: Tracker — akcje (`tracker.py` część 2, F-04…F-10)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-1-rdzen.md](../../../docs/plany/2026-09-25-plan-1-rdzen.md) — kod, testy i komendy każdego
  kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Pliki:
- Modify: `src/kimai_tray/core/tracker.py` (dopisanie metod akcji i importów)
- Test: `tests/core/test_tracker_actions.py`

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] `.venv/bin/pytest tests/core/test_tracker_actions.py tests/core/test_tracker_refresh.py -v` → wszystkie PASS.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające) `tests/core/test_tracker_actions.py`
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Dopisz importy w `src/kimai_tray/core/tracker.py`
- [x] Step 4: Dopisz metody akcji do klasy `Tracker`
- [x] Step 5: Dopisz metody pomocnicze do sekcji `# -- internals`
- [x] Step 6: Uruchom — mają przejść
- [x] Step 7: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg: `135 passed in 0.10s`

## Dziennik

### 2026-09-25

- Utworzono zadanie z Planu 1.
- Start wykonania.
- Zamknięte: testy zielone, commity w gałęzi feat/plan-1-rdzen.

## Wynik

[src/kimai_tray/core/tracker.py](../../../src/kimai_tray/core/tracker.py) (część 2): `start` (czas w strefie konta,
ponowienie bez billable i blokada, timeout bez ponownego POST), `stop` (także z godziną końca), `resume` (sprawdzenie
przed zatrzymaniem), `update_description/update_begin`, `set_billable`, `apply_settings`. Testy:
[tests/core/test_tracker_actions.py](../../../tests/core/test_tracker_actions.py) — 25 zielonych (RED: 25×
AttributeError). Bez odchyleń.
