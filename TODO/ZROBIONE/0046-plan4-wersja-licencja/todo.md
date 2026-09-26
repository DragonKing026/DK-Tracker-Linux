---
noteId: "399710040deb43d4b12435b1527e025b"
tytul: "Plan 4 · Zadanie 1: Wersja 0.9.0 i licencja w pakiecie"
numer: "0046"
status: zrobione
priorytet: p1
tags: [todo, plan-4, flatpak]
zalezy_od: ["0045"]
utworzono: 2026-09-26 11:28
zaktualizowano: 2026-09-26 11:30
zamknieto: 2026-09-26 11:30
---

# 0046 — Plan 4 · Zadanie 1: Wersja 0.9.0 i licencja w pakiecie

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 1** z [Planu 4: Flatpak i wydanie](../../../docs/plany/2026-09-26-plan-4-flatpak.md)
(sekcja „Task 1: Wersja 0.9.0 i licencja w pakiecie”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-26-plan-4-flatpak.md](../../../docs/plany/2026-09-26-plan-4-flatpak.md) — kod, testy i komendy każdego
  kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md); decyzje:
  [0045](../0045-plan4-projekt-flatpak/todo.md).
- Pliki:

- Modify: `pyproject.toml`, `src/kimai_tray/__init__.py`, `tests/core/test_package.py`
- Create: `tests/test_pakiet.py`

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] Wynik planu: 399 passed, 1 skipped.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające)
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Zaimplementuj
- [x] Step 4: Uruchom — mają przejść
- [x] Step 5: Commit

## Materiały

- [testy/pytest-2026-09-26.txt](testy/pytest-2026-09-26.txt) — końcowy przebieg:
  `399 passed, 1 skipped, 12 deselected in 2.46s`

## Dziennik

### 2026-09-26

- **11:28** Utworzono zadanie z Planu 4.
- **11:29** Start wykonania.
- **11:30** Zamknięte: 399 passed, 1 skipped, 12 deselected in 2.46s, commity na main.

## Wynik

Wersja **0.9.0** i licencja **AGPL-3.0-or-later** (PEP 639) w [pyproject.toml](../../../pyproject.toml) i
[`__init__.py`](../../../src/dk_tracker/__init__.py); testy spójności:
[test_pakiet.py](../../../tests/test_pakiet.py).
Bez odchyleń od planu.
