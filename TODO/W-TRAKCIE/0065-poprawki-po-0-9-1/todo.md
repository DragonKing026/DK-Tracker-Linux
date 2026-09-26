---
noteId: "6498b6e1407647ca9135c9477808d508"
tytul: "Poprawki po 0.9.1: zmiana rozmiaru okna, mała ikona, zrzut w Discover"
numer: "0065"
status: w-trakcie
priorytet: p1
tags: [todo, ui, ikona, wydanie]
zalezy_od: []
utworzono: 2026-09-26 14:13
zaktualizowano: 2026-09-26 14:13
zamknieto:
---

# 0065 — Poprawki po 0.9.1: zmiana rozmiaru okna, mała ikona, zrzut w Discover

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Naprawić trzy zgłoszenia użytkownika po wydaniu 0.9.1.

## Kontekst

- **Zmiana rozmiaru okna skacze**, róg ucieka od kursora — z kodu i we Flatpaku. Uchwyt liczył przesunięcie z pozycji
  globalnej kursora, której okno przy tacce (layer-shell na Waylandzie) nie zna.
- **Ikona w nagłówku okna nieczytelna** (18 px, ciemny kafel na ciemnym tle) — mały wariant bez kafla i większy
  rozmiar ([0063](../../ZROBIONE/0063-ikona-ws-tracker/todo.md)).
- **Zrzut w Discover** pokazuje stare okno „Kimai Tray” — nowy zrzut z aplikacji na zmyślonych danych (zrzutów
  użytkownika z firmowymi wpisami nie publikujemy).
- Stara ikona w menu, na pasku i w Discover — pamięć podręczna KDE, nie paczka (sprawdzone sumami kontrolnymi).

## Kryteria akceptacji

- [ ] Zmiana rozmiaru liczona z pozycji w uchwycie, test (TDD); sprawdzone przez użytkownika
- [ ] Mały wariant ikony do nagłówka i paska tytułu, większy w nagłówku
- [ ] Nowy `docs/assets/zrzuty/okno-ciemny-motyw.png`

## Kroki

- [ ] Testy (TDD), implementacja, dokumentacja

## Materiały

Brak.

## Dziennik

### 2026-09-26

- **14:13** Utworzono i start.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
