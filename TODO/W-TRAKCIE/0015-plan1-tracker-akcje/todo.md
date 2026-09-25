---
noteId: "e69841fb57c64eb7abda7346719a1806"
tytul: "Plan 1 · Zadanie 11: Tracker — akcje (`tracker.py` część 2, F-04…F-10)"
numer: "0015"
status: w-trakcie
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0014"]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
zamknieto:
---

# 0015 — Plan 1 · Zadanie 11: Tracker — akcje (`tracker.py` część 2, F-04…F-10)

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 11** z [Planu 1: Rdzeń](../../../docs/plany/2026-09-25-plan-1-rdzen.md)
(sekcja „Task 11: Tracker — akcje (`tracker.py` część 2, F-04…F-10)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-1-rdzen.md](../../../docs/plany/2026-09-25-plan-1-rdzen.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Pliki:
- Modify: `src/kimai_tray/core/tracker.py` (dopisanie metod akcji i importów)
- Test: `tests/core/test_tracker_actions.py`

## Kryteria akceptacji

- [ ] Każdy test z zadania napisany przed kodem i widziany jako padający
- [ ] `.venv/bin/pytest tests/core/test_tracker_actions.py tests/core/test_tracker_refresh.py -v` → wszystkie PASS.
- [ ] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [ ] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [ ] Step 1: Napisz testy (padające) `tests/core/test_tracker_actions.py`
- [ ] Step 2: Uruchom — mają paść
- [ ] Step 3: Dopisz importy w `src/kimai_tray/core/tracker.py`
- [ ] Step 4: Dopisz metody akcji do klasy `Tracker`
- [ ] Step 5: Dopisz metody pomocnicze do sekcji `# -- internals`
- [ ] Step 6: Uruchom — mają przejść
- [ ] Step 7: Commit

## Materiały

- `testy/` — wynik końcowego przebiegu testów zadania

## Dziennik

### 2026-09-25
- Utworzono zadanie z Planu 1.
- Start wykonania.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
