---
noteId: "33cad5a935d24a40a9faabae4f43a1a9"
tytul: "Plan 4 · Zadanie 6: GitHub Actions — testy i wydanie"
numer: "0051"
status: zrobione
priorytet: p1
tags: [todo, plan-4, flatpak]
zalezy_od: ["0050"]
utworzono: 2026-09-26 11:28
zaktualizowano: 2026-09-26 11:58
zamknieto: 2026-09-26 11:58
---

# 0051 — Plan 4 · Zadanie 6: GitHub Actions — testy i wydanie

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 6** z [Planu 4: Flatpak i wydanie](../../../docs/plany/2026-09-26-plan-4-flatpak.md)
(sekcja „Task 6: GitHub Actions — testy i wydanie”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-26-plan-4-flatpak.md](../../../docs/plany/2026-09-26-plan-4-flatpak.md) — kod, testy i komendy każdego
  kroku.
- Specyfikacja: [WS Tracker Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md); decyzje:
  [0045](../../W-TRAKCIE/0045-plan4-projekt-flatpak/todo.md).
- Pliki:

- Create: `.github/workflows/testy.yml`, `.github/workflows/wydanie.yml`
- Modify: `tests/test_pakiet.py`
- Create (skill `nowa-integracja`): `docs/integracje/github-actions.md`, `docs/integracje/github-pages.md`
- Create (skill `nowa-decyzja`): `docs/decyzje/0007-dystrybucja-repozytorium-flatpak-na-github-pages.md`

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] Wynik planu: 413 passed, 1 skipped; `actionlint` bez uwag.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające)
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Zaimplementuj
- [x] Step 4: Uruchom — mają przejść
- [x] Step 5: Dokumentacja
- [x] Step 6: Commit

## Materiały

- [testy/pytest-2026-09-26.txt](testy/pytest-2026-09-26.txt) — końcowy przebieg:
  `413 passed, 1 skipped, 12 deselected in 2.46s`

## Dziennik

### 2026-09-26

- **11:28** Utworzono zadanie z Planu 4.
- **11:55** Start wykonania.
- **11:58** Zamknięte: 413 passed, 1 skipped, 12 deselected in 2.46s, commity na main.

## Wynik

Workflowy [testy.yml](../../../.github/workflows/testy.yml) i [wydanie.yml](../../../.github/workflows/wydanie.yml)
(actionlint bez uwag), testy w [test_pakiet.py](../../../tests/test_pakiet.py). Dokumentacja:
[GitHub Actions](../../../docs/integracje/github-actions.md), [GitHub Pages](../../../docs/integracje/github-pages.md),
[ADR-0007](../../../docs/decyzje/0007-dystrybucja-repozytorium-flatpak-na-github-pages.md). Workflowy uruchomią się
dopiero po pushu (zadanie 8).
