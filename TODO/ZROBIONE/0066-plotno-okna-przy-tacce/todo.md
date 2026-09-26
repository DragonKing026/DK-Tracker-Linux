---
noteId: "d8221fd7d22b4305a4e3c4d5967aa69e"
tytul: "Zmiana rozmiaru okna przy tacce bez skoków: przezroczyste płótno i panel"
numer: "0066"
status: zrobione
priorytet: p1
tags: [todo, ui, wayland, layer-shell]
zalezy_od: ["0065"]
utworzono: 2026-09-26 14:46
zaktualizowano: 2026-09-26 14:51
zamknieto: 2026-09-26 14:51
---

# 0066 — Zmiana rozmiaru okna przy tacce bez skoków: przezroczyste płótno i panel

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Okno przy tacce (KDE, layer-shell) ma przy przeciąganiu uchwytu iść za kursorem na żywo, bez opóźnień i skoków,
w każdym rozmiarze.

## Kontekst

Trzy próby poprawienia liczenia rozmiaru zawiodły ([0065](../0065-poprawki-po-0-9-1/todo.md), logi z testów na żywo):

1. Przesunięcie w uchwycie dodawane do żądanego rozmiaru — przy szybkim ruchu liczone kilka razy.
2. Od narysowanego rozmiaru — dobrze do ok. ¼ ekranu, wyżej okno oscyluje: KWin nakłada nowy rozmiar później niż
   rysujemy, a pozycje kursora odnoszą się do rozmiaru, który KWin właśnie pokazuje (nieznanego aplikacji).
3. Od rozmiaru potwierdzonego sygnałem klatki (`UpdateRequest`) — Qt nie przekazuje go widżetom; skacze zawsze.

Wniosek: dopóki powierzchnia zmienia rozmiar w trakcie przeciągania, pozycja kursora odnosi się do nieznanego
rozmiaru. **Nowa budowa (zaakceptowana przez użytkownika):** w trybie layer powierzchnia stale ma największy
dozwolony rozmiar i jest przezroczysta; zawartość to panel w jej prawym dolnym rogu, maska (region wejścia) obejmuje
tylko panel — kliknięcia obok trafiają na pulpit. Przeciąganie zmienia tylko panel (po stronie aplikacji), więc
pozycja kursora jest zawsze dokładna. Tryby frameless (GNOME) i window bez zmian.

## Kryteria akceptacji

- [x] Płótno, panel w prawym dolnym rogu, maska = panel (TDD)
- [x] Uchwyt zmienia tylko panel, dokładnie o ruch kursora; płótno bez zmian (TDD)
- [x] Rozmiar zapamiętywany jak dotąd; tryb kompaktowy (nieskonfigurowane) działa
- [x] Test na żywo: płynnie w każdym rozmiarze, kliknięcia obok okna działają

## Kroki

- [x] Testy, implementacja, test na żywo, dokumentacja (ADR-0005, layer-shell-qt)

## Materiały

- [testy/pytest-2026-09-26.txt](testy/pytest-2026-09-26.txt) — końcowy przebieg:
  `465 passed, 1 skipped, 14 deselected in 3.60s`

## Dziennik

### 2026-09-26

- **14:46** Utworzono po trzeciej nieudanej próbie w 0065; nowa budowa zaakceptowana (wariant „najpierw przebudowa”).
- **14:51** Zamknięte: 465 passed, 1 skipped, 14 deselected in 3.60s, commity na main.

## Wynik

[popup.py](../../../src/dk_tracker/ui/popup.py): w trybie layer przezroczyste płótno (obszar roboczy minus marginesy),
panel w prawym dolnym rogu, maska na panelu, uchwyt zmienia tylko panel;
[placement.py](../../../src/dk_tracker/ui/placement.py) ustawia przezroczystość przed layer-shell. Testy w
[test_popup.py](../../../tests/ui/test_popup.py). Test na żywo: zmiana rozmiaru płynna w każdym rozmiarze.
