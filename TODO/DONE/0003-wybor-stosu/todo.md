---
tytul: "Wybór stosu technologicznego"
numer: "0003"
status: zrobione
priorytet: p0
tagi: [todo, planowanie, adr]
zalezy_od: []
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
zamknieto: 2026-09-25
---

# 0003 — Wybór stosu technologicznego

> [!info] Status
> **zrobione** · priorytet **p0** · [[TODO/README|← tablica zadań]]

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

> [!warning] Ustalone: Tauri na Linuksie nie obsługuje kliknięcia ikony w tacce
> Według dokumentacji Tauri typ `TrayIconEvent` (Click, DoubleClick, Enter, Move, Leave)
> jest oznaczony „unsupported on Linux”; `setShowMenuOnLeftClick` również.
> Na Linuksie działa tylko menu ikony, więc lewy klik nie otworzy okna jak we wtyczce.
> Źródła: [namespace tray](https://tauri.app/reference/javascript/api/namespacetray),
> [TrayIconConfig](https://tauri.app/reference/config).

## Kryteria akceptacji

- [x] Porównanie opcji ze źródłami
- [x] ADR `docs/decyzje/0002-*.md` zaakceptowany przez użytkownika
- [x] Dokumenty integracji dla wybranych bibliotek (Qt/PySide6; HTTP i sekrety — przy wyborze tych bibliotek)
- [ ] ~~Sekcja „Komendy” w `AGENTS.md` uzupełniona~~ → przeniesione do zadania 0002 (wymaga szkieletu projektu)

## Dziennik

### 2026-09-25
- Utworzono zadanie z wstępną listą kandydatów.
- Context7: w Tauri 2 zdarzenia kliknięcia tacki nie działają na Linuksie, co jest poważnym minusem tej opcji.
- Użytkownik zaakceptował rekomendację: Python + PySide6.
- Zweryfikowano: dokumentacja QSystemTrayIcon (SNI w KDE/GNOME/Xfce/LXQt, ograniczenia
  GNOME ≥ 3.26 i X11), baza Flatpak io.qt.PySide.BaseApp 6.11, lokalnie PySide6 6.11.2,
  Python 3.14.7, runtime KDE 6.10/6.11 bez layer-shell-qt.

## Wynik

- Decyzja: [[docs/decyzje/0002-stos-python-pyside6|ADR-0002 — Python + PySide6 na runtime KDE]].
- Integracja: [[docs/integracje/qt-pyside6|Qt 6 / PySide6]].
- Na później: UI w Widgets czy QML, biblioteka HTTP, biblioteka sekretów, forma okna na
  Waylandzie — w specyfikacji ([[TODO/0002-specyfikacja-projektu/todo|0002]]); sekcja
  „Komendy” w `AGENTS.md` — przy szkielecie projektu.
