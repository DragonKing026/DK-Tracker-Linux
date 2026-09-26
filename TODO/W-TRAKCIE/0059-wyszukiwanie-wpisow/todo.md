---
noteId: "4cefa800a16e41adb7e18d3af322f669"
tytul: "Wyszukiwanie we wszystkich wpisach Kimai (F-33)"
numer: "0059"
status: w-trakcie
priorytet: p1
tags: [todo, ui, rdzen, kimai-api, lista-wpisow]
zalezy_od: ["0058"]
utworzono: 2026-09-26 13:19
zaktualizowano: 2026-09-26 13:19
zamknieto:
---

# 0059 — Wyszukiwanie we wszystkich wpisach Kimai (F-33)

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

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

- [ ] `KimaiClient.search`, `Tracker.search` (bez trwającego wpisu), `$` działa na wynikach
- [ ] Pole wyszukiwania, wyniki, „brak wyników”, błąd, powrót do ostatnich wpisów; teksty PL/EN
- [ ] Test kontraktowy na Kimai w Dockerze
- [ ] Dokumentacja F-33, pełny zestaw kontroli z CI

## Kroki

- [ ] Rdzeń (TDD)
- [ ] Interfejs i kontroler (TDD)
- [ ] Test kontraktowy
- [ ] Dokumentacja

## Materiały

Brak.

## Dziennik

### 2026-09-26

- **13:19** Utworzono i start.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
