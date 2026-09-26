---
noteId: "aa8a9939ba774ea799dcaff6f7e999f8"
tytul: "Plan 4 — projekt paczki Flatpak (decyzje przed planem)"
numer: "0045"
status: zrobione
priorytet: p1
tags: [todo, plan-4, flatpak, projekt]
zalezy_od: ["0044"]
utworzono: 2026-09-26 10:19
zaktualizowano: 2026-09-26 13:36
zamknieto: 2026-09-26 13:36
---

# 0045 — Plan 4 — projekt paczki Flatpak (decyzje przed planem)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Rozstrzygnąć z użytkownikiem decyzje, których nie zamyka
[specyfikacja](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md),
a potem napisać Plan 4 (Flatpak i wydanie).

## Kontekst

- Ustalone: paczka `.flatpak` (specyfikacja, kryteria akceptacji), `org.kde.Platform` 6.11 + `io.qt.PySide.BaseApp`
  ([ADR-0002](../../../docs/decyzje/0002-stos-python-pyside6.md)), uprawnienia (specyfikacja, sekcja 8), budowa w
  kontenerze
  ([ADR-0006](../../../docs/decyzje/0006-budowanie-flatpaka-w-kontenerze.md)), integracja
  [Flatpak](../../../docs/integracje/flatpak.md).

## Kryteria akceptacji

- [x] Każda otwarta decyzja rozstrzygnięta i zapisana
- [x] Plan 4 napisany, zweryfikowany i zaakceptowany przez użytkownika

## Decyzje

- [x] **Licencja:** AGPL-3.0-or-later (jak Kimai; logo Kimai może zostać). Plik `LICENSE` i pole licencji w
  `pyproject.toml` i MetaInfo — w Planie 4.
- [x] **Dystrybucja:** wariant C — plik `.flatpak` budowany lokalnie (`flatpak/buduj.sh`, Docker) **i** przez
  GitHub Actions po tagu wersji (wydanie na GitHubie z paczką), **plus** własne repozytorium Flatpaka na GitHub Pages
  (podpisane GPG) z automatycznymi aktualizacjami przez Discover / GNOME Software.
- [x] **Repozytorium kodu publiczne** (`DragonKing026/Kimai-App--Linux-`) — użytkownik zmienił widoczność; Pages działa
  na darmowym koncie. Wypychanie, tagi i sekrety tylko na prośbę użytkownika.
- [x] **Nazwa:** „Kimai Tray” zostaje nazwą docelową (identyfikator `pl.websystems.KimaiTray`).
- [x] **Zmiana nazwy (2026-09-26 11:45):** „WS Tracker Tray”, identyfikator `pl.websystems.WsTrackerTray`, bo
  „Kimai Tray” zlewa się z [KimaiTray](../../../docs/architektura/podobne-aplikacje.md); zadanie
  [0055](../0055-zmiana-nazwy-ws-tracker-tray/todo.md).
- [x] **Pierwsza wersja:** 0.9.0 (beta) — 1.0.0 po testach na GNOME
      ([0020](../../DO-ZROBIENIA/0020-testy-gnome/todo.md)).

## Materiały

- Wynik: Plan 4 wykonany, wydania 0.9.0 i 0.9.1

## Dziennik

### 2026-09-26

- **10:19** Utworzono. Licencja: AGPL-3.0-or-later (decyzja użytkownika).
- **10:23** Dystrybucja: wariant C (paczka + Actions + repozytorium na Pages); repozytorium publiczne.
- **10:24** Nazwa: Kimai Tray; wersja 0.9.0 (beta).
- **11:01** Próba budowy w obrazie Flathuba udana (71 MB); test paczki z użytkownikiem: wszystko działa.
- **11:24** Plan 4 napisany ([plan](../../../docs/plany/2026-09-26-plan-4-flatpak.md)); kod z planu w świeżej kopii: 411
  testów + test klucza (zadanie 8), `actionlint` i shellcheck czyste, próba publikacji z podpisem w kontenerze udana.
  Czeka na akceptację.
- **13:36** Zamknięte: Plan 4 wykonany, wydania 0.9.0 i 0.9.1, commity na main.
