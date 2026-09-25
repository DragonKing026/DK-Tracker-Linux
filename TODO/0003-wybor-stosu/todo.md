---
tytul: "Wybór stosu technologicznego"
numer: "0003"
status: do-zrobienia
priorytet: p0
tagi: [todo, planowanie, adr]
zalezy_od: []
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
zamknieto:
---

# 0003 — Wybór stosu technologicznego

> [!info] Status
> **do-zrobienia** · priorytet **p0** · [[TODO/README|← tablica zadań]]

## Cel

Wybrać język, toolkit UI, sposób realizacji tacki i runtime Flatpaka, zapisać jako ADR.

## Kontekst

Wymagania wynikające z dokumentacji:
- ikona SNI działająca w Plasmie 6 (Wayland) i w GNOME z AppIndicator
  ([[docs/integracje/statusnotifieritem|SNI]]),
- okno szybkiej obsługi mimo braku pozycjonowania na Waylandzie,
- sekrety przez portal/Secret Service ([[docs/integracje/secret-service|sekrety]]),
- paczka Flatpak z minimalnymi `finish-args` ([[docs/integracje/flatpak|Flatpak]]),
- możliwie duże przeniesienie logiki wtyczki (JS) — albo przepisanie z testami.

Wstępni kandydaci (do porównania w ADR):

| Kandydat | Tray | Runtime | Uwagi |
|---|---|---|---|
| Python + PySide6 (Qt 6) | `QSystemTrayIcon` (SNI) | `org.kde.Platform` + PySide BaseApp | natywne w KDE, szybki rozwój |
| C++ / QML + KDE Frameworks | `KStatusNotifierItem` | `org.kde.Platform` | najbardziej „KDE”, więcej kodu |
| Tauri 2 (Rust + web) | libayatana-appindicator | `org.gnome.Platform` / Freedesktop | reużycie HTML/CSS/JS wtyczki |
| Python/Rust + GTK4/libadwaita | własny SNI przez D-Bus | `org.gnome.Platform` | GTK4 nie ma API tacki |

> [!todo] Każdą opcję zweryfikować przez Context7/dokumentację przed ADR.

## Kryteria akceptacji

- [ ] Porównanie opcji ze źródłami
- [ ] ADR `docs/decyzje/0002-*.md` zaakceptowany przez użytkownika
- [ ] Dokumenty integracji dla wybranych bibliotek
- [ ] Sekcja „Komendy” w `AGENTS.md` uzupełniona

## Dziennik

### 2026-09-25
- Utworzono zadanie z wstępną listą kandydatów.

## Wynik
