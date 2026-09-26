---
noteId: "eb520c52ff1b412b8d653352f7482e3c"
tytul: Okno szybkiej obsługi — przy tacce na KDE, na środku gdzie indziej
tags: [adr, ui, wayland, tray, kde]
status: zaakceptowana
zastapiona_przez:
utworzono: 2026-09-25 20:37
zaktualizowano: 2026-09-26 14:51
---

# ADR-0005: Okno przy tacce na KDE (layer-shell), na środku gdzie indziej

Zastępuje [ADR-0003](0003-okno-szybkiej-obslugi-na-wayland.md).

## Kontekst

ADR-0003 wybrał na 1.0 okno bezramkowe, które kompozytor stawia gdzie chce, a okno
zakotwiczone przy tacce (`layer-shell-qt`) odłożył do sprawdzenia w
[prototypie 0004](../../TODO/ZROBIONE/0004-prototyp-tacki-i-okna/todo.md). Prototyp na Plasmie 6.7.5 (Wayland) pokazał
([ustalenia](../../TODO/ZROBIONE/0004-prototyp-tacki-i-okna/notatki/ustalenia.md)):

- okno bezramkowe KWin stawia **na środku ekranu**;
- `layer-shell-qt` da się użyć z PySide bez kompilacji (`ctypes` + `setProperty`), okno staje
  **w prawym dolnym rogu, tuż nad panelem i tacką**, da się w nim pisać, chowa się po kliknięciu obok;
- działa **we Flatpaku** — `layer-shell-qt` dołożony modułem manifestu, zbudowany pod Qt
  runtime'u (budowa w kontenerze: [ADR-0006](0006-budowanie-flatpaka-w-kontenerze.md));
- w **obu** wariantach kliknięcie ikony przy otwartym oknie **nic nie robi** (Plasma nie wysyła
  `Activate`) — ikona nie jest przełącznikiem;
- GNOME nie obsługuje `layer-shell` dla aplikacji (tam zostaje okno na środku); na GNOME nie testowano.

Użytkownik po obu testach ręcznych wolał okno przy tacce.

## Rozważane opcje

| Opcja | Zalety | Wady |
| --- | --- | --- |
| Okno na środku wszędzie (ADR-0003) | jedna ścieżka kodu | na KDE okno daleko od ikony |
| **Okno przy tacce na KDE, na środku gdzie indziej** | na KDE jak popup wtyczki; działa we Flatpaku | dwie ścieżki; `layer-shell` obejmuje cały proces; moduł w manifeście |
| Okno przy tacce tylko lokalnie, bez Flatpaka | prościej | sprzeczne z dystrybucją jako Flatpak |

## Decyzja

**Na KDE Plasma (Wayland, dostępny `layer-shell`) okno szybkiej obsługi jest powierzchnią
`layer-shell` zakotwiczoną w prawym dolnym rogu nad panelem (warstwa `top`, klawiatura
`on-demand`, marginesy 12 px). Wszędzie indziej (GNOME, X11, brak `layer-shell`) — okno
bezramkowe stawiane przez kompozytor (zwykle na środku). W obu przypadkach: chowanie po
utracie fokusu, przycisk zamknięcia w nagłówku i klawisz `Esc`; prawy klik ikony = menu
kontekstowe (F-20).**

Zaakceptowane przez użytkownika 2026-09-25 20:37.

## Aktualizacja (2026-09-26 14:51): płótno i panel

Zmiana rozmiaru uchwytem skakała: powierzchnia layer-shell przyklejona prawym dolnym rogiem przesuwa lewy górny róg
przy każdej zmianie rozmiaru, a Wayland podaje pozycję kursora względem rozmiaru, który KWin właśnie pokazuje —
nakłada go później niż aplikacja rysuje, a Qt nie przekazuje widżetom sygnału klatki. Trzy próby liczenia rozmiaru
zawiodły ([0065](../../TODO/W-TRAKCIE/0065-poprawki-po-0-9-1/todo.md)).

**Teraz** ([0066](../../TODO/W-TRAKCIE/0066-plotno-okna-przy-tacce/todo.md)): w trybie layer powierzchnia stale ma
rozmiar obszaru roboczego ekranu minus marginesy i jest przezroczysta; widoczny **panel** leży w jej prawym dolnym rogu,
a **maska** (region wejścia) obejmuje tylko panel, więc kliknięcia obok trafiają na pulpit. Uchwyt zmienia tylko panel
— po stronie aplikacji, natychmiast, a pozycja kursora jest zawsze dokładna. Sprawdzone na żywo na KDE Plasma 6.

## Konsekwencje

- ~~`QT_WAYLAND_SHELL_INTEGRATION=layer-shell` działa dla całego procesu~~ — **niepotrzebne**: w layer-shell-qt 6.7.5
  `LayerShellQt::Window::get(okno)` podpina layer-shell **tylko do tego okna** (`setShellIntegration` na jednym
  `QWaylandWindow`). Okno ustawień zostaje zwykłym oknem z ramką. Sprawdzone na żywo 2026-09-25 22:08
  ([0028](../../TODO/ZROBIONE/0028-plan3-projekt-ui/todo.md)).
- Wybór ścieżki przy starcie: `layer-shell` tylko gdy sesja Wayland i kompozytor go obsługuje
  (Plasma); inaczej ścieżka bezramkowa. Test na GNOME — zadanie dla testerów.
- Kod `ctypes` do `LayerShellQt::Window::get` jest kruchy (nazwa symbolu C++) — zamknięty
  w jednym module UI z testem, który sprawdza obecność symbolu.
- Manifest Flatpaka zawiera moduł `layer-shell-qt` (wersja zgodna z Plasmą) — integracja:
  [layer-shell-qt](../integracje/layer-shell-qt.md).
- Ikona w tacce nie zamyka okna — to zachowanie Plasmy, nie do obejścia po stronie aplikacji.

## Powiązane

- [ADR-0003](0003-okno-szybkiej-obslugi-na-wayland.md) (zastąpiona), [ADR-0006](0006-budowanie-flatpaka-w-kontenerze.md)
- [Prototyp 0004 — ustalenia](../../TODO/ZROBIONE/0004-prototyp-tacki-i-okna/notatki/ustalenia.md)
- [Katalog funkcji — F-03, F-20](../architektura/funkcje.md)
