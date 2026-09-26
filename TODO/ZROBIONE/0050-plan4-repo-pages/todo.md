---
noteId: "cd296bd545804359a5a4559eb4f7e6e5"
tytul: "Plan 4 · Zadanie 5: Repozytorium Flatpaka dla GitHub Pages"
numer: "0050"
status: zrobione
priorytet: p1
tags: [todo, plan-4, flatpak]
zalezy_od: ["0049"]
utworzono: 2026-09-26 11:28
zaktualizowano: 2026-09-26 11:55
zamknieto: 2026-09-26 11:55
---

# 0050 — Plan 4 · Zadanie 5: Repozytorium Flatpaka dla GitHub Pages

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 5** z [Planu 4: Flatpak i wydanie](../../../docs/plany/2026-09-26-plan-4-flatpak.md)
(sekcja „Task 5: Repozytorium Flatpaka dla GitHub Pages”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-26-plan-4-flatpak.md](../../../docs/plany/2026-09-26-plan-4-flatpak.md) — kod, testy i komendy każdego
  kroku.
- Specyfikacja: [WS Tracker Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md); decyzje:
  [0045](../../W-TRAKCIE/0045-plan4-projekt-flatpak/todo.md).
- Pliki:

- Create: `flatpak/pages.py`, `flatpak/publikuj.sh`, `flatpak/klucz-gpg.sh`
- Test: `tests/test_strona_repo.py`

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] Wynik planu: 411 passed, 1 skipped; próba na sucho bez ostrzeżeń GPG.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające)
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Zaimplementuj
- [x] Step 4: Uruchom — mają przejść
- [x] Step 5: Próba na sucho w kontenerze
- [x] Step 6: Commit

## Materiały

- [testy/pytest-2026-09-26.txt](testy/pytest-2026-09-26.txt) — końcowy przebieg:
  `411 passed, 1 skipped, 12 deselected in 2.59s`

## Dziennik

### 2026-09-26

- **11:28** Utworzono zadanie z Planu 4.
- **11:54** Start wykonania.
- **11:55** Zamknięte: 411 passed, 1 skipped, 12 deselected in 2.59s, commity na main.

## Wynik

[pages.py](../../../flatpak/pages.py), [publikuj.sh](../../../flatpak/publikuj.sh),
[klucz-gpg.sh](../../../flatpak/klucz-gpg.sh), testy [test_strona_repo.py](../../../tests/test_strona_repo.py). Próba na
sucho
([log](testy/proba-na-sucho-2026-09-26.log)): podpisane wszystkie refy, instalacja z `.flatpakref` bez ostrzeżeń GPG,
`Nothing to update.`. Odchylenie: kolejność nazw w teście po zmianie nazwy.
