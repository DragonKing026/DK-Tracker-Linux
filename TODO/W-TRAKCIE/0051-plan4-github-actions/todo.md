---
noteId: "33cad5a935d24a40a9faabae4f43a1a9"
tytul: "Plan 4 · Zadanie 6: GitHub Actions — testy i wydanie"
numer: "0051"
status: w-trakcie
priorytet: p1
tags: [todo, plan-4, flatpak]
zalezy_od: ["0050"]
utworzono: 2026-09-26 11:28
zaktualizowano: 2026-09-26 11:55
zamknieto:
---

# 0051 — Plan 4 · Zadanie 6: GitHub Actions — testy i wydanie

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 6** z [Planu 4: Flatpak i wydanie](../../../docs/plany/2026-09-26-plan-4-flatpak.md)
(sekcja „Task 6: GitHub Actions — testy i wydanie”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-26-plan-4-flatpak.md](../../../docs/plany/2026-09-26-plan-4-flatpak.md) — kod, testy i komendy każdego
  kroku.
- Specyfikacja: [WS Tracker Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md); decyzje:
  [0045](../0045-plan4-projekt-flatpak/todo.md).
- Pliki:

- Create: `.github/workflows/testy.yml`, `.github/workflows/wydanie.yml`
- Modify: `tests/test_pakiet.py`
- Create (skill `nowa-integracja`): `docs/integracje/github-actions.md`, `docs/integracje/github-pages.md`
- Create (skill `nowa-decyzja`): `docs/decyzje/0007-dystrybucja-repozytorium-flatpak-na-github-pages.md`

## Kryteria akceptacji

- [ ] Każdy test z zadania napisany przed kodem i widziany jako padający
- [ ] Wynik planu: 413 passed, 1 skipped; `actionlint` bez uwag.
- [ ] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [ ] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [ ] Step 1: Napisz testy (padające)
- [ ] Step 2: Uruchom — mają paść
- [ ] Step 3: Zaimplementuj
- [ ] Step 4: Uruchom — mają przejść
- [ ] Step 5: Dokumentacja
- [ ] Step 6: Commit

## Materiały

Brak (materiały pojawią się w podfolderach przy wykonaniu).

## Dziennik

### 2026-09-26

- **11:28** Utworzono zadanie z Planu 4.
- **11:55** Start wykonania.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
