---
noteId: "65c8faaefb604512b64a50e1133bf0d7"
tytul: Podobne aplikacje — KimaiTray i KimTrack
tags: [architektura, konkurencja, funkcje, porownanie]
utworzono: 2026-09-26 11:42
zaktualizowano: 2026-09-26 11:42
---

# Podobne aplikacje

Inne aplikacje tackowe dla Kimai, co je od nas odróżnia i co warto od nich przejąć. Stan na 2026-09-26 11:42,
sprawdzony w kodzie źródłowym KimaiTray (klon repozytorium) i na stronach wydań. Zadanie:
[0054](../../TODO/W-TRAKCIE/0054-podobne-aplikacje/todo.md).

## KimaiTray (Engazan)

- Repozytorium: [Engazan/KimaiTray](https://github.com/Engazan/KimaiTray), wpis w
  [sklepie Kimai](https://www.kimai.org/en/store/engazan-kimaitray.html).
- Licencja **MIT**, kod otwarty. Tauri 2 (Rust) + React 19 + TypeScript (interfejs w WebKitGTK).
- Od 2026-05-18, ok. 350 commitów, wersja 0.22.11 (2026-09-15), jeden główny autor; przyjmuje pull requesty z zewnątrz
  (m.in. poprawki Waylanda i sway).
- Paczki: **deb, rpm, AppImage** (podpisane), Windows, macOS; własny updater z GitHub Releases. Bez Flatpaka i Snapa.
- Identyfikator `eu.engazan.kimaitray`. Języki: EN, SK, CS, DE, UK — **bez polskiego**.

### Ograniczenia na KDE/Wayland (z kodu)

- Tacka przez `libappindicator`: **lewy i prawy klik otwierają menu**, okno otwiera **środkowy klik**
  (README, „Wayland AppIndicator”).
- Na Waylandzie wyłączone: pozycjonowanie okna, „zawsze na wierzchu”, skróty globalne
  (`src-tauri/src/platform.rs`: `supports_window_positioning = !is_wayland()`).
- Czas pomiaru jako napis przy ikonie tylko na macOS; na Linuksie tooltip i kolor/kształt ikony
  (`src-tauri/src/tray/ticker.rs`).

## KimTrack (Playmoweb)

- Strona: [playmoweb/kimtrack](https://github.com/playmoweb/kimtrack),
  [sklep Kimai](https://www.kimai.org/en/store/playmoweb-kimtrack.html).
- **Zamknięty kod, płatna licencja** ze sklepu Kimai; repozytorium służy tylko do wydań i zgłoszeń.
- Paczki: deb, rpm (x86_64, aarch64), Windows, macOS. Wersja 1.2.5 (2026-07-08).
- Funkcje według opisu: start/stop jednym kliknięciem, wykrywanie bezczynności, serwer MCP dla agentów AI.
  Kodu nie da się sprawdzić, więc dalej porównujemy się głównie z KimaiTray.

## Porównanie z naszą aplikacją

| | KimaiTray | Nasza aplikacja |
| --- | --- | --- |
| Licencja | MIT | AGPL-3.0-or-later |
| Technologia | Tauri + React (WebKitGTK) | Python + Qt 6 (natywnie w KDE) |
| Systemy | Linux, Windows, macOS | Linux (KDE, GNOME) |
| Paczki | deb, rpm, AppImage | Flatpak (sandbox) z repozytorium na GitHub Pages |
| Języki | EN, SK, CS, DE, UK | PL, EN |
| Otwarcie okna na KDE/Wayland | środkowy klik, okno w dowolnym miejscu | lewy klik, okno przy ikonie (layer-shell) |
| Czas w tacce na Linuksie | tylko tooltip | cyfry w ikonie |
| Walidacja jakości opisu | brak | tak ([F-11](funkcje.md#f-11-walidacja-jakości-opisu)) |
| Suma tygodniowa | brak (suma dnia, cel dzienny) | tak ([F-12](funkcje.md#f-12-sumy-dzienna-i-tygodniowa)) |
| Przypomnienie o długim timerze | brak | powiadomienie z „Zatrzymaj” / „Nie zatrzymuj” |
| Pauza, wiele timerów | tak | nie |
| Wiele kont Kimai | tak | nie |
| Integracje z trackerami zadań | GitLab, GitHub, Gitea | nie |

Nasza przewaga jest wąska, ale konkretna: wygoda na KDE/Wayland, zasady wtyczki
[kimai-ws-tracker](../integracje/kimai-ws-tracker.md) i język polski. W liczbie funkcji KimaiTray jest daleko przed
nami.

## Co warto przejąć

Kandydaci na funkcje po 1.0, w kolejności od najbardziej przydatnych. Numery F-25… to nowe pozycje w
[katalogu funkcji](funkcje.md#funkcje-nowe-względem-wtyczki-kandydaci).

| Id | Pomysł (jak w KimaiTray) | Ocena dla nas |
| --- | --- | --- |
| F-25 | **Przypomnienie, gdy żaden timer nie działa** — po N minutach bez pomiaru (u nich domyślnie 15) | tanie: warunek w `notification_policy`, powiadomienie portalu zamiast pełnego ekranu; warto ograniczyć do godzin pracy |
| F-23 | **Wykrywanie bezczynności** — u nich na KDE/Wayland przez `org.kde.KWin` `/org/kde/KIdleTime` `idleTime` | wykonalne, ale w Flatpaku wymaga `--talk-name=org.kde.KWin` (szerokie uprawnienie) i nie działa na GNOME bez osobnej ścieżki (Mutter IdleMonitor) |
| F-24 | **Skróty globalne** (okno, start/stop, wznów ostatni) | u nich wyłączone na Waylandzie; my możemy przez portal GlobalShortcuts, który KDE obsługuje — przewaga nad nimi |
| F-26 | **Ulubione zadania** — przypięte pozycje obok ostatnich wpisów | niewielka zmiana w `Memory` i liście w oknie |
| F-27 | **Oś czasu dnia** — dzisiejsze wpisy z czasami i billable | mamy dane z listy ostatnich; nowy widok w oknie |
| F-28 | **Cel dzienny** — ile zostało do normy i szacowana godzina końca | proste obliczenie na sumie dnia (F-12) |
| F-29 | **Tagi przy starcie i edycji** | API Kimai je ma; zależy, czy firma używa tagów |
| F-30 | **Własna godzina startu nowego wpisu** | edycję początku trwającego wpisu już mamy (F-07); tu to samo przy starcie |
| F-31 | **Linki `…://start` z przeglądarki** (np. przycisk przy zadaniu w GitLabie) | ciekawe dla firmy; w Flatpaku przez `.desktop` z `MimeType=x-scheme-handler/…` |
| F-32 | **Ekran „Co nowego”** po aktualizacji | lista zmian mamy w MetaInfo; pokazać raz po zmianie wersji |

Świadomie **nie** przejmujemy:

- wielu kont Kimai (jedno firmowe konto wystarcza);
- integracji z GitLab, GitHub i Gitea (duży zakres, osobne tokeny);
- własnych motywów, układów i skalowania (trzymamy się motywu systemu, decyzja z
  [0028](../../TODO/ZROBIONE/0028-plan3-projekt-ui/todo.md));
- własnego updatera (aktualizacje daje Flatpak).

## Wnioski

- Nazwa „Kimai Tray” zlewa się z „KimaiTray”, więc zmieniamy ją przed wydaniem 0.9.0.
- Polskie tłumaczenie możemy też wysłać do KimaiTray jako pull request; nic nas to nie kosztuje.

## Powiązane

- [Katalog funkcji](funkcje.md)
- [Przegląd projektu](przeglad.md)
- [Specyfikacja 1.0](../specyfikacja/2026-09-25-kimai-tray-1.0.md)
