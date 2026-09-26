---
noteId: "aa8a9939ba774ea799dcaff6f7e999f8"
tytul: "Plan 4 — projekt paczki Flatpak (decyzje przed planem)"
numer: "0045"
status: w-trakcie
priorytet: p1
tags: [todo, plan-4, flatpak, projekt]
zalezy_od: ["0044"]
utworzono: 2026-09-26 10:19
zaktualizowano: 2026-09-26 10:24
---

# 0045 — Plan 4 — projekt paczki Flatpak (decyzje przed planem)

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

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

- [ ] Każda otwarta decyzja rozstrzygnięta i zapisana
- [ ] Plan 4 napisany, zweryfikowany i zaakceptowany przez użytkownika

## Decyzje

- [x] **Licencja:** AGPL-3.0-or-later (jak Kimai; logo Kimai może zostać). Plik `LICENSE` i pole licencji w
  `pyproject.toml` i MetaInfo — w Planie 4.
- [x] **Dystrybucja:** wariant C — plik `.flatpak` budowany lokalnie (`flatpak/buduj.sh`, Docker) **i** przez
  GitHub Actions po tagu wersji (wydanie na GitHubie z paczką), **plus** własne repozytorium Flatpaka na GitHub Pages
  (podpisane GPG) z automatycznymi aktualizacjami przez Discover / GNOME Software.
- [x] **Repozytorium kodu publiczne** (`DragonKing026/Kimai-App--Linux-`) — użytkownik zmienił widoczność; Pages działa
  na darmowym koncie. Wypychanie, tagi i sekrety tylko na prośbę użytkownika.
- [x] **Nazwa:** „Kimai Tray” zostaje nazwą docelową (identyfikator `pl.websystems.KimaiTray`).
- [x] **Pierwsza wersja:** 0.9.0 (beta) — 1.0.0 po testach na GNOME
      ([0020](../../DO-ZROBIENIA/0020-testy-gnome/todo.md)).

## Materiały

## Dziennik

### 2026-09-26

- **10:19** Utworzono. Licencja: AGPL-3.0-or-later (decyzja użytkownika).
- **10:23** Dystrybucja: wariant C (paczka + Actions + repozytorium na Pages); repozytorium publiczne.
- **10:24** Nazwa: Kimai Tray; wersja 0.9.0 (beta).
