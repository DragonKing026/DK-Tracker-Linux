---
noteId: "e922262bb3ed471dac98637e4d227e73"
tytul: "Plan 1 · Zadanie 14: Komendy, pokrycie i dokumentacja rdzenia"
numer: "0018"
status: do-zrobienia
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0017"]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
zamknieto:
---

# 0018 — Plan 1 · Zadanie 14: Komendy, pokrycie i dokumentacja rdzenia

> [!info] Status
> **do-zrobienia** · priorytet **p1** · [← tablica zadań](../../README.md)

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

- [ ] Każdy test z zadania napisany przed kodem i widziany jako padający
- [ ] `.venv/bin/pytest --cov=kimai_tray.core --cov-report=term-missing --cov-fail-under=90` → PASS, „Required test coverage of 90% reached”. Jeśli nie — dopisz testy dla linii z `term-missing` w odpowiednim pliku `tests/core/test_*.py` (nie obniżaj progu).
- [ ] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [ ] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [ ] Step 1: Sprawdź pokrycie
- [ ] Step 2: Uzupełnij `AGENTS.md` → „7. Komendy”
- [ ] Step 3: Zaktualizuj `docs/architektura/architektura-aplikacji.md`
- [ ] Step 4: Zaktualizuj `docs/architektura/struktura-repozytorium.md`
- [ ] Step 5: Kontrola i commit

## Materiały

- `testy/` — wynik końcowego przebiegu testów zadania

## Dziennik

### 2026-09-25
- Utworzono zadanie z Planu 1.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
