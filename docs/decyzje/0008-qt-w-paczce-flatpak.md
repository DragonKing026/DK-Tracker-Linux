---
noteId: "67dcc934441b48d08f3fb311150d919d"
tytul: Qt dołączone do paczki Flatpak
tags: [adr, flatpak, qt, pyside6]
status: zaakceptowana
zastapiona_przez:
utworzono: 2026-11-20 10:29
zaktualizowano: 2026-11-20 10:29
---

# ADR-0008: Qt w paczce — PySide6 z PyPI na `org.freedesktop.Platform`

Zmienia część runtime'u w [ADR-0002](0002-stos-python-pyside6.md): zamiast `org.kde.Platform` z bazą
`io.qt.PySide.BaseApp` paczka stoi na `org.freedesktop.Platform` i niesie własne Qt.

## Kontekst

- PySide6 korzysta z prywatnego API Qt. Jego symbole mają w nazwie łatkę Qt (`QtPrivate_6_11_2`), więc PySide6
  działa tylko z Qt dokładnie tej wersji, z którą go zbudowano.
- PySide6 trafia do paczki w chwili budowania (z `io.qt.PySide.BaseApp//6.11`), a `org.kde.Platform//6.11`
  aktualizuje się u użytkownika osobno. Przejście runtime'u na Qt 6.11.3 wyłączyło wydaną 0.10.18
  ([0085](../../TODO/ZROBIONE/0085-flatpak-qt-6-11-3/todo.md),
  [issue #3](https://github.com/DragonKing026/DK-Tracker-Linux/issues/3)). Poprawka była możliwa dopiero, gdy
  BaseApp dogonił runtime.
- To samo dotyczy `layer-shell-qt` (prywatne API QtWaylandClient), budowanego na Qt runtime'u.
- Wymaganie użytkownika: aplikacja ma działać zawsze, bez zależności od tego, co i kiedy zaktualizuje się na jego
  komputerze.

## Rozważane opcje

| Opcja | Zalety | Wady |
| --- | --- | --- |
| Zostać przy runtime KDE + strażnik w CI | mała paczka, Qt i łatki z runtime'u | każda łatka Qt psuje paczkę do czasu przebudowy; przebudowa możliwa dopiero po aktualizacji BaseApp (dni) |
| Qt budowane ze źródeł w manifeście + PySide6 ze źródeł | pełna kontrola | build w CI 1–2 h, duże utrzymanie |
| **PySide6 z PyPI (wheel niesie Qt) na `org.freedesktop.Platform`** | runtime bez Qt — jego aktualizacja nie dotyka naszego Qt; gotowe, podpisane sumami wheele; build kilka minut | paczka większa; łatki Qt przychodzą z nowym PySide6, nie z runtime'u |

`layer-shell-qt` odrzucił przy tej opcji [ADR-0006](0006-budowanie-flatpaka-w-kontenerze.md) (brak nagłówków Qt
w wheelu). Rozwiązanie: nagłówki i pliki CMake z oficjalnych binariów Qt tej samej wersji
(`download.qt.io/online/qtsdkrepository`, z nich powstają wheele) — tylko na czas budowy.

## Decyzja

**Paczka stoi na `org.freedesktop.Platform` i niesie Qt z wheeli `shiboken6` i `pyside6-essentials` z PyPI;
`layer-shell-qt` jest budowany na nagłówkach oficjalnych binariów Qt tej samej wersji i ładuje Qt z wheela.**

## Uzasadnienie

- Aplikacja i tak nie korzysta z integracji z Plasmą: okno ma na stałe styl `Basic`
  ([window.py](../../src/dk_tracker/ui/main_window/window.py)), a tacka, portal plików i Wayland są w samym Qt
  (wheel ma `libqwayland.so`, `xdg-shell`, `libqxdgdesktopportal.so`).
- `pyside6-essentials` zawiera wszystkie moduły, których używa aplikacja (Core, Gui, Network, Qml, Quick,
  QuickControls2, Svg, Widgets); `pyside6-addons` nie jest potrzebny.
- Runtime freedesktop nie zawiera Qt, więc jego aktualizacje (Mesa, biblioteki systemowe) nie dotykają ABI Qt.
- Bez `base:` znika też powód budowy w kontenerze z ADR-0006 (regresja `build-init --base`), choć kontener zostaje
  dla powtarzalności.

## Konsekwencje

- Paczka rośnie (Qt w środku); nieużywane części Qt usuwa `cleanup` manifestu.
- Łatki bezpieczeństwa Qt przychodzą z nowym wydaniem PySide6 — pilnuje ich strażnik w CI
  ([0086](../../TODO/W-TRAKCIE/0086-flatpak-straznik-qt/todo.md)).
- Wersja wheela PySide6 i oficjalnych binariów Qt w manifeście musi być ta sama — pilnuje test pakietu.
- Python w paczce pochodzi z runtime'u freedesktop (26.08: Python 3.14).

## Powiązane

- [Flatpak](../integracje/flatpak.md), [Qt / PySide6](../integracje/qt-pyside6.md),
  [layer-shell-qt](../integracje/layer-shell-qt.md)
- Zadanie [0086](../../TODO/W-TRAKCIE/0086-flatpak-straznik-qt/todo.md)
