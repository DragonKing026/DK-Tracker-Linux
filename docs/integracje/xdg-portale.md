---
tytul: Portale XDG (autostart, powiadomienia, linki, skróty)
tagi: [integracja, flatpak, portale, dbus]
status_integracji: planowana
wersja: xdg-desktop-portal (Background v2, GlobalShortcuts v2)
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
---

# Portale XDG Desktop

> [!info] W skrócie
> Portale to API D-Bus (`org.freedesktop.portal.*`), przez które aplikacja w piaskownicy
> prosi system o usługi. System (backend KDE/GNOME) może zapytać użytkownika o zgodę.
> Nie wymagają `finish-args`.

## Portale, których potrzebujemy

| Portal | Po co | Funkcja | Priorytet |
|---|---|---|---|
| **Background** | autostart z sesją, zgoda na działanie w tle, status w tle | F-22 | wysoki — aplikacja tackowa |
| **Notification** | powiadomienia (długi timer, błąd połączenia) | F-21 | średni |
| **OpenURI** | otwarcie „Moje czasy” / tokenów API w przeglądarce | F-08 | wysoki |
| **Secret** | klucz główny do szyfrowania tokenu | F-01 | wysoki — [osobny dokument](secret-service.md) |
| **GlobalShortcuts** | globalny skrót start/stop | F-24 | niski |
| **Inhibit** | (opcjonalnie) informacja o wylogowaniu/wyłączeniu przy trwającym timerze | — | niski |

## Background — autostart

([dokumentacja, wersja 2](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.Background.html))

- `RequestBackground(parent_window, options)`:
  - `autostart` (b) — uruchamiaj przy logowaniu,
  - `commandline` (as) — komenda autostartu (domyślnie `Exec` z pliku `.desktop`),
  - `dbus-activatable` (b) — aktywacja przez D-Bus zamiast komendy.
  - Wynik: czy działanie w tle jest dozwolone i czy autostart włączono.
- `SetStatus(message)` (od v2) — krótki (≤ 96 znaków) status aplikacji w tle, np.
  „Timer: 1:22 — Moduł rezerwacji”. KDE/GNOME pokazują go w listach aplikacji w tle.

```mermaid
sequenceDiagram
    actor U as Użytkownik
    participant App as Kimai Tray
    participant P as Portal Background
    U->>App: ustawienia: „Uruchamiaj przy logowaniu” ✓
    App->>P: RequestBackground(autostart=true, commandline=[kimai-tray, --hidden])
    P-->>U: (opcjonalnie) okno zgody systemu
    P-->>App: background=true, autostart=true
    loop co zmianę stanu
        App->>P: SetStatus("Timer: 1:22 — Projekt")
    end
```

> [!tip] Start „do tacki”
> Autostart powinien uruchamiać aplikację z flagą w rodzaju `--hidden` (bez okna),
> ale **tylko gdy jest host tacki** — inaczej pokazać okno
> ([GNOME bez tacki](gnome-appindicator.md)).

## Notification

([dokumentacja](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.Notification.html))

- `AddNotification(id, notification)` / `RemoveNotification(id)`; powiadomienie może mieć
  przyciski akcji (np. „Zatrzymaj timer”), które wracają do aplikacji jako akcje.
- Na maszynie deweloperskiej backend: `plasmanotify` (`kde-portals.conf`).
- Toolkity (Qt/GTK) często używają portalu automatycznie w piaskownicy.

## OpenURI

([dokumentacja](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.OpenURI.html))
— `OpenURI(parent, uri, options)` otwiera link w domyślnej przeglądarce użytkownika.

## GlobalShortcuts

([dokumentacja, wersja 2](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.GlobalShortcuts.html))
— skróty działają oparte o sesję: `CreateSession` → `BindShortcuts` (system zwykle
pokazuje okno konfiguracji skrótu) → sygnały `Activated`/`Deactivated`.

## Stan backendów na maszynie deweloperskiej (2026-09-25)

```text
kde-portals.conf:
  default=kde
  org.freedesktop.impl.portal.Secret=kwallet
  org.freedesktop.impl.portal.Notification=plasmanotify
```

## Pułapki

> [!warning]
> - Obsługa danego portalu zależy od backendu pulpitu i jego wersji — każdą funkcję
>   opartą o portal trzeba mieć z łagodną degradacją (brak portalu → funkcja wyłączona,
>   bez awarii).
> - Autostart spoza piaskownicy (uruchomienie z `cargo run`/`python` w dev) nie przechodzi
>   przez portal tak samo — testować w zbudowanym Flatpaku.

## Dokumentacja

- [XDG Desktop Portal — dokumentacja](https://flatpak.github.io/xdg-desktop-portal/docs/)
- [Flatpak — portale](https://docs.flatpak.org/en/latest/portals.html)
- Linki do poszczególnych portali — w sekcjach powyżej.

## Powiązane

- [Flatpak](flatpak.md)
- [Sekrety](secret-service.md)
- [Katalog funkcji F-20…F-24](../architektura/funkcje.md)
