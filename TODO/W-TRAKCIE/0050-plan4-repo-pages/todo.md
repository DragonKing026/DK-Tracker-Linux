---
noteId: "cd296bd545804359a5a4559eb4f7e6e5"
tytul: "Plan 4 · Zadanie 5: Repozytorium Flatpaka dla GitHub Pages"
numer: "0050"
status: w-trakcie
priorytet: p1
tags: [todo, plan-4, flatpak]
zalezy_od: ["0049"]
utworzono: 2026-09-26 11:28
zaktualizowano: 2026-09-26 11:54
zamknieto:
---

# 0050 — Plan 4 · Zadanie 5: Repozytorium Flatpaka dla GitHub Pages

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 5** z [Planu 4: Flatpak i wydanie](../../../docs/plany/2026-09-26-plan-4-flatpak.md)
(sekcja „Task 5: Repozytorium Flatpaka dla GitHub Pages”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-26-plan-4-flatpak.md](../../../docs/plany/2026-09-26-plan-4-flatpak.md) — kod, testy i komendy każdego
  kroku.
- Specyfikacja: [WS Tracker Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md); decyzje:
  [0045](../0045-plan4-projekt-flatpak/todo.md).
- Pliki:

- Create: `flatpak/pages.py`, `flatpak/publikuj.sh`, `flatpak/klucz-gpg.sh`
- Test: `tests/test_strona_repo.py`

## Kryteria akceptacji

- [ ] Każdy test z zadania napisany przed kodem i widziany jako padający
- [ ] Wynik planu: 411 passed, 1 skipped; próba na sucho bez ostrzeżeń GPG.
- [ ] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [ ] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [ ] Step 1: Napisz testy (padające)
- [ ] Step 2: Uruchom — mają paść
- [ ] Step 3: Zaimplementuj
- [ ] Step 4: Uruchom — mają przejść
- [ ] Step 5: Próba na sucho w kontenerze
- [ ] Step 6: Commit

## Materiały

Brak (materiały pojawią się w podfolderach przy wykonaniu).

## Dziennik

### 2026-09-26

- **11:28** Utworzono zadanie z Planu 4.
- **11:54** Start wykonania.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
