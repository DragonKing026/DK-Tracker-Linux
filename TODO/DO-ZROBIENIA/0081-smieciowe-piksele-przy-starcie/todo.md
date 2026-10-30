---
noteId: "b7b4a8ff666847a083d482df171f5cc4"
tytul: "Śmieciowe piksele okienka przy tacce po starcie (issue #1)"
numer: "0081"
status: do-zrobienia
priorytet: p1
tags: [todo, blad, okienko, layer-shell]
zalezy_od: []
utworzono: 2026-10-30 14:19
zaktualizowano: 2026-10-30 14:19
zamknieto:
---

# 0081 — Śmieciowe piksele okienka przy tacce po starcie (issue #1)

> [!info] Status
> **do-zrobienia** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Okienko przy tacce na KDE (tryb layer) rysuje tylko panel w prawym dolnym rogu: obok panelu nie zostają
kawałki nagłówka, formularza ani listy z wcześniejszej klatki.

## Kontekst

- Zgłoszenie: [issue #1 „Bug when starting app”](https://github.com/DragonKing026/DK-Tracker-Linux/issues/1),
  wersja 0.10.17. Na zrzucie widać okienko narysowane dwa razy: właściwy panel w rogu i rozciągnięty do
  prawej krawędzi drugi nagłówek z formularzem i listą, a w przezroczystych miejscach — okna pod spodem.
  Zrzutu nie kopiujemy do repo (są na nim cudze dane z powiadomienia).
- Tryb layer to przezroczyste płótno na cały obszar roboczy z panelem w rogu i maską tylko na panelu
  ([0066](../../ZROBIONE/0066-plotno-okna-przy-tacce/todo.md),
  [layer-shell-qt](../../../docs/integracje/layer-shell-qt.md)). Po pokazaniu kompozytor kładzie powierzchnię
  na kliknięty monitor, a `fit_screen` zmienia rozmiar płótna
  ([0075](../../ZROBIONE/0075-okno-na-ekranie-kliknietej-tacki/todo.md)).

## Kryteria akceptacji

- [ ] Przyczyna potwierdzona na prawdziwej sesji Wayland (dziennik malowania).
- [ ] Poprawka w [popup.py](../../../src/dk_tracker/ui/popup.py) i test regresji, który bez niej nie przechodzi.
- [ ] Dokumentacja ([layer-shell-qt](../../../docs/integracje/layer-shell-qt.md)) zaktualizowana.
- [ ] Issue #1 zamknięte z odnośnikiem do commita.

## Kroki

- [ ] Odtworzenie: skrypt z filtrem zdarzeń na płótnie (Resize, LayoutRequest, Paint).
- [ ] Poprawka i test.
- [ ] Dokumentacja, commit, zamknięcie issue.

## Materiały

## Dziennik

### 2026-10-30 14:19

- Utworzono zadanie.

## Wynik
