---
tytul: Integracje — indeks
tagi: [integracja, indeks]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
---

# Integracje

Każda zewnętrzna zależność ma tu osobny plik z faktami ze źródeł i linkami do oficjalnej
dokumentacji. Nową dodajesz skillem `nowa-integracja`.

```mermaid
flowchart LR
    APP((Kimai Tray))
    APP --> K[Kimai REST API]
    APP --> SNI[StatusNotifierItem]
    SNI --> GN[GNOME AppIndicator]
    APP --> SEC[Secret Service / portal Secret]
    APP --> POR[Portale XDG]
    APP --> FP[Flatpak]
    APP --> QT[Qt 6 / PySide6]
    QT --> SNI
    REF[WS Tracker<br/>wzorzec] -. inspiracja .-> APP
```

| Integracja | Rola | Status | Dokument |
|---|---|---|---|
| Kimai REST API | źródło danych | planowana | [kimai-api](kimai-api.md) |
| WS Tracker | projekt referencyjny (wzorzec funkcji i UI) | referencja | [kimai-ws-tracker](kimai-ws-tracker.md) |
| StatusNotifierItem | ikona w tacce przez D-Bus | planowana | [statusnotifieritem](statusnotifieritem.md) |
| GNOME AppIndicator | host tacki w GNOME | planowana | [gnome-appindicator](gnome-appindicator.md) |
| Secret Service / portal Secret | przechowywanie tokenu | planowana | [secret-service](secret-service.md) |
| Portale XDG | autostart, powiadomienia, linki, skróty | planowana | [xdg-portale](xdg-portale.md) |
| Flatpak | budowanie i dystrybucja | planowana | [flatpak](flatpak.md) |
| Qt 6 / PySide6 | UI, tacka, pętla zdarzeń | w użyciu ([ADR-0002](../decyzje/0002-stos-python-pyside6.md)) | [qt-pyside6](qt-pyside6.md) |

> [!todo] Do dopisania
> Biblioteka HTTP i biblioteka sekretów, gdy zostaną wybrane.
