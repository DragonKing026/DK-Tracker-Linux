---
noteId: "e922262bb3ed471dac98637e4d227e73"
tytul: "Plan 1 · Zadanie 14: Komendy, pokrycie i dokumentacja rdzenia"
numer: "0018"
status: zrobione
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0017"]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
zamknieto: 2026-09-25
---

# 0018 — Plan 1 · Zadanie 14: Komendy, pokrycie i dokumentacja rdzenia

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 14** z [Planu 1: Rdzeń](../../../docs/plany/2026-09-25-plan-1-rdzen.md)
(sekcja „Task 14: Komendy, pokrycie i dokumentacja rdzenia”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-1-rdzen.md](../../../docs/plany/2026-09-25-plan-1-rdzen.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Pliki:
- Modify: `AGENTS.md` (sekcja „7. Komendy”)
- Modify: `docs/architektura/architektura-aplikacji.md` (tabela komponentów → ścieżki modułów)
- Modify: `docs/architektura/struktura-repozytorium.md` (drzewo: `src/`, `tests/core/`, `pyproject.toml`)

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] `.venv/bin/pytest --cov=kimai_tray.core --cov-report=term-missing --cov-fail-under=90` → PASS, „Required test coverage of 90% reached”. Jeśli nie — dopisz testy dla linii z `term-missing` w odpowiednim pliku `tests/core/test_*.py` (nie obniżaj progu).
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Sprawdź pokrycie
- [x] Step 2: Uzupełnij `AGENTS.md` → „7. Komendy”
- [x] Step 3: Zaktualizuj `docs/architektura/architektura-aplikacji.md`
- [x] Step 4: Zaktualizuj `docs/architektura/struktura-repozytorium.md`
- [x] Step 5: Kontrola i commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg: `144 passed, 8 deselected in 0.11s`
- [testy/pokrycie-2026-09-25.txt](testy/pokrycie-2026-09-25.txt) — raport pokrycia rdzenia: 98,34%

## Dziennik

### 2026-09-25
- Utworzono zadanie z Planu 1.
- Start wykonania.
- Zamknięte: testy zielone, commity w gałęzi feat/plan-1-rdzen.

## Wynik

Pokrycie rdzenia **98,34%** (próg 90%) — [raport](testy/pokrycie-2026-09-25.txt). [AGENTS.md](../../../AGENTS.md) → „Komendy”: venv, pytest, pokrycie, testy kontraktowe, ruff. [Architektura](../../../docs/architektura/architektura-aplikacji.md): mapa modułów rdzenia. [Struktura repozytorium](../../../docs/architektura/struktura-repozytorium.md): src/, tests/, pyproject.toml. Ruling: osobna tabela modułów zamiast kolumny.
