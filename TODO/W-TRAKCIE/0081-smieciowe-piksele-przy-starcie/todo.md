---
noteId: "b7b4a8ff666847a083d482df171f5cc4"
tytul: "Śmieciowe piksele okienka przy tacce po starcie (issue #1)"
numer: "0081"
status: w-trakcie
priorytet: p1
tags: [todo, blad, okienko, layer-shell]
zalezy_od: []
utworzono: 2026-10-30 14:19
zaktualizowano: 2026-10-30 14:59
zamknieto:
---

# 0081 — Śmieciowe piksele okienka przy tacce po starcie (issue #1)

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

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

- [x] Przyczyna potwierdzona na prawdziwej sesji Wayland (dziennik malowania).
- [x] Poprawka w [popup.py](../../../src/dk_tracker/ui/popup.py) i test regresji, który bez niej nie przechodzi.
- [x] Dokumentacja ([layer-shell-qt](../../../docs/integracje/layer-shell-qt.md)) zaktualizowana.
- [x] Issue #1 zamknięte z odnośnikiem do commita.

## Kroki

- [x] Odtworzenie: skrypt z filtrem zdarzeń na płótnie (Resize, LayoutRequest, Paint).
- [x] Poprawka i test.
- [x] Dokumentacja, commit, zamknięcie issue.

## Materiały

- [odtworz_malowanie_plotna.py](testy/odtworz_malowanie_plotna.py) — okienko w trybie layer z filtrem zdarzeń:
  każde `Resize`, `LayoutRequest` i `Paint` z położeniem nagłówka i marginesami układu.
- [malowanie-przed.log](testy/malowanie-przed.log) — bez poprawki: po `Resize` płótna (kompozytor przeniósł
  powierzchnię na monitor 2560×1440) całe płótno jest malowane z nagłówkiem w starym miejscu (1196, 406) i szerokości
  1340 px, a marginesy mówią już (1836, 766). Następne malowania obejmują tylko panel.
- [malowanie-po.log](testy/malowanie-po.log) — z poprawką: to samo malowanie ma nagłówek w panelu (1836, 766), 700 px.

## Dziennik

### 2026-10-30 14:19

- Utworzono zadanie.
- **14:20** Start pracy: odtworzenie na sesji Wayland.

### 2026-10-30 14:21

- Przyczyna: maska (`setMask`) przycina malowanie do panelu, a płótno jest malowane całe tylko raz po zmianie rozmiaru
  (`fit_screen` po `screenChanged`). W tym malowaniu dzieci stały jeszcze tam, gdzie postawiły je stare marginesy —
  nowe działały dopiero po `LayoutRequest`. Zmniejszanie panelu uchwytem jest w porządku (Qt odmalowuje stary prostokąt
  panelu).
- Poprawka: `layout().activate()` w `_place_panel` (3947a70), test
  `test_a_new_canvas_is_painted_with_the_panel_already_in_place` — bez poprawki nie przechodzi. Docs: 0cff17c.
- Poprawka gotowa, czeka na wydanie. Issue #1 zamknięte z odnośnikiem do 3947a70.

### 2026-10-30 14:59

- Wydane w 0.10.18 (46a116f, tag `v0.10.18`); `flatpak update` je widzi. Czeka na potwierdzenie u użytkownika.

## Wynik
