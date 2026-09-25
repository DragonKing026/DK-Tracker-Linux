---
noteId: "e907f3179ef74e638478cb910aaa1405"
tytul: "Plan 1 · Zadanie 10: Tracker — stan i odświeżanie (`tracker.py` część 1)"
numer: "0014"
status: do-zrobienia
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0013"]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
zamknieto:
---

# 0014 — Plan 1 · Zadanie 10: Tracker — stan i odświeżanie (`tracker.py` część 1)

> [!info] Status
> **do-zrobienia** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 10** z [Planu 1: Rdzeń](../../../docs/plany/2026-09-25-plan-1-rdzen.md)
(sekcja „Task 10: Tracker — stan i odświeżanie (`tracker.py` część 1)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-1-rdzen.md](../../../docs/plany/2026-09-25-plan-1-rdzen.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Pliki:
- Create: `src/kimai_tray/core/tracker.py`
- Create: `tests/core/fakes.py`
- Test: `tests/core/test_tracker_refresh.py`

## Kryteria akceptacji

- [ ] Każdy test z zadania napisany przed kodem i widziany jako padający
- [ ] `.venv/bin/pytest tests/core/test_tracker_refresh.py -v` → 14 PASS.
- [ ] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [ ] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [ ] Step 1: Utwórz fałszywego klienta `tests/core/fakes.py`
- [ ] Step 2: Napisz testy (padające) `tests/core/test_tracker_refresh.py`
- [ ] Step 3: Uruchom — mają paść
- [ ] Step 4: Zaimplementuj `src/kimai_tray/core/tracker.py` (część 1)
- [ ] Step 5: Uruchom — mają przejść
- [ ] Step 6: Commit

## Materiały

- `testy/` — wynik końcowego przebiegu testów zadania

## Dziennik

### 2026-09-25
- Utworzono zadanie z Planu 1.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
