---
noteId: "24d8789388df48c987cf537a7f79e1ad"
tytul: "Kalendarz otwiera się na pierwszym wpisie"
numer: "0091"
status: do-zrobienia
priorytet: p2
tags: [todo, kalendarz]
zalezy_od: ["0090-wiersz-tytulu-w-kalendarzu"]
utworzono: 2026-11-20 13:54
zaktualizowano: 2026-11-20 13:54
zamknieto:
---

# 0091 — Kalendarz otwiera się na pierwszym wpisie

> [!info] Status
> **do-zrobienia** · priorytet **p2** · [← tablica zadań](../../README.md)

## Cel

Kalendarz domyślnie pokazuje godziny od najwcześniejszego wpisu w widocznych dniach, a nie puste godziny nocne.

## Kontekst

- Prośba użytkownika (2026-11-20 13:54): „domyślnie w kalendarzu od najwyższego wpisu — bez sensu ładować od 0:00 czy
  1:00 w nocy”.
- Dotąd: od 8:00, później tylko gdy „teraz” byłoby poza widokiem
  ([0079](../../ZROBIONE/0079-skala-kalendarza/todo.md)), i tylko raz — przy pierwszym pokazaniu dni.
- Opis: [F-37 Kalendarz](../../../docs/architektura/funkcje.md#f-37-kalendarz-0105).

## Kryteria akceptacji

- [ ] Widok przewinięty na pełną godzinę najwcześniejszego wpisu widocznych dni.
- [ ] Bez wpisów — jak dotąd: 8:00, później gdy „teraz” byłoby poza widokiem.
- [ ] Przy przejściu na inny dzień / tydzień — przewinięcie na jego pierwszy wpis; odświeżenie co minutę nie rusza
  widoku.
- [ ] Test, dokumentacja, wydanie.

## Kroki

- [ ] `CalendarView.qml`: `scrollToWork` od najwcześniejszego bloku, ponownie przy zmianie okresu.
- [ ] Test w `tests/ui/main_window/test_window.py`.
- [ ] Dokumentacja, wydanie.

## Materiały

Brak.

## Dziennik

### 2026-11-20 13:54

- Utworzono zadanie.

## Wynik

<!-- Wypełniane przy zamknięciu: co powstało, gdzie, co zostało na później. -->
