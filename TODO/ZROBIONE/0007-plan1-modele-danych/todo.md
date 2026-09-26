---
noteId: "a34f273545dd4505984ad704709ae5a3"
tytul: "Plan 1 · Zadanie 3: Modele danych (`models.py`)"
numer: "0007"
status: zrobione
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0006"]
utworzono: 2026-09-25 19:01
zaktualizowano: 2026-09-25 19:01
zamknieto: 2026-09-25 19:01
---

# 0007 — Plan 1 · Zadanie 3: Modele danych (`models.py`)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 3** z [Planu 1: Rdzeń](../../../docs/plany/2026-09-25-plan-1-rdzen.md)
(sekcja „Task 3: Modele danych (`models.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-1-rdzen.md](../../../docs/plany/2026-09-25-plan-1-rdzen.md) — kod, testy i komendy każdego
  kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Pliki:
- Create: `src/kimai_tray/core/models.py`
- Test: `tests/core/test_models.py`

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] `.venv/bin/pytest tests/core/test_models.py -v` → 7 PASS.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające)
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Zaimplementuj `src/kimai_tray/core/models.py`
- [x] Step 4: Uruchom — mają przejść
- [x] Step 5: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg: `23 passed in 0.04s`

## Dziennik

### 2026-09-25

- Utworzono zadanie z Planu 1.
- Start wykonania.
- Zamknięte: testy zielone, commity w gałęzi feat/plan-1-rdzen.

## Wynik

[src/kimai_tray/core/models.py](../../../src/dk_tracker/core/models.py): `User`, `Customer`, `Project`, `Activity`,
`Entry` z `from_api` (obiekty rozwinięte lub same id, brakujące pola). Testy:
[tests/core/test_models.py](../../../tests/core/test_models.py) — 7 zielonych. Bez odchyleń.
