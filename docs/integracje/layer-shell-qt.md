---
noteId: "f3efec82850c4e988d4ce0c0ce95e4b5"
tytul: layer-shell-qt (okno zakotwiczone przy tacce na KDE)
tags: [integracja, wayland, kde, ui]
status_integracji: planowana
wersja: 6.7.5 (Plasma 6.7.5; moduł we Flatpaku ze źródeł KDE)
utworzono: 2026-09-25 20:38
zaktualizowano: 2026-09-25 22:08
---

# layer-shell-qt

> [!info] W skrócie
> Biblioteka KDE, która pozwala oknu Qt być powierzchnią protokołu Wayland
> **wlr-layer-shell** — przyklejoną do krawędzi ekranu, ponad oknami, z własnymi marginesami.
> Tak robi się panele i aplety. Używamy jej, żeby okno szybkiej obsługi stało **przy tacce**
> na KDE ([ADR-0005](../decyzje/0005-okno-przy-tacce-na-kde.md)).

## Jak używamy (sprawdzone w prototypie)

PySide6 nie ma wiązań do `LayerShellQt`. Działa wywołanie C++ przez `ctypes` i ustawienie
właściwości przez system meta-obiektów Qt:

```python
# NIE ustawiamy QT_WAYLAND_SHELL_INTEGRATION — Window::get() wystarczy dla jednego okna (6.7.5)
...
window.winId()                                                # utwórz QWindow przed show()
lib = ctypes.CDLL("libLayerShellQtInterface.so.6")
get = lib["_ZN12LayerShellQt6Window3getEP7QWindow"]           # LayerShellQt::Window::get(QWindow*)
get.restype, get.argtypes = ctypes.c_void_p, [ctypes.c_void_p]
layer = shiboken6.wrapInstance(get(shiboken6.getCppPointer(window.windowHandle())[0]), QObject)
layer.setProperty("anchors", 2 | 8)                # AnchorBottom | AnchorRight
layer.setProperty("layer", 2)                      # LayerTop
layer.setProperty("keyboardInteractivity", 2)      # OnDemand — da się pisać
layer.setProperty("margins", QMargins(0, 0, 12, 12))
layer.setProperty("scope", "kimai-tray-popup")
```

Wynik na Plaśmie 6.7.5: okno 12 px od prawej, tuż nad panelem (kompozytor respektuje strefę
panelu); lokalnie i we Flatpaku. Szczegóły: [ustalenia prototypu](../../TODO/ZROBIONE/0004-prototyp-tacki-i-okna/notatki/ustalenia.md).

## Flatpak

Biblioteki **nie ma** w `org.kde.Platform` 6.10/6.11. Moduł manifestu budowany ze źródeł KDE
pod Qt runtime'u (wymaga prywatnego API QtWaylandClient — dlatego nie działa z Qt z paczek pip):

```yaml
- name: layer-shell-qt
  buildsystem: cmake-ninja
  config-opts: [-DCMAKE_BUILD_TYPE=Release, -DBUILD_TESTING=OFF]
  sources:
    - type: archive
      url: https://download.kde.org/stable/plasma/6.7.5/layer-shell-qt-6.7.5.tar.xz
      sha256: ccdcfec7081ca956f7a52c9113a4df3a226575bfbe98b56a2a9a4d7d7e19e8f0
```

Wtyczka trafia do `/app/lib/plugins/wayland-shell-integration/liblayer-shell.so`
(`QT_PLUGIN_PATH` runtime'u obejmuje `/app/lib/plugins`). Budowa: [ADR-0006](../decyzje/0006-budowanie-flatpaka-w-kontenerze.md).

## Pułapki

> [!warning]
> - **Bez zmiennej środowiskowej**: `QT_WAYLAND_SHELL_INTEGRATION=layer-shell` (tak robił prototyp)
>   zamienia **każde** okno procesu w warstwę. Zamiast niej: `Window::get(okno)` przed pokazaniem —
>   w 6.7.5 podpina integrację tylko do tego okna ([źródło](https://github.com/KDE/layer-shell-qt/blob/v6.7.5/src/interfaces/window.cpp),
>   sprawdzone na żywo 2026-09-25 22:08, [0028](../../TODO/ZROBIONE/0028-plan3-projekt-ui/todo.md)).
> - **Kruchy symbol C++**: nazwa `_ZN12LayerShellQt6Window3getEP7QWindow` zależy od ABI;
>   w aplikacji zamknięta w jednym module z testem obecności symbolu.
> - **Odczyt** enumów (`anchors`, `layer`) z PySide nie działa (brak konwertera) — tylko zapis.
> - Zmienne `LAYERSHELLQT_*` z dawnych wersji **nie istnieją** w 6.7.5.
> - GNOME (Mutter) nie udostępnia `layer-shell` aplikacjom — tam ścieżka bezramkowa.
> - Kliknięcie ikony w tacce przy otwartym oknie nie dociera do aplikacji (Plasma) — okno
>   zamyka przycisk, `Esc` albo klik obok.

## Gdzie w kodzie

> [!todo] Plan 3: moduł UI odpowiedzialny za wybór ścieżki (layer-shell / bezramkowe).
> Prototyp: [tray_demo.py](../../TODO/ZROBIONE/0004-prototyp-tacki-i-okna/prototyp/tray_demo.py) (`anchor_bottom_right`).

## Dokumentacja

- [layer-shell-qt — kod źródłowy (KDE Invent)](https://invent.kde.org/plasma/layer-shell-qt)
- [Protokół wlr-layer-shell-unstable-v1](https://wayland.app/protocols/wlr-layer-shell-unstable-v1)
- [Źródła wydania 6.7.5](https://download.kde.org/stable/plasma/6.7.5/)

## Powiązane

- [ADR-0005](../decyzje/0005-okno-przy-tacce-na-kde.md), [ADR-0006](../decyzje/0006-budowanie-flatpaka-w-kontenerze.md)
- [Qt / PySide6](qt-pyside6.md), [Flatpak](flatpak.md), [StatusNotifierItem](statusnotifieritem.md)
