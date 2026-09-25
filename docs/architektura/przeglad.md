---
noteId: "26c430953cad4545a2234350cf834e0b"
tytul: Przegląd projektu
tags: [architektura, wizja, zakres]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
---

# Przegląd projektu

> [!info] W skrócie
> Natywna aplikacja linuksowa w **tacce systemowej**, dystrybuowana jako **Flatpak**, która
> pozwala mierzyć czas w firmowym **Kimai** jednym kliknięciem — tak jak wtyczka
> przeglądarkowa [WS Tracker](../integracje/kimai-ws-tracker.md), ale bez przeglądarki.

## Problem

Zespół mierzy czas w self-hostowanym Kimai. Wtyczka przeglądarkowa WS Tracker rozwiązuje
to dobrze, ale:

- działa tylko, gdy przeglądarka jest otwarta, i jest przywiązana do jednego profilu,
- licznik na ikonie wtyczki ginie wśród innych rozszerzeń,
- nie ma powiadomień systemowych (np. „timer działa od 9 godzin”),
- nie startuje razem z sesją pulpitu.

Ikona w tacce systemowej jest widoczna zawsze, niezależnie od tego, która aplikacja jest
na pierwszym planie.

## Dla kogo

- **Główny użytkownik**: pracownik Web Systems na Fedorze z **KDE Plasma** (Wayland).
- **Drugorzędnie**: użytkownicy **GNOME** (Fedora Workstation, Ubuntu) i innych pulpitów
  obsługujących StatusNotifierItem (XFCE, Cinnamon, Budgie…).

## Kontekst systemu

```mermaid
flowchart LR
    U([Użytkownik]) -- klik w ikonę / menu --> APP
    subgraph Pulpit Linux
        TRAY[Tacka systemowa<br/>KDE Plasma / GNOME + AppIndicator]
        APP[Kimai Tray<br/>Flatpak]
        SEC[(Magazyn sekretów<br/>KWallet / GNOME Keyring)]
        PORT[Portale XDG<br/>autostart, powiadomienia]
    end
    APP -- StatusNotifierItem D-Bus --> TRAY
    APP -- token API --> SEC
    APP -- Background / Notification --> PORT
    APP -- HTTPS + Bearer token --> KIMAI[(Kimai firmy<br/>REST API)]
```

Szczegóły każdej strzałki: [Integracje](../integracje/README.md).

## Zakres — wersja 1.0 (parytet z wtyczką)

Pełny opis każdej funkcji: [Katalog funkcji](funkcje.md).

- [ ] Konfiguracja: adres Kimai, token API, język, minimalna długość opisu, test połączenia
- [ ] Ikona w tacce: stan (bezczynny / trwa / błąd) i czas trwającego wpisu
- [ ] Okno szybkiej obsługi po kliknięciu ikony (odpowiednik popupu wtyczki)
- [ ] Start / stop timera; wybór projektu (grupowanie po kliencie) i czynności
- [ ] Zapamiętanie ostatniego projektu i czynności
- [ ] Edycja trwającego wpisu: opis, godzina rozpoczęcia, godzina zakończenia, billable
- [ ] Lista ostatnich wpisów pogrupowana po dniach z sumami; wznawianie wpisu
- [ ] Przełącznik billable (z obsługą braku uprawnienia `edit_billable_own_timesheet`)
- [ ] Sumy dzienna i tygodniowa
- [ ] Walidacja jakości opisu (za krótki / zbyt ogólny)
- [ ] Link „Moje czasy” do panelu Kimai
- [ ] Język polski i angielski
- [ ] Menu kontekstowe ikony (prawy klik): stop, wznów ostatni, otwórz Kimai, ustawienia, zakończ
- [ ] Powiadomienia systemowe (długi timer, problemy z połączeniem)
- [ ] Autostart z sesją (opcja w ustawieniach)
- [ ] Paczka Flatpak

## Poza wtyczką — kandydaci na później

Funkcje, które ma sens dodać, bo aplikacja desktopowa może więcej niż wtyczka.
Każda wymaga osobnej decyzji — nie wchodzą do 1.0 automatycznie.

- Wykrywanie bezczynności (idle) i propozycja odjęcia czasu
- Skrót klawiszowy globalny (portal GlobalShortcuts)

## Poza zakresem

- Zarządzanie projektami/klientami/fakturami — to robi panel Kimai.
- Obsługa przestarzałego uwierzytelnienia `X-AUTH-USER`/`X-AUTH-TOKEN` (jak we wtyczce —
  tylko token Bearer).
- Windows / macOS.
- Telemetria.

## Ograniczenia i ryzyka

> [!warning] Wayland a pozycjonowanie okna
> Na Waylandzie aplikacja **nie może sama ustawić pozycji swojego okna**. Okno
> „popupu” nie pojawi się automatycznie tuż przy ikonie w tacce tak jak w przeglądarce —
> o jego położeniu decyduje kompozytor. Menu kontekstowe ikony (renderowane przez hosta
> tacki) nie ma tego problemu. Rozwiązanie: [ADR-0003](../decyzje/0003-okno-szybkiej-obslugi-na-wayland.md).

> [!warning] GNOME nie ma tacki domyślnie
> GNOME Shell nie wyświetla ikon StatusNotifierItem bez rozszerzenia
> [AppIndicator and KStatusNotifierItem Support](../integracje/gnome-appindicator.md).
> Ubuntu ma je domyślnie, Fedora Workstation — nie. Aplikacja musi działać sensownie
> także bez tacki (np. zwykłe okno).

## Kryteria sukcesu

1. Na Fedorze KDE: instalacja z pliku `.flatpak`, konfiguracja w < 2 min, start/stop
   timera w ≤ 2 kliknięciach od ikony w tacce.
2. Na GNOME z rozszerzeniem AppIndicator — to samo; bez rozszerzenia — aplikacja nadal
   używalna jako okno.
3. Wszystkie funkcje z listy „Zakres 1.0” działają tak jak we wtyczce.
4. Token przechowywany wyłącznie w magazynie sekretów systemu.

## Powiązane

- [Katalog funkcji](funkcje.md)
- [Projekt referencyjny: WS Tracker](../integracje/kimai-ws-tracker.md)
- [Decyzje](../decyzje/README.md)
- [Tablica zadań](../../TODO/README.md)
