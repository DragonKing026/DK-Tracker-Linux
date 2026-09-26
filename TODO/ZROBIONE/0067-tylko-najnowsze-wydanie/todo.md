---
noteId: "b7cc90570da84e4f9c711ffb6820486a"
tytul: "Na GitHubie tylko najnowsze wydanie; starsze jako tagi"
numer: "0067"
status: zrobione
priorytet: p2
tags: [todo, wydanie, github]
zalezy_od: []
utworzono: 2026-09-26 15:44
zaktualizowano: 2026-09-26 15:45
zamknieto: 2026-09-26 15:45
---

# 0067 — Na GitHubie tylko najnowsze wydanie; starsze jako tagi

> [!info] Status
> **zrobione** · priorytet **p2** · [← tablica zadań](../../README.md)

## Cel

Lista Releases pokazuje tylko najnowsze wydanie; starsze wersje zostają w historii gita jako tagi. Wydania 0.x zostają
pre-release do 1.0 (decyzja użytkownika).

## Kontekst

- Uwaga użytkownika: na stronie repozytorium widać „Deployments” (GitHub Pages — repozytorium Flatpaka, niezbędne dla
  aktualizacji; ukrywa się je w ustawieniach strony głównej repozytorium) i wszystkie stare wydania.
- Decyzja: usuwać strony starszych wydań automatycznie przy każdym nowym wydaniu, tagi zostają.

## Kryteria akceptacji

- [x] Strony wydań 0.9.0–0.9.2 usunięte, tagi zostają
- [x] [wydanie.yml](../../../.github/workflows/wydanie.yml) po utworzeniu wydania usuwa strony poprzednich (test)
- [x] [wydania.md](../../../docs/procesy/wydania.md) opisuje zasadę i ukrycie „Deployments”

## Kroki

- [x] Test, workflow, usunięcie starych stron, dokumentacja

## Materiały

- Wynik: 467 passed, 1 skipped, 14 deselected in 3.52s

## Dziennik

### 2026-09-26

- **15:44** Utworzono i start.
- **15:45** Zamknięte: 467 passed, 1 skipped, 14 deselected in 3.52s, commity na main.

## Wynik

Strony wydań 0.9.0–0.9.2 usunięte (tagi zostały); [wydanie.yml](../../../.github/workflows/wydanie.yml) usuwa strony
poprzednich wydań po nowym; [wydania.md](../../../docs/procesy/wydania.md) opisuje zasadę i ukrycie „Deployments”.
