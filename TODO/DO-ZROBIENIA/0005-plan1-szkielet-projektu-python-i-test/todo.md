---
noteId: "ced057af55a84b4f97cf2f7d2e83df13"
tytul: "Plan 1 · Zadanie 1: Szkielet projektu Python i test architektury"
numer: "0005"
status: do-zrobienia
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0002"]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
zamknieto:
---

# 0005 — Plan 1 · Zadanie 1: Szkielet projektu Python i test architektury

> [!info] Status
> **do-zrobienia** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 1** z [Planu 1: Rdzeń](../../../docs/plany/2026-09-25-plan-1-rdzen.md)
(sekcja „Task 1: Szkielet projektu Python i test architektury”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-1-rdzen.md](../../../docs/plany/2026-09-25-plan-1-rdzen.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Pliki:
- Create: `pyproject.toml`
- Create: `src/kimai_tray/__init__.py`, `src/kimai_tray/core/__init__.py`
- Create: `tests/__init__.py`, `tests/core/__init__.py`, `tests/test_architektura.py`, `tests/core/test_package.py`
- Modify: `.gitignore`

## Kryteria akceptacji

- [ ] Każdy test z zadania napisany przed kodem i widziany jako padający

- [ ] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [ ] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [ ] Step 1: Utwórz `pyproject.toml`
- [ ] Step 2: Dopisz do `.gitignore`
- [ ] Step 3: Napisz testy (padające)
- [ ] Step 4: Utwórz środowisko i uruchom testy — mają paść
- [ ] Step 5: Utwórz pakiet
- [ ] Step 6: Zainstaluj i uruchom testy — mają przejść
- [ ] Step 7: Commit

## Materiały

- `testy/` — wynik końcowego przebiegu testów zadania

## Dziennik

### 2026-09-25
- Utworzono zadanie z Planu 1.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
