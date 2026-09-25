---
noteId: "e907f3179ef74e638478cb910aaa1405"
tytul: "Plan 1 · Zadanie 10: Tracker — stan i odświeżanie (`tracker.py` część 1)"
numer: "0014"
status: zrobione
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0013"]
utworzono: 2026-09-25 19:03
zaktualizowano: 2026-09-25 19:03
zamknieto: 2026-09-25 19:03
---

# 0014 — Plan 1 · Zadanie 10: Tracker — stan i odświeżanie (`tracker.py` część 1)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 10** z [Planu 1: Rdzeń](../../../docs/plany/2026-09-25-plan-1-rdzen.md)
(sekcja „Task 10: Tracker — stan i odświeżanie (`tracker.py` część 1)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-1-rdzen.md](../../../docs/plany/2026-09-25-plan-1-rdzen.md) — kod, testy i komendy każdego
  kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Pliki:
- Create: `src/kimai_tray/core/tracker.py`
- Create: `tests/core/fakes.py`
- Test: `tests/core/test_tracker_refresh.py`

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] `.venv/bin/pytest tests/core/test_tracker_refresh.py -v` → 14 PASS.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Utwórz fałszywego klienta `tests/core/fakes.py`
- [x] Step 2: Napisz testy (padające) `tests/core/test_tracker_refresh.py`
- [x] Step 3: Uruchom — mają paść
- [x] Step 4: Zaimplementuj `src/kimai_tray/core/tracker.py` (część 1)
- [x] Step 5: Uruchom — mają przejść
- [x] Step 6: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg: `110 passed in 0.09s`

## Dziennik

### 2026-09-25

- Utworzono zadanie z Planu 1.
- Start wykonania.
- Zamknięte: testy zielone, commity w gałęzi feat/plan-1-rdzen.

## Wynik

[src/kimai_tray/core/tracker.py](../../../src/kimai_tray/core/tracker.py) (część 1): `Snapshot`, `Totals`,
`Tracker.refresh_active/refresh_full/load_catalog/activities/default_billable/kimai_tz`, licznik błędów, flaga różnicy
stref, zapamiętanie locale. Fałszywy klient: [tests/core/fakes.py](../../../tests/core/fakes.py). 14 testów zielonych.
Bez odchyleń.
