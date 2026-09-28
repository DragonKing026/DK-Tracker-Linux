---
noteId: "95c49cbeb79a45d79051be52f95515e7"
tytul: "Okno przy tacce na ekranie klikniętej ikony"
numer: "0075"
status: zrobione
priorytet: p1
tags: [todo, bug, okno-przy-tacce, kde, wayland]
zalezy_od: ["0066-plotno-okna-przy-tacce"]
utworzono: 2026-09-28 07:34
zaktualizowano: 2026-09-28 07:40
zamknieto: 2026-09-28 07:40
---

# 0075 — Okno przy tacce na ekranie klikniętej ikony

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Przy kilku monitorach kliknięcie ikony w tacce otwiera okienko na monitorze, na którym kliknięto,
a nie zawsze na głównym.

## Kontekst

- Błąd zgłoszony dla 0.10.x (KDE Plasma, Wayland): okienko zawsze pojawia się na monitorze głównym.
- Przyczyna: powierzchnia layer-shell ([ADR-0005](../../../docs/decyzje/0005-okno-przy-tacce-na-kde.md)) dostaje
  od layer-shell-qt 6.7.5 wyjście z `QWindow::screen()`, a to bez naszej ingerencji jest ekran główny.
  Właściwość `wantsToBeOnActiveScreen` zostawia wybór kompozytorowi (KWin: aktywny ekran, czyli ten z kursorem);
  powierzchnia powstaje od nowa przy każdym pokazaniu okna.
- Płótno ([0066](../0066-plotno-okna-przy-tacce/todo.md)) ma rozmiar obszaru roboczego ekranu — po
  przejściu na inny ekran trzeba je dopasować do niego.

## Kryteria akceptacji

- [x] Na KDE Wayland okienko otwiera się na monitorze, na którym kliknięto ikonę
- [x] Płótno i panel mieszczą się na tym monitorze (także mniejszym niż główny)
- [x] Test jednostkowy: zmiana ekranu okna dopasowuje płótno
- [x] Dokumentacja zaktualizowana
- [x] Zmiany zacommitowane małymi krokami

## Kroki

- [x] `placement.py`: `wantsToBeOnActiveScreen = true`
- [x] `popup.py`: na `screenChanged` okna płótno i panel dopasowane do nowego ekranu
- [x] Test na dwóch monitorach (ręcznie)
- [x] Dokumentacja okna przy tacce

## Materiały

Brak.

## Dziennik

### 2026-09-28 07:34

- Utworzono zadanie. Przyczyna ustalona w źródle layer-shell-qt 6.7.5 (`qwaylandlayersurface.cpp`).
- **07:35** Start pracy.

### 2026-09-28 07:37

- `placement.py`: `wantsToBeOnActiveScreen = true` (sprawdzone na żywo: właściwość prawdziwa, nie dynamiczna;
  okno się pokazuje). `popup.py`: `fit_screen` na `QWindow.screenChanged`. Testy: 746 zielonych.
- Dokumentacja: [layer-shell-qt](../../../docs/integracje/layer-shell-qt.md), sekcja „Który monitor”.
- Czeka na test ręczny na dwóch monitorach (ta sesja widzi jeden ekran, DP-6).
- **07:40** Użytkownik potwierdził na dwóch monitorach: okno otwiera się na monitorze klikniętej ikony.

## Wynik

Okno przy tacce na KDE Wayland otwiera się na monitorze klikniętej ikony i mieści się na nim
([placement.py](../../../src/dk_tracker/ui/placement.py), [popup.py](../../../src/dk_tracker/ui/popup.py),
[layer-shell-qt](../../../docs/integracje/layer-shell-qt.md)). Commity: `4f66e4d`, `358af41`, `7879344`.
Nic nie zostało na później.
