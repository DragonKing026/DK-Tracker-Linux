---
noteId: "cfe8810cb23947eaa959912018b9e68d"
tytul: "Wyraźny podpis „dni z wpisami” w podsumowaniach"
numer: "0092"
status: do-zrobienia
priorytet: p3
tags: [todo, podsumowania]
zalezy_od: []
utworzono: 2026-11-20 13:55
zaktualizowano: 2026-11-20 13:55
zamknieto:
---

# 0092 — Wyraźny podpis „dni z wpisami” w podsumowaniach

> [!info] Status
> **do-zrobienia** · priorytet **p3** · [← tablica zadań](../../README.md)

## Cel

Kafelek „Łącznie” nie sugeruje liczby wpisów tam, gdzie liczy dni.

## Kontekst

- Pytanie użytkownika (2026-11-20 13:55): „dlaczego piszesz 5 wpisami, jak było ewidentnie więcej?” — podpis
  „Dni robocze: 5 · z wpisami: 5” czytany jako liczba wpisów; to liczba dni, w których są wpisy.
- Opis kafelków: [F-36 Podsumowania](../../../docs/architektura/funkcje.md).

## Kryteria akceptacji

- [ ] Podpis „Dni robocze: 5 · dni z wpisami: 5” (en: „Working days: 5 · days with entries: 5”).
- [ ] Testy zaktualizowane, wydanie.

## Kroki

- [ ] `sumDaysLine` w `pl.json` i `en.json`, testy.

## Materiały

Brak.

## Dziennik

### 2026-11-20 13:55

- Utworzono zadanie.

## Wynik

<!-- Wypełniane przy zamknięciu: co powstało, gdzie, co zostało na później. -->
