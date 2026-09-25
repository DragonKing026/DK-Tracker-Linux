---
noteId: "88803f062d77411790e9a0c0cbd856bd"
tytul: Stos technologiczny — Python + PySide6 (Qt 6) na runtime KDE
tags: [adr, stos, qt, python, flatpak]
status: zaakceptowana
zastapiona_przez:
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
---

# ADR-0002: Python + PySide6 (Qt 6) na runtime KDE

## Kontekst

Aplikacja ma siedzieć w tacce systemowej KDE Plasma (priorytet) i GNOME (z rozszerzeniem
AppIndicator), otwierać okno po **lewym** kliknięciu ikony, być pakowana jako Flatpak
i odtworzyć logikę wtyczki WS Tracker (JavaScript) — najlepiej z testami.
Wymagania szczegółowe: [zadanie 0003](../../TODO/DONE/0003-wybor-stosu/todo.md).

## Rozważane opcje

| Opcja | Zalety | Wady |
|---|---|---|
| **Python + PySide6** | `QSystemTrayIcon` działa przez SNI w KDE, GNOME, Xfce, LXQt; sygnał `activated` z powodem (Trigger/Context/DoubleClick/MiddleClick); gotowa baza Flatpak `io.qt.PySide.BaseApp`; szybki rozwój; łatwe przeniesienie logiki JS z testami (pytest, pytest-qt) | interpreter w paczce (runtime KDE i tak go ma); typowanie tylko przez mypy |
| C++ / QML + KDE Frameworks | najbardziej natywne dla KDE, `KStatusNotifierItem` z pełnym API SNI | dużo więcej kodu, wolniejszy rozwój |
| Tauri 2 (Rust + web) | można użyć HTML/CSS/JS wtyczki | **zdarzenia kliknięcia ikony nie działają na Linuksie** (dokumentacja Tauri) — lewy klik nie otworzy okna |
| GTK4 / libadwaita | natywne w GNOME | GTK4 nie ma API tacki — trzeba samodzielnie pisać SNI przez D-Bus |

## Decyzja

**Piszemy w Pythonie z PySide6 (Qt 6), pakujemy jako Flatpak na `org.kde.Platform`
z bazą `io.qt.PySide.BaseApp` (gałąź 6.11).**

Zaakceptowane przez użytkownika 2026-09-25.

## Uzasadnienie

- Qt oficjalnie deklaruje obsługę SNI we wszystkich pulpitach, które jej potrzebujemy
  ([QSystemTrayIcon](https://doc.qt.io/qt-6/qsystemtrayicon.html)), a KDE jest
  głównym środowiskiem użytkownika.
- Lewy klik (`QSystemTrayIcon.ActivationReason.Trigger`) jest dostępny, co w Tauri odpada.
- Baza Flatpak jest utrzymywana na Flathubie, więc nie budujemy PySide6 sami.
- Lokalnie są już PySide6 6.11.2, Python 3.14.7 i runtime `org.kde.Platform` 6.10/6.11.

## Konsekwencje

- Runtime: `org.kde.Platform//6.11`, SDK `org.kde.Sdk//6.11`, baza `io.qt.PySide.BaseApp//6.11`.
  Manifest musi zawierać `cleanup-commands: [/app/cleanup-BaseApp.sh]`; warto ustawić
  `BASEAPP_REMOVE_WEBENGINE`, bo WebEngine nie jest nam potrzebny.
- Qt dokumentuje, że w GNOME ≥ 3.26 bez rozszerzeń nie wszystkie `ActivationReason`
  są obsługiwane. To wymaga sprawdzenia w [prototypie](../../TODO/0004-prototyp-tacki-i-okna/todo.md).
- Tooltip przez `QHelpEvent` i kółko myszy działają tylko na X11. Na Waylandzie tooltip
  ustawiamy właściwością `toolTip` (SNI), bez zdarzeń.
- Do ustalenia osobno: UI w Qt Widgets czy QML, klient HTTP (np. `QNetworkAccessManager`
  albo `httpx`), dostęp do sekretów (np. `QtKeychain` / `secretstorage` / libsecret).
- `layer-shell-qt` (pozycjonowanie okien na Waylandzie w KDE) **nie jest** w runtime
  `org.kde.Platform` 6.10/6.11 (sprawdzone lokalnie). Użycie go wymagałoby osobnego
  modułu w manifeście.

## Powiązane

- [Qt / PySide6](../integracje/qt-pyside6.md)
- [Flatpak](../integracje/flatpak.md)
- [StatusNotifierItem](../integracje/statusnotifieritem.md)
