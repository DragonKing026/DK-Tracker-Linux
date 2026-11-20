---
noteId: "f3efec82850c4e988d4ce0c0ce95e4b5"
tytul: layer-shell-qt (okno zakotwiczone przy tacce na KDE)
tags: [integracja, wayland, kde, ui]
status_integracji: planowana
wersja: 6.7.5 (Plasma 6.7.5; moduł we Flatpaku ze źródeł KDE)
utworzono: 2026-09-25 20:38
zaktualizowano: 2026-11-20 10:41
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
layer.setProperty("scope", "dk-tracker-popup")
layer.setProperty("wantsToBeOnActiveScreen", True) # monitor wybiera kompozytor (0075)
```

Wynik na Plaśmie 6.7.5: okno 12 px od prawej, tuż nad panelem (kompozytor respektuje strefę
panelu); lokalnie i we Flatpaku. Szczegóły:
[ustalenia prototypu](../../TODO/ZROBIONE/0004-prototyp-tacki-i-okna/notatki/ustalenia.md).

## Flatpak

Biblioteki nie ma w żadnym runtime'ie. Od 0.10.20 Qt jest w paczce
([ADR-0008](../decyzje/0008-qt-w-paczce-flatpak.md)), więc `layer-shell-qt` budujemy na Qt z koła PySide6:

- nagłówki i pliki CMake bierzemy z oficjalnych binariów Qt **tej samej wersji** (moduł `qt-sdk`, tylko na czas
  budowy) — z tej samej kompilacji powstają koła, więc symbole prywatnego API QtWaylandClient się zgadzają;
- `-DCMAKE_INSTALL_RPATH=/app/lib/python3.14/site-packages/PySide6/Qt/lib` — biblioteka ładuje Qt z koła;
- wtyczka `liblayer-shell.so` trafia do `PySide6/Qt/plugins/wayland-shell-integration/` (katalog wtyczek Qt z koła),
  `libLayerShellQtInterface.so.6` do `/app/lib` (tam szuka jej `ctypes`);
- potrzebuje też `extra-cmake-modules` (moduł manifestu) oraz `wayland-scanner` i `wayland-protocols` z SDK.

Do 0.10.19 moduł był budowany na Qt z `org.kde.Platform` — i psuł się razem z PySide6 przy łatce Qt w runtime'ie.
Moduły i źródła: [Flatpak](flatpak.md#qt-w-paczce-adr-0008).

## Zmiana rozmiaru: płótno zamiast zmiany powierzchni

Powierzchnia layer-shell nie zna swojej pozycji na ekranie (pozycja globalna kursora jest zmyślona), a przy zmianie
rozmiaru przyklejonej prawym dolnym rogiem powierzchni pozycje kursora odnoszą się do rozmiaru, który kompozytor
dopiero nałoży. Dlatego okno w trybie layer to **przezroczyste płótno** o rozmiarze obszaru roboczego z **panelem**
w prawym dolnym rogu i maską (`QWidget.setMask` → region wejścia) tylko na panelu; przeciąganie zmienia panel, nie
powierzchnię ([ADR-0005](../decyzje/0005-okno-przy-tacce-na-kde.md),
[0066](../../TODO/ZROBIONE/0066-plotno-okna-przy-tacce/todo.md)). `WA_TranslucentBackground` trzeba ustawić przed
utworzeniem natywnego okna — robi to `placement.apply` przed `layer-shell`.

> [!warning] Układ nie może ustalać minimum okna
> Górny i lewy margines układu to „płótno − panel”. Przy domyślnym `SetDefaultConstraint` minimum okna = margines +
> minimum zawartości, więc panel niższy niż zawartość (zapamiętane 420 px przy formularzu 306 px) powiększał płótno,
> ono margines i tak bez końca — aż `QWaylandShmBuffer` nie dostał bufora i proces padał (SIGSEGV). Na płótnie układ ma
> `SetNoConstraint`, a panel nie schodzi poniżej minimum zawartości (także gdy zawartość rośnie — `LayoutRequest`)
> ([0076](../../TODO/ZROBIONE/0076-petla-rozmiaru-plotna/todo.md)).

Maska ma też skutek przy rysowaniu, nie tylko przy kliknięciach:

> [!warning] Maska przycina też malowanie
> Po `setMask` Qt maluje okno tylko w obrębie maski: poza panelem płótno jest czyszczone (przezroczyste) wyłącznie
> wtedy, gdy Qt maluje całe płótno, czyli raz po zmianie jego rozmiaru (`fit_screen` na innym monitorze). Nowe marginesy
> układu działają jednak dopiero po `LayoutRequest`, a to malowanie przychodzi wcześniej — nagłówek, formularz i lista
> zostawały w starym miejscu, rozciągnięte do prawej krawędzi, i nic ich już nie zamalowywało
> ([issue #1](https://github.com/DragonKing026/DK-Tracker-Linux/issues/1),
> [0081](../../TODO/ZROBIONE/0081-smieciowe-piksele-przy-starcie/todo.md)). Dlatego `_place_panel` po zmianie
> marginesów od razu wywołuje `layout().activate()`.

## Który monitor

Bez ustawień layer-shell-qt podaje kompozytorowi wyjście z `QWindow::screen()` — to zawsze ekran główny, bo aplikacja
na Waylandzie nie zna pozycji kursora poza własnymi oknami. `wantsToBeOnActiveScreen = true` wysyła
`get_layer_surface` bez wyjścia, a KWin wybiera **aktywny ekran** (ten z kursorem, czyli z klikniętą ikoną tacki).
Powierzchnia powstaje od nowa przy każdym pokazaniu okna, więc wybór jest świeży przy każdym kliknięciu
([źródło](https://github.com/KDE/layer-shell-qt/blob/v6.7.5/src/qwaylandlayersurface.cpp),
[0075](../../TODO/ZROBIONE/0075-okno-na-ekranie-kliknietej-tacki/todo.md)). Qt poznaje ekran z `wl_surface.enter`
i emituje `QWindow.screenChanged`; wtedy `QuickWindow.fit_screen` dopasowuje płótno i panel do obszaru roboczego
tego monitora. (`screenConfiguration` robi to samo, ale w 6.7.5 jest przestarzała.)

## Pułapki

> [!warning]
>
> - **Bez zmiennej środowiskowej**: `QT_WAYLAND_SHELL_INTEGRATION=layer-shell` (tak robił prototyp)
>   zamienia **każde** okno procesu w warstwę. Zamiast niej: `Window::get(okno)` przed pokazaniem —
>   w 6.7.5 podpina integrację tylko do tego okna
>   ([źródło](https://github.com/KDE/layer-shell-qt/blob/v6.7.5/src/interfaces/window.cpp),
>   sprawdzone na żywo 2026-09-25 22:08, [0028](../../TODO/ZROBIONE/0028-plan3-projekt-ui/todo.md)).
> - **Kruchy symbol C++**: nazwa `_ZN12LayerShellQt6Window3getEP7QWindow` zależy od ABI;
>   w aplikacji zamknięta w jednym module z testem obecności symbolu.
> - **Odczyt** enumów (`anchors`, `layer`) z PySide nie działa (brak konwertera) — tylko zapis.
> - Zmienne `LAYERSHELLQT_*` z dawnych wersji **nie istnieją** w 6.7.5.
> - GNOME (Mutter) nie udostępnia `layer-shell` aplikacjom — tam ścieżka bezramkowa.
> - Kliknięcie ikony w tacce przy otwartym oknie nie dociera do aplikacji (Plasma) — okno
>   zamyka przycisk, `Esc` albo klik obok.
> - **Systemowa biblioteka nie działa z Qt z koła**: `layer-shell-qt` z dystrybucji (np. Fedory) wymaga
>   `Qt_6.11_PRIVATE_API` systemowego Qt, którego nie eksportuje Qt z koła PySide6 — `CDLL` rzuca `OSError`,
>   aplikacja przechodzi na okno bez ramki. Na żywo z `.venv` uruchamiamy więc systemowym Pythonem; we Flatpaku moduł
>   jest budowany na nagłówkach Qt z tej samej kompilacji co koło.

## Gdzie w kodzie

- [src/dk_tracker/ui/placement.py](../../src/dk_tracker/ui/placement.py) — `choose_mode` / `detect_mode`
  (layer / bez
  ramki / okno), `apply`, wywołanie `LayerShellQt::Window::get` przez ctypes tylko dla okna szybkiej obsługi.
- Test obecności symbolu: [tests/ui/test_popup.py](../../tests/ui/test_popup.py)
  (`test_layer_shell_symbol_is_present_when_the_library_is`).

## Dokumentacja

- [layer-shell-qt — kod źródłowy (KDE Invent)](https://invent.kde.org/plasma/layer-shell-qt)
- [Protokół wlr-layer-shell-unstable-v1](https://wayland.app/protocols/wlr-layer-shell-unstable-v1)
- [Źródła wydania 6.7.5](https://download.kde.org/stable/plasma/6.7.5/)

## Powiązane

- [ADR-0005](../decyzje/0005-okno-przy-tacce-na-kde.md), [ADR-0006](../decyzje/0006-budowanie-flatpaka-w-kontenerze.md)
- [Qt / PySide6](qt-pyside6.md), [Flatpak](flatpak.md), [StatusNotifierItem](statusnotifieritem.md)
