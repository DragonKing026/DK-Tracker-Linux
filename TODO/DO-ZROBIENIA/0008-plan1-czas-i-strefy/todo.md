---
noteId: "4dec5afaac8647d1b61c56595efd9848"
tytul: "Plan 1 · Zadanie 4: Czas i strefy (`timefmt.py`)"
numer: "0008"
status: do-zrobienia
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0007"]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
zamknieto:
---

# 0008 — Plan 1 · Zadanie 4: Czas i strefy (`timefmt.py`)

> [!info] Status
> **do-zrobienia** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 4** z [Planu 1: Rdzeń](../../../docs/plany/2026-09-25-plan-1-rdzen.md)
(sekcja „Task 4: Czas i strefy (`timefmt.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-1-rdzen.md](../../../docs/plany/2026-09-25-plan-1-rdzen.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Pliki:
- Create: `src/kimai_tray/core/timefmt.py`
- Test: `tests/core/test_timefmt.py`

## Kryteria akceptacji

- [ ] Każdy test z zadania napisany przed kodem i widziany jako padający
- [ ] `.venv/bin/pytest tests/core/test_timefmt.py -v` → wszystkie PASS (19 przypadków z parametryzacją).
- [ ] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [ ] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [ ] Step 1: Napisz testy (padające)
- [ ] Step 2: Uruchom — mają paść
- [ ] Step 3: Zaimplementuj `src/kimai_tray/core/timefmt.py`
- [ ] Step 4: Uruchom — mają przejść
- [ ] Step 5: Commit

## Materiały

- `testy/` — wynik końcowego przebiegu testów zadania

## Dziennik

### 2026-09-25
- Utworzono zadanie z Planu 1.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
