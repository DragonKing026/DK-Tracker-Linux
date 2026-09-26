# WS Tracker Tray

Mierzenie czasu w [Kimai](https://www.kimai.org/) prosto z tacki systemowej Linuksa — bez otwierania przeglądarki.
Natywny odpowiednik firmowej wtyczki [WS Tracker](https://github.com/websystemspl/kimai-ws-tracker).

![Okno WS Tracker Tray przy tacce (ciemny motyw)](../docs/assets/zrzuty/okno-ciemny-motyw.png)

> **Status:** wersja **0.9.0 (beta)** — sprawdzona na KDE Plasma 6 (Wayland). GNOME: testy w toku.

## Co potrafi

- ikona w tacce z czasem trwającego wpisu (`47m`, `1:22`), menu: zatrzymaj, wznów ostatni, ustawienia;
- okno przy ikonie: opis, projekt (z wyszukiwaniem), rodzaj pracy, płatne / niepłatne, godziny „od / do”;
- ostatnie wpisy pogrupowane po dniach, wznawianie jednym kliknięciem, sumy dnia i tygodnia;
- wyszukiwanie we wszystkich swoich wpisach w Kimai (po opisie), długie opisy rozwijane kliknięciem;
- zmiana projektu i rodzaju pracy trwającego wpisu (wtyczka tego nie pozwala);
- przypomnienie o długim timerze, powiadomienia o utracie połączenia;
- token API w portfelu systemu (KWallet / GNOME Keyring), autostart, wersja polska i angielska.

## Instalacja

Aplikacja jest dystrybuowana jako [Flatpak](https://flatpak.org/). Instalacja z repozytorium — aktualizacje przyjdą
same (Discover, GNOME Software, `flatpak update`):

```bash
flatpak install --user https://dragonking026.github.io/Kimai-App--Linux-/pl.websystems.WsTrackerTray.flatpakref
```

Plik `.flatpak` jest też w [najnowszym wydaniu](https://github.com/DragonKing026/Kimai-App--Linux-/releases/latest),
ale tak zainstalowana aplikacja nie dostaje aktualizacji. Szczegóły i przejście z pliku na repozytorium:
[wydania i instalacja](../docs/procesy/wydania.md).

Na GNOME ikona w tacce wymaga rozszerzenia
[AppIndicator and KStatusNotifierItem Support](https://extensions.gnome.org/extension/615/appindicator-support/);
bez niego WS Tracker Tray działa jako zwykłe okno.

## Konfiguracja

1. Kliknij ikonę w tacce → **Otwórz ustawienia**.
2. Podaj adres Kimai i **token API** (Kimai: Profil → API — to nie jest hasło do logowania).
3. **Sprawdź połączenie**, potem **Zapisz**.

## Dokumentacja i rozwój

- [Indeks dokumentacji](../docs/README.md) · [specyfikacja 1.0](../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md) ·
  [plany](../docs/plany/README.md) · [zadania](../TODO/README.md)
- Zasady pracy (także dla agentów AI): [AGENTS.md](../AGENTS.md)
- Stos: Python 3.13, PySide6 (Qt 6), Flatpak na `org.kde.Platform` 6.11

## Licencja

[AGPL-3.0-or-later](../LICENSE) — jak Kimai. Logo Kimai pochodzi z projektu [Kimai](https://github.com/kimai/kimai).
