---
noteId: "f2457ebe5b9e4815b0a6468cafa8514e"
tytul: "Plan 7: kalendarz 0.10.5 — wykonanie"
numer: "0073"
status: w-trakcie
priorytet: p1
tags: [todo, ui, qml, okno-glowne, kalendarz, wydanie]
zalezy_od: ["0070-plan6-podsumowania"]
utworzono: 2026-09-27 13:13
zaktualizowano: 2026-09-27 13:13
zamknieto:
---

# 0073 — Plan 7: kalendarz 0.10.5 — wykonanie

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Widok **Kalendarz** w oknie głównym według
[specyfikacji 0.10, sekcja 8](../../../docs/specyfikacja/2026-09-26-okno-glowne-0.10.md#8-kalendarz-0105) i wydanie
0.10.5.

## Kontekst

- Użytkownik (2026-09-27, po wydaniu 0.10.4): „Możesz iść dalej”.
- Plan: [Plan 7](../../../docs/plany/2026-09-27-plan-7-kalendarz.md). Wygląd:
  [wygląd okna głównego](../../../docs/architektura/wyglad-okna-glownego.md).

## Kryteria akceptacji

- [ ] Dzień / tydzień (5 lub 7 dni), ◀ ▶, „Dziś”; siatka 0–24 przewinięta na godziny pracy; linia „teraz”
- [ ] Bloki w kolorach projektów, trwający rośnie na żywo, nakładające się obok siebie, wyeksportowane z kłódką
- [ ] Przeciągnięcie w pustym miejscu → nowy wpis z dymka; krawędź → godziny; blok → przesunięcie (też na inny dzień)
- [ ] Klik w blok → dymek z „Usuń” i „Wznów”; odmowa Kimai → blok wraca, komunikat
- [ ] Przyciąganie co 15 min, Alt wyłącza
- [ ] Test kontraktowy przesunięcia na inny dzień; galeria w obu motywach; PL/EN; dokumentacja
- [ ] Test na żywo z użytkownikiem, wydanie 0.10.5

## Kroki

- [ ] Plan 7
- [ ] Rdzeń: `core/calendar.py` (dni, układ bloków, przyciąganie) i `Tracker.reschedule`
- [ ] `CalendarPage` (`app.calendarPage`)
- [ ] Widok QML: siatka, bloki, przeciąganie, dymek
- [ ] Kontroler
- [ ] Test kontraktowy, galeria, dokumentacja
- [ ] Wersja i wydanie

## Materiały

Brak.

## Dziennik

### 2026-09-27

- **13:13** Utworzono i start.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
