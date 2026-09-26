---
noteId: "709e67ca60b943a3b5e9e3e23a96ecd7"
tytul: "Identyfikator aplikacji i wydawca — firma czy prywatnie"
numer: "0056"
status: w-trakcie
priorytet: p1
tags: [todo, decyzja, flatpak, wydanie]
zalezy_od: ["0055"]
utworzono: 2026-09-26 12:22
zaktualizowano: 2026-09-26 14:25
zamknieto:
---

# 0056 — Identyfikator aplikacji i wydawca — firma czy prywatnie

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Ustalić przed pierwszym publicznym wydaniem ([0053](../../ZROBIONE/0053-plan4-pierwsze-wydanie/todo.md))
identyfikator aplikacji i wydawcę w MetaInfo. Po wydaniu zmiana identyfikatora oznacza dla każdego ponowną instalację i
utratę ustawień (`~/.var/app/<id>`) oraz tokenu w portfelu.

## Kontekst

- Końcowa recenzja Planu 4: obecny `pl.websystems.WsTrackerTray` to odwrócona domena `websystems.pl` — **innej
  firmy**. Domena Web Systems to `web-systems.pl` → prefiks `pl.web_systems` (myślnik zamienia się na podkreślnik).
- Identyfikator jest w: nazwie Flatpaka i repozytorium aktualizacji, `~/.var/app`, `.desktop`, ikonie, autostarcie,
  źródle powiadomień, wpisie tokenu w portfelu (`application=<id>`).
- Weryfikacja na Flathubie ([dokumentacja](https://docs.flathub.org/docs/for-app-authors/verification)) potrzebna tylko
  przy publikacji tam: dla domeny firmy — token w
  `https://web-systems.pl/.well-known/org.flathub.VerifiedApps.txt`; dla `io.github.*` — logowanie kontem GitHub.
  Własne repozytorium na GitHub Pages
  ([ADR-0007](../../../docs/decyzje/0007-dystrybucja-repozytorium-flatpak-na-github-pages.md))
  weryfikacji nie wymaga.

| Wariant | Identyfikator | Wydawca w MetaInfo |
| --- | --- | --- |
| Firma | `pl.web_systems.WsTrackerTray` | Web Systems |
| Prywatnie | `io.github.dragonking026.WsTrackerTray` | autor (DragonKing026) |

**Blokada:** użytkownik zapytał właściciela firmy (2026-09-26 12:22), czy aplikacja ma być firmowa, czy prywatna.

## Kryteria akceptacji

- [ ] Decyzja właściciela firmy zapisana w dzienniku
- [ ] Identyfikator i `<developer>` w MetaInfo zmienione w kodzie, danych, testach i dokumentacji (jak w
  [0055](../../ZROBIONE/0055-zmiana-nazwy-ws-tracker-tray/todo.md))
- [ ] Budowa (`flatpak/buduj.sh`) i testy zielone

## Kroki

- [ ] Czekać na odpowiedź właściciela firmy
- [ ] Zmienić identyfikator i wydawcę
- [ ] Odblokować [0053](../../ZROBIONE/0053-plan4-pierwsze-wydanie/todo.md)

## Materiały

Brak.

## Dziennik

### 2026-09-26

- **12:22** Utworzono po końcowej recenzji Planu 4; zablokowane do decyzji właściciela firmy.
- **12:55** Użytkownik: pełne wydanie 0.9.0 **teraz** z tymczasowym identyfikatorem `pl.websystems.WsTrackerTray`
  (świadomie: po zmianie identyfikatora instalacje trzeba będzie odinstalować i zainstalować od nowa, z nowym tokenem).
  Wydanie 0053 już na to nie czeka; zmiana identyfikatora wyjdzie w kolejnej wersji.
- **14:25** Decyzja właściciela firmy: projekt prywatny użytkownika. Użytkownik: identyfikator
  io.github.dragonking026.WS-Tracker-Linux (Flathub: ostatni człon = nazwa repozytorium), wydawca Artur Ograbek, pakiet
  ws_tracker i komenda ws-tracker.
- **14:30** Użytkownik: inicjały autora zamiast WS — nazwa **DK Tracker**, repozytorium `DK-Tracker-Linux`,
  identyfikator `io.github.dragonking026.DK-Tracker-Linux`, pakiet `dk_tracker`, komenda `dk-tracker`, ikona „DK”.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
