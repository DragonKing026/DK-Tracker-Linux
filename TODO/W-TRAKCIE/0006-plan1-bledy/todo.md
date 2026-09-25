---
noteId: "1bcc8bed6a9145e5b30403431017a2dd"
tytul: "Plan 1 · Zadanie 2: Błędy (`errors.py`)"
numer: "0006"
status: w-trakcie
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0005"]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
zamknieto:
---

# 0006 — Plan 1 · Zadanie 2: Błędy (`errors.py`)

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 2** z [Planu 1: Rdzeń](../../../docs/plany/2026-09-25-plan-1-rdzen.md)
(sekcja „Task 2: Błędy (`errors.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-1-rdzen.md](../../../docs/plany/2026-09-25-plan-1-rdzen.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Pliki:
- Create: `src/kimai_tray/core/errors.py`
- Test: `tests/core/test_errors.py`

## Kryteria akceptacji

- [ ] Każdy test z zadania napisany przed kodem i widziany jako padający
- [ ] `.venv/bin/pytest tests/core/test_errors.py -v` → 13 PASS.
- [ ] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [ ] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [ ] Step 1: Napisz testy (padające)
- [ ] Step 2: Uruchom — mają paść
- [ ] Step 3: Zaimplementuj `src/kimai_tray/core/errors.py`
- [ ] Step 4: Uruchom — mają przejść
- [ ] Step 5: Commit

## Materiały

- `testy/` — wynik końcowego przebiegu testów zadania

## Dziennik

### 2026-09-25
- Utworzono zadanie z Planu 1.
- Start wykonania.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
