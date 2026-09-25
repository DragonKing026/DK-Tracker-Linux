---
noteId: "1bcc8bed6a9145e5b30403431017a2dd"
tytul: "Plan 1 · Zadanie 2: Błędy (`errors.py`)"
numer: "0006"
status: zrobione
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0005"]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
zamknieto: 2026-09-25
---

# 0006 — Plan 1 · Zadanie 2: Błędy (`errors.py`)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

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

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] `.venv/bin/pytest tests/core/test_errors.py -v` → 13 PASS.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające)
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Zaimplementuj `src/kimai_tray/core/errors.py`
- [x] Step 4: Uruchom — mają przejść
- [x] Step 5: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg: `16 passed in 0.03s`

## Dziennik

### 2026-09-25
- Utworzono zadanie z Planu 1.
- Start wykonania.
- Zamknięte: testy zielone, commity w gałęzi feat/plan-1-rdzen.

## Wynik

[src/kimai_tray/core/errors.py](../../../src/kimai_tray/core/errors.py): `ApiError` (rodzaje błędów, zbieranie błędów formularza Kimai), `TrackerError`, `describe()`. Testy: [tests/core/test_errors.py](../../../tests/core/test_errors.py) — 13 zielonych. Bez odchyleń od planu.
