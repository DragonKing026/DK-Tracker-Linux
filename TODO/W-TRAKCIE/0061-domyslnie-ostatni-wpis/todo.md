---
noteId: "6f72023cf9b946f2a97632feca4f24a5"
tytul: "Domyślny projekt i rodzaj pracy z ostatniego wpisu w Kimai"
numer: "0061"
status: w-trakcie
priorytet: p1
tags: [todo, ui, rdzen]
zalezy_od: ["0060"]
utworzono: 2026-09-26 13:31
zaktualizowano: 2026-09-26 13:31
zamknieto:
---

# 0061 — Domyślny projekt i rodzaj pracy z ostatniego wpisu w Kimai

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Gdy nic nie trwa, formularz podpowiada projekt i rodzaj pracy **ostatniego wpisu w Kimai** (najnowszy z listy ostatnich
wpisów), a nie tylko ostatniego startu z tej aplikacji — także gdy wpis powstał w przeglądarce.

## Kontekst

- Prośba użytkownika. Dotąd: `Memory.last_project` / `last_activity` — zapisywane tylko przy starcie z aplikacji
  ([F-06](../../../docs/architektura/funkcje.md#f-06-wybór-projektu-i-czynności)).
- Brak wpisów w Kimai → jak dotąd, zapamiętany wybór.

## Kryteria akceptacji

- [ ] `Tracker.default_work()` (TDD): najnowszy zakończony wpis, inaczej pamięć
- [ ] Okno podpowiada te wartości przy wczytaniu katalogu i rodzajów pracy (TDD)
- [ ] Dokumentacja F-06, pełny zestaw kontroli z CI

## Kroki

- [ ] Rdzeń
- [ ] Kontroler
- [ ] Dokumentacja

## Materiały

Brak.

## Dziennik

### 2026-09-26

- **13:31** Utworzono i start.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
