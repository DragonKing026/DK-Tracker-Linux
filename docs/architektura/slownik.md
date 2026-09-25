---
tytul: Słownik pojęć
tagi: [architektura, slownik]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
---

# Słownik pojęć

| Pojęcie | Znaczenie |
|---|---|
| **Kimai** | Open-source'owy system rejestracji czasu pracy (PHP/Symfony), u nas self-hostowany. [[docs/integracje/kimai-api\|Kimai API]] |
| **Wpis / timesheet** | Jeden odcinek czasu w Kimai: początek, koniec, projekt, czynność, opis, billable. |
| **Trwający wpis** | Wpis bez `end` — „włączony timer”. Kimai zwraca go z `/api/timesheets/active`. |
| **Klient (customer)** | Najwyższy poziom hierarchii Kimai: klient → projekt → czynność. |
| **Projekt** | Należy do klienta; ma kolor, flagę billable, opcjonalne okno dat. |
| **Czynność (activity)** | Rodzaj pracy; globalna albo przypisana do projektu. |
| **Billable** | Czy czas trafia na fakturę klienta. Domyślnie wynika z flag klienta, projektu i czynności. |
| **Token API** | Osobisty token Bearer tworzony w Kimai: Profil → API. Pokazywany tylko raz. |
| **WS Tracker** | Wtyczka przeglądarkowa Web Systems — wzorzec funkcjonalny tej aplikacji. [[docs/integracje/kimai-ws-tracker\|opis]] |
| **Tacka systemowa (system tray)** | Obszar ikon aplikacji działających w tle na panelu pulpitu. |
| **SNI / StatusNotifierItem** | Standard freedesktop (z KDE) ikon w tacce przez D-Bus. Następca XEmbed. [[docs/integracje/statusnotifieritem\|opis]] |
| **AppIndicator** | Wariant SNI od Canonical (libappindicator / libayatana-appindicator). |
| **Flatpak** | Format dystrybucji aplikacji linuksowych w piaskownicy. [[docs/integracje/flatpak\|opis]] |
| **Runtime / SDK** | Wspólna baza bibliotek Flatpaka (np. `org.kde.Platform`, `org.gnome.Platform`). |
| **finish-args** | Uprawnienia piaskownicy Flatpaka zadeklarowane w manifeście. |
| **Portal (XDG Desktop Portal)** | API D-Bus, przez które aplikacja w piaskownicy prosi system o usługi (autostart, powiadomienia, sekrety). [[docs/integracje/xdg-portale\|opis]] |
| **Secret Service** | Standard freedesktop przechowywania haseł (GNOME Keyring, KWallet). [[docs/integracje/secret-service\|opis]] |
| **Wayland** | Protokół wyświetlania; m.in. nie pozwala aplikacji ustawiać pozycji własnych okien. |
| **ADR** | Architecture Decision Record — zapis decyzji w `docs/decyzje/`. |
| **MOC** | Map of Content — strona-indeks w Obsidianie. |
