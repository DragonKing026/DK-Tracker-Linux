---
noteId: "1b424de021dc418d81c73c71abfe0bb9"
tytul: "Plan 4 · Zadanie 7: Proces wydania i instrukcja instalacji"
numer: "0052"
status: zrobione
priorytet: p1
tags: [todo, plan-4, flatpak]
zalezy_od: ["0051"]
utworzono: 2026-09-26 11:28
zaktualizowano: 2026-09-26 11:59
zamknieto: 2026-09-26 11:59
---

# 0052 — Plan 4 · Zadanie 7: Proces wydania i instrukcja instalacji

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 7** z [Planu 4: Flatpak i wydanie](../../../docs/plany/2026-09-26-plan-4-flatpak.md)
(sekcja „Task 7: Proces wydania i instrukcja instalacji”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-26-plan-4-flatpak.md](../../../docs/plany/2026-09-26-plan-4-flatpak.md) — kod, testy i komendy każdego
  kroku.
- Specyfikacja: [WS Tracker Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md); decyzje:
  [0045](../../W-TRAKCIE/0045-plan4-projekt-flatpak/todo.md).
- Pliki:

- Create: `docs/procesy/wydania.md`
- Modify: `.github/README.md` (instalacja), `README.md` (instalacja, status),
  `docs/architektura/struktura-repozytorium.md`
  (`flatpak/`, `data/`, `.github/`), `docs/README.md` (link do wydań)

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] Wynik planu: linki, frontmatter i markdownlint bez uwag.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: `docs/procesy/wydania.md`
- [x] Step 2: `.github/README.md` i `README.md` → „Instalacja”
- [x] Step 3: Struktura
- [x] Step 4: Kontrole
- [x] Step 5: Commit

## Materiały

- [testy/pytest-2026-09-26.txt](testy/pytest-2026-09-26.txt) — końcowy przebieg:
  `413 passed, 1 skipped, 12 deselected in 2.46s`

## Dziennik

### 2026-09-26

- **11:28** Utworzono zadanie z Planu 4.
- **11:58** Start wykonania.
- **11:59** Zamknięte: 413 passed, 1 skipped, 12 deselected in 2.46s, commity na main.

## Wynik

[Wydania i instalacja](../../../docs/procesy/wydania.md), sekcja „Instalacja” w [README](../../../README.md) i
[.github/README.md](../../../.github/README.md),
[struktura repozytorium](../../../docs/architektura/struktura-repozytorium.md),
link w [indeksie dokumentacji](../../../docs/README.md). Linki, frontmatter i markdownlint bez uwag.
