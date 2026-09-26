---
noteId: "f0ec236fea6f418a98eeff5fc066cbec"
tytul: "Pole opisu w okienku rośnie z kolejnymi liniami"
numer: "0068"
status: w-trakcie
priorytet: p1
tags: [todo, ui, poprawka]
zalezy_od: []
utworzono: 2026-09-26 16:40
zaktualizowano: 2026-09-26 16:40
zamknieto:
---

# 0068 — Pole opisu w okienku rośnie z kolejnymi liniami

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Zgłoszenie użytkownika (2026-09-26 16:40): przy wpisywaniu kolejnych linii opisu w okienku przy tacce pole się nie
rozciąga —
druga linia chowa pierwszą.

## Kontekst

- Pole (`DescriptionEdit` w `src/dk_tracker/ui/form.py`) liczyło wysokość z odstępu linii plus stałe 18 px i miało
  najmniej 38 px. Arkusz stylu okienka (`#description` w `src/dk_tracker/ui/theme.py`: padding 6 px, ramka 1 px,
  czcionka 15 px) i margines dokumentu (4 px) dają więcej, a Qt liczy wysokość bloku inaczej niż odstęp linii — już
  jedna linia nie mieściła się w 38 px, więc pole było przewijalne i przy drugiej linii przewijało do niej.
- Linia zawinięta (bez Shift+Enter) w ogóle nie powiększała pola: liczba linii była czytana przed ułożeniem zawinięć.
- Opis funkcji: [F-04](../../../docs/architektura/funkcje.md#f-04-start-timera).

## Kryteria akceptacji

- [x] Test (TDD) na prawdziwym okienku z jego stylem: dwie linie (Shift+Enter) i linia zawinięta — cały tekst
  widoczny, nic nie przewinięte; jedna linia też bez przewijania; nowe testy padają na starym kodzie
- [x] Wysokość mierzona tak jak Qt: wysokości ułożonych bloków + margines dokumentu + ramka i padding stylu
  (`contentsMargins`), przeliczana także po ułożeniu zawinięć i po zmianie szerokości
- [ ] Sprawdzone przez użytkownika w okienku

## Kroki

- [x] Odtworzenie w teście, przyczyna, poprawka, dokumentacja ([funkcje.md](../../../docs/architektura/funkcje.md))
- [ ] Sprawdzenie przez użytkownika

## Materiały

- [testy/pytest-2026-09-26.txt](testy/pytest-2026-09-26.txt) — przebieg po poprawce

## Dziennik

### 2026-09-26

- **2026-09-26 16:40** Utworzono i start; poprawka z testami. Jedna linia ma teraz ok. 41 px zamiast 38 px (margines
  dokumentu
  2 px zamiast 4 px) — stare 38 px było niższe niż linia, stąd przewijanie.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
