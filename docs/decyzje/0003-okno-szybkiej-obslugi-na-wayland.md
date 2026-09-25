---
noteId: "52881c915ddd4b6b9caca3b509b690db"
tytul: Forma okna szybkiej obsługi na Waylandzie
tags: [adr, ui, wayland, tray]
status: zaakceptowana
zastapiona_przez:
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
---

# ADR-0003: Okno szybkiej obsługi — bezramkowe, chowane po utracie fokusu

## Kontekst

Wtyczka otwiera popup tuż pod ikoną w pasku przeglądarki. Na Waylandzie aplikacja
**nie może ustawić pozycji własnego okna** — decyduje kompozytor
([Wayland and Qt](https://doc.qt.io/qt-6/wayland-and-qt.html)). Menu kontekstowe ikony
SNI rysuje host tacki, więc ono zawsze pojawia się przy ikonie.
Aplikacja ma działać w KDE Plasma (priorytet) i w GNOME.

## Rozważane opcje

| Opcja | Zalety | Wady |
|---|---|---|
| **A. Okno bez ramki, chowane po kliknięciu obok** | zachowanie jak popup wtyczki; jedna implementacja dla KDE i GNOME | pozycję wybiera kompozytor (zwykle środek ekranu); w KDE można to poprawić regułą okna KWin |
| B. Popup przez `layer-shell-qt`, zakotwiczony przy panelu (tylko KDE) | wygląda jak natywny aplet Plasmy | biblioteki nie ma w `org.kde.Platform` (trzeba dołożyć moduł); nie działa w GNOME (fallback do A); więcej ryzyka |
| C. Najpierw menu, okno z menu | menu zawsze przy ikonie | lista i formularz startu w menu są niewygodne |
| D. Zwykłe okno z ramką | najprostsze | nie przypomina popupu |

## Decyzja

**Wersja 1.0 używa wariantu A: bezramkowe okno narzędziowe, pokazywane/chowane lewym
kliknięciem ikony i chowane po utracie fokusu. Dodatkowo prawy klik otwiera menu
kontekstowe z szybkimi akcjami (F-20). Wariant B sprawdzamy w prototypie 0004
i dokładamy dla KDE, jeśli okaże się stabilny.**

Zaakceptowane przez użytkownika 2026-09-25.

## Uzasadnienie

Wariant A daje zachowanie najbliższe wtyczce przy jednej ścieżce kodu dla obu pulpitów.
Menu kontekstowe kompensuje brak pozycjonowania: najczęstsze akcje (stop, wznów ostatni)
są zawsze dostępne tuż przy ikonie. Wariant B jest opcjonalnym ulepszeniem i nie blokuje 1.0.

## Konsekwencje

- Okno potrzebuje trybu „bez tacki” (GNOME bez rozszerzenia): wtedy zwykłe okno z ramką,
  bez chowania po utracie fokusu. Inaczej użytkownik nie miałby jak do niego wrócić.
- Do sprawdzenia w prototypie: czy chowanie po utracie fokusu nie koliduje z kliknięciem
  ikony (klik w ikonę zabiera fokus → okno się chowa → `Trigger` pokazuje je znowu).
  Może być potrzebne krótkie „okno czasowe” ignorowania.
- Kontrakt okna nie zależy od tego, jak zostało pokazane. Dzięki temu wariant B można
  dodać później bez przebudowy UI.
- Funkcja F-20 (menu kontekstowe) wchodzi do zakresu 1.0.

## Powiązane

- [F-03](../architektura/funkcje.md), [F-20](../architektura/funkcje.md)
- [Prototyp 0004](../../TODO/0004-prototyp-tacki-i-okna/todo.md)
- [Qt / PySide6](../integracje/qt-pyside6.md)
