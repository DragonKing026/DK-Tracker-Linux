---
noteId: "24d8789388df48c987cf537a7f79e1ad"
tytul: "Kalendarz otwiera się na pierwszym wpisie"
numer: "0091"
status: zrobione
priorytet: p2
tags: [todo, kalendarz]
zalezy_od: ["0090-wiersz-tytulu-w-kalendarzu"]
utworzono: 2026-11-20 13:54
zaktualizowano: 2026-11-20 13:56
zamknieto: 2026-11-20 13:56
---

# 0091 — Kalendarz otwiera się na pierwszym wpisie

> [!info] Status
> **zrobione** · priorytet **p2** · [← tablica zadań](../../README.md)

## Cel

Kalendarz domyślnie pokazuje godziny od najwcześniejszego wpisu w widocznych dniach, a nie puste godziny nocne.

## Kontekst

- Prośba użytkownika (2026-11-20 13:54): „domyślnie w kalendarzu od najwyższego wpisu — bez sensu ładować od 0:00 czy
  1:00 w nocy”.
- Dotąd: od 8:00, później tylko gdy „teraz” byłoby poza widokiem
  ([0079](../0079-skala-kalendarza/todo.md)), i tylko raz — przy pierwszym pokazaniu dni.
- Opis: [F-37 Kalendarz](../../../docs/architektura/funkcje.md#f-37-kalendarz-0105).

## Kryteria akceptacji

- [x] Widok przewinięty na pełną godzinę najwcześniejszego wpisu widocznych dni.
- [x] Bez wpisów — jak dotąd: 8:00, później gdy „teraz” byłoby poza widokiem.
- [x] Przy przejściu na inny dzień / tydzień — przewinięcie na jego pierwszy wpis; odświeżenie co minutę nie rusza
  widoku.
- [x] Test, dokumentacja, wydanie.

## Kroki

- [x] `CalendarView.qml`: `scrollToWork` od najwcześniejszego bloku, ponownie przy zmianie okresu.
- [x] Test w `tests/ui/main_window/test_window.py`.
- [x] Dokumentacja, wydanie.

## Materiały

Brak.

## Dziennik

### 2026-11-20 13:54

- Utworzono zadanie.
- **13:54** Start pracy.
- **13:56** Kod c78e531, docs c500abe, wersja 0.10.24; pytest 874 zielonych.

## Wynik

- Przewijanie od pełnej godziny najwcześniejszego bloku, ponownie przy zmianie okresu: `scrollToWork` w
  [CalendarView.qml](../../../src/dk_tracker/ui/main_window/qml/CalendarView.qml) (`c78e531`), test w
  [test_window.py](../../../tests/ui/main_window/test_window.py), opis w F-37 (`c500abe`). Wydanie 0.10.24.
