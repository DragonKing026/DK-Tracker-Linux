---
noteId: "480b092e39f04fec8671f63156b6301d"
tytul: "Zmiana projektu i rodzaju pracy trwającego wpisu (F-34)"
numer: "0060"
status: w-trakcie
priorytet: p1
tags: [todo, ui, rdzen, kimai-api]
zalezy_od: ["0059"]
utworzono: 2026-09-26 13:27
zaktualizowano: 2026-09-26 13:27
zamknieto:
---

# 0060 — Zmiana projektu i rodzaju pracy trwającego wpisu (F-34)

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

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

- [ ] `Tracker.change_work` (TDD), test kontraktowy `PATCH project/activity` na Kimai w Dockerze
- [ ] Formularz: aktywne listy przy trwającym wpisie, zapis, błąd, odświeżanie (TDD)
- [ ] Dokumentacja F-34, pełny zestaw kontroli z CI

## Kroki

- [ ] Rdzeń
- [ ] Formularz i kontroler
- [ ] Test kontraktowy, dokumentacja

## Materiały

Brak.

## Dziennik

### 2026-09-26

- **13:27** Utworzono i start.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
