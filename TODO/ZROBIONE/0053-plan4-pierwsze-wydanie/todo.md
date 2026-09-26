---
noteId: "6de6b49e4f19404bbc64944d98ab24a3"
tytul: "Plan 4 · Zadanie 8: Pierwsze wydanie 0.9.0 (z użytkownikiem)"
numer: "0053"
status: zrobione
priorytet: p1
tags: [todo, plan-4, flatpak]
zalezy_od: ["0052"]
utworzono: 2026-09-26 11:28
zaktualizowano: 2026-09-26 13:36
zamknieto: 2026-09-26 13:36
---

# 0053 — Plan 4 · Zadanie 8: Pierwsze wydanie 0.9.0 (z użytkownikiem)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 8** z [Planu 4: Flatpak i wydanie](../../../docs/plany/2026-09-26-plan-4-flatpak.md)
(sekcja „Task 8: Pierwsze wydanie 0.9.0 (z użytkownikiem)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-26-plan-4-flatpak.md](../../../docs/plany/2026-09-26-plan-4-flatpak.md) — kod, testy i komendy każdego
  kroku.
- Specyfikacja: [WS Tracker Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md); decyzje:
  [0045](../0045-plan4-projekt-flatpak/todo.md).
- Pliki:

- Create: `flatpak/ws-tracker-tray-repo.gpg` (klucz publiczny)
- Modify: `tests/test_pakiet.py`

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] Wynik planu: 414 passed, 1 skipped; wydanie v0.9.0 na GitHubie i Pages; instalacja z repozytorium u użytkownika.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Test klucza (padający)
- [x] Step 2: Klucz
- [x] Step 3: Sekret i Pages — za zgodą użytkownika w tej chwili:
- [x] Step 4: Wypchnięcie i tag — za zgodą:
- [x] Step 5: Instalacja z repozytorium u użytkownika:
- [x] Step 6: Zamknięcie

## Materiały

- Wynik: wydanie v0.9.0 (pre-release), Pages, instalacja z .flatpakref bez ostrzeżeń

## Dziennik

### 2026-09-26

- **11:28** Utworzono zadanie z Planu 4.
- **12:55** Start: pełne wydanie z tymczasowym identyfikatorem (decyzja użytkownika, 0056).
- **13:36** Zamknięte: wydanie v0.9.0 (pre-release), Pages, instalacja z .flatpakref bez ostrzeżeń, commity na main.

## Wynik

Wydanie [v0.9.0](https://github.com/DragonKing026/Kimai-App--Linux-/releases/tag/v0.9.0) (pre-release, paczka 71 MB),
repozytorium
Flatpaka na [Pages](https://dragonking026.github.io/Kimai-App--Linux-/) podpisane kluczem `955CDDB9…A41D` (sekret
`FLATPAK_GPG_PRIVATE_KEY`, plik prywatny zniszczony), środowisko `github-pages` z regułą tagów `v*`. U użytkownika:
instalacja z `.flatpakref` bez ostrzeżeń, źródło `ws-tracker-tray`, `flatpak update` → brak aktualizacji; aplikacja
działa (test na żywo, zgłoszenia → [0058](../0058-dlugie-opisy-na-liscie/todo.md)). Wydanie z tymczasowym
identyfikatorem — decyzja w [0056](../../W-TRAKCIE/0056-identyfikator-i-wydawca/todo.md).
