---
noteId: "4cefa800a16e41adb7e18d3af322f669"
tytul: "Wyszukiwanie we wszystkich wpisach Kimai (F-33)"
numer: "0059"
status: zrobione
priorytet: p1
tags: [todo, ui, rdzen, kimai-api, lista-wpisow]
zalezy_od: ["0058"]
utworzono: 2026-09-26 13:19
zaktualizowano: 2026-09-26 13:35
zamknieto: 2026-09-26 13:35
---

# 0059 — Wyszukiwanie we wszystkich wpisach Kimai (F-33)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Pole „Szukaj we wszystkich wpisach…” nad listą ostatnich wpisów: szukanie w całej historii użytkownika w Kimai, wyniki
jak lista ostatnich (dni, wznów, `$`, rozwijany opis).

## Kontekst

Prośba użytkownika po teście 0.9.0; projekt zaakceptowany 2026-09-26 13:19:

- `GET /api/timesheets?term=…&size=50&orderBy=begin&order=DESC&full=true` — Kimai 2.67.0 szuka tylko w **opisie**
  (`TimesheetRepository`: `SearchConfiguration(['t.description'], …)`), słowa rozdzielone spacją, domyślnie wpisy
  bieżącego użytkownika ([Kimai API](../../../docs/integracje/kimai-api.md)).
- Od 2 znaków, 0,4 s po ostatnim klawiszu; spóźnione odpowiedzi ignorowane; Esc / puste pole → ostatnie wpisy.
- Wydanie razem z [0058](../0058-dlugie-opisy-na-liscie/todo.md) jako 0.9.1.

## Kryteria akceptacji

- [x] `KimaiClient.search`, `Tracker.search` (bez trwającego wpisu), `$` działa na wynikach
- [x] Pole wyszukiwania, wyniki, „brak wyników”, błąd, powrót do ostatnich wpisów; teksty PL/EN
- [x] Test kontraktowy na Kimai w Dockerze
- [x] Dokumentacja F-33, pełny zestaw kontroli z CI

## Kroki

- [x] Rdzeń (TDD)
- [x] Interfejs i kontroler (TDD)
- [x] Test kontraktowy
- [x] Dokumentacja

## Materiały

- [testy/pytest-2026-09-26.txt](testy/pytest-2026-09-26.txt) — końcowy przebieg:
  `459 passed, 1 skipped, 14 deselected in 3.53s`

## Dziennik

### 2026-09-26

- **13:19** Utworzono i start.
- **13:35** Zamknięte: 459 passed, 1 skipped, 14 deselected in 3.53s, commity na main.

## Wynik

F-33: [KimaiClient.search](../../../src/ws_tracker_tray/core/kimai_client.py),
[Tracker.search](../../../src/ws_tracker_tray/core/tracker.py), pole w
[recent.py](../../../src/ws_tracker_tray/ui/recent.py),
kontroler; rok w nagłówku dnia z innego roku; test kontraktowy. Przy okazji: liniowe wyszukiwanie projektów (CI).
Sprawdzone
na żywo. Wydanie 0.9.1.
