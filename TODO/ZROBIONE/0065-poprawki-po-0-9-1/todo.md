---
noteId: "6498b6e1407647ca9135c9477808d508"
tytul: "Poprawki po 0.9.1: zmiana rozmiaru okna, mała ikona, zrzut w Discover"
numer: "0065"
status: zrobione
priorytet: p1
tags: [todo, ui, ikona, wydanie]
zalezy_od: []
utworzono: 2026-09-26 14:13
zaktualizowano: 2026-09-26 14:51
zamknieto: 2026-09-26 14:51
---

# 0065 — Poprawki po 0.9.1: zmiana rozmiaru okna, mała ikona, zrzut w Discover

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Naprawić trzy zgłoszenia użytkownika po wydaniu 0.9.1.

## Kontekst

- **Zmiana rozmiaru okna skacze**, róg ucieka od kursora — z kodu i we Flatpaku. Uchwyt liczył przesunięcie z pozycji
  globalnej kursora, której okno przy tacce (layer-shell na Waylandzie) nie zna.
- **Ikona w nagłówku okna nieczytelna** (18 px, ciemny kafel na ciemnym tle) — mały wariant bez kafla i większy
  rozmiar ([0063](../0063-ikona-ws-tracker/todo.md)).
- **Zrzut w Discover** pokazuje stare okno „Kimai Tray” — nowy zrzut z aplikacji na zmyślonych danych (zrzutów
  użytkownika z firmowymi wpisami nie publikujemy).
- Stara ikona w menu, na pasku i w Discover — pamięć podręczna KDE, nie paczka (sprawdzone sumami kontrolnymi).

## Kryteria akceptacji

- [x] Zmiana rozmiaru liczona z pozycji w uchwycie, test (TDD); sprawdzone przez użytkownika
- [x] Mały wariant ikony do nagłówka i paska tytułu, większy w nagłówku
- [x] Nowy `docs/assets/zrzuty/okno-ciemny-motyw.png`

## Kroki

- [x] Testy (TDD), implementacja, dokumentacja

## Materiały

- [testy/pytest-2026-09-26.txt](testy/pytest-2026-09-26.txt) — końcowy przebieg:
  `465 passed, 1 skipped, 14 deselected in 3.60s`

## Dziennik

### 2026-09-26

- **14:13** Utworzono i start.
- **14:51** Zamknięte: 465 passed, 1 skipped, 14 deselected in 3.60s, commity na main.

## Wynik

Zrzut okna i znak w nagłówku (24 px, bez kafla) zrobione tutaj; zmiana rozmiaru — trzy próby zawiodły (opis w
[0066](../0066-plotno-okna-przy-tacce/todo.md)), rozwiązana przebudową okna w 0066.
