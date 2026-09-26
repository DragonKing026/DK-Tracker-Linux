---
noteId: "480b092e39f04fec8671f63156b6301d"
tytul: "Zmiana projektu i rodzaju pracy trwającego wpisu (F-34)"
numer: "0060"
status: zrobione
priorytet: p1
tags: [todo, ui, rdzen, kimai-api]
zalezy_od: ["0059"]
utworzono: 2026-09-26 13:27
zaktualizowano: 2026-09-26 13:35
zamknieto: 2026-09-26 13:35
---

# 0060 — Zmiana projektu i rodzaju pracy trwającego wpisu (F-34)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

W przeciwieństwie do wtyczki ([kimai-ws-tracker](../../../docs/integracje/kimai-ws-tracker.md)) projekt i rodzaj pracy
trwającego wpisu można zmienić w oknie; zmiana zapisuje się w Kimai.

## Kontekst

Prośba użytkownika; projekt zaakceptowany 2026-09-26 13:27:

- Zmiana rodzaju pracy → zapis od razu. Zmiana projektu → rodzaje pracy nowego projektu; gdy obecny rodzaj pracy w nim
  jest, zapis od razu, inaczej czeka na wybór i zapisuje projekt z rodzajem pracy razem.
- `$` przyjmuje wartość domyślną nowego projektu i rodzaju pracy (jak przy starcie) — decyzja użytkownika; bez
  uprawnienia do billable nie jest wysyłany.
- Błąd → pasek błędu, listy wracają do stanu z Kimai. Odświeżanie nie nadpisuje wyboru w toku.

## Kryteria akceptacji

- [x] `Tracker.change_work` (TDD), test kontraktowy `PATCH project/activity` na Kimai w Dockerze
- [x] Formularz: aktywne listy przy trwającym wpisie, zapis, błąd, odświeżanie (TDD)
- [x] Dokumentacja F-34, pełny zestaw kontroli z CI

## Kroki

- [x] Rdzeń
- [x] Formularz i kontroler
- [x] Test kontraktowy, dokumentacja

## Materiały

- [testy/pytest-2026-09-26.txt](testy/pytest-2026-09-26.txt) — końcowy przebieg:
  `459 passed, 1 skipped, 14 deselected in 3.53s`

## Dziennik

### 2026-09-26

- **13:27** Utworzono i start.
- **13:35** Zamknięte: 459 passed, 1 skipped, 14 deselected in 3.53s, commity na main.

## Wynik

F-34: [Tracker.change_work](../../../src/ws_tracker_tray/core/tracker.py), aktywne listy w
[form.py](../../../src/ws_tracker_tray/ui/form.py), odmowa przywraca listy; test kontraktowy (także konto bez billable).
Sprawdzone na żywo. Wydanie 0.9.1.
