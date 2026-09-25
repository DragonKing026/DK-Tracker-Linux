---
noteId: "7cb3ce12d7bb46f18e16d51aa4764890"
tytul: "Plan 1 · Zadanie 6: Grupowanie list i reguły billable (`grouping.py`, `billable.py`, F-06/F-08/F-09)"
numer: "0010"
status: do-zrobienia
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0009"]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
zamknieto:
---

# 0010 — Plan 1 · Zadanie 6: Grupowanie list i reguły billable (`grouping.py`, `billable.py`, F-06/F-08/F-09)

> [!info] Status
> **do-zrobienia** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 6** z [Planu 1: Rdzeń](../../../docs/plany/2026-09-25-plan-1-rdzen.md)
(sekcja „Task 6: Grupowanie list i reguły billable (`grouping.py`, `billable.py`, F-06/F-08/F-09)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-1-rdzen.md](../../../docs/plany/2026-09-25-plan-1-rdzen.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Pliki:
- Create: `src/kimai_tray/core/grouping.py`, `src/kimai_tray/core/billable.py`
- Test: `tests/core/test_grouping.py`, `tests/core/test_billable.py`

## Kryteria akceptacji

- [ ] Każdy test z zadania napisany przed kodem i widziany jako padający
- [ ] `.venv/bin/pytest tests/core/test_grouping.py tests/core/test_billable.py -v` → 7 PASS.
- [ ] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [ ] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [ ] Step 1: Napisz testy (padające)
- [ ] Step 2: Uruchom — mają paść
- [ ] Step 3: Zaimplementuj `src/kimai_tray/core/grouping.py`
- [ ] Step 4: Zaimplementuj `src/kimai_tray/core/billable.py`
- [ ] Step 5: Uruchom — mają przejść
- [ ] Step 6: Commit

## Materiały

- `testy/` — wynik końcowego przebiegu testów zadania

## Dziennik

### 2026-09-25
- Utworzono zadanie z Planu 1.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
