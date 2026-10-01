---
noteId: "00ae916f75594921b0a7814450317a7f"
tytul: "Kalendarz: większa skala od 8:00, przybliżanie Ctrl + kółko"
numer: "0079"
status: w-trakcie
priorytet: p2
tags: [todo, kalendarz, wyglad]
zalezy_od: []
utworzono: 2026-10-01 18:48
zaktualizowano: 2026-10-01 18:48
zamknieto:
---

# 0079 — Kalendarz: większa skala od 8:00, przybliżanie Ctrl + kółko

> [!info] Status
> **w-trakcie** · priorytet **p2** · [← tablica zadań](../../README.md)

## Cel

Kalendarz pokazuje mniej godzin, ale wyraźniej: domyślnie od 8:00 w większej skali, a skalę zmienia się kółkiem
myszy z Ctrl.

## Kontekst

- Uwaga użytkownika (zrzut niżej): na dużym ekranie mieści się cała doba (48 px na godzinę), krótkie wpisy są
  nieczytelne. „Większy rozkład, więcej minut, skupić się na przedziale po 8, powiększenie scrollem”.
- Kalendarz: [F-37](../../../docs/architektura/funkcje.md#f-37-kalendarz-0105),
  [wygląd okna głównego](../../../docs/architektura/wyglad-okna-glownego.md); poprzednie zmiany:
  [0078](../0078-sekundy-w-kalendarzu-i-klik-na-gnome/todo.md).

## Kryteria akceptacji

- [x] Domyślnie 96 px na godzinę, widok od 8:00 (później, gdy „teraz” by nie było widać)
- [x] Ctrl + kółko przybliża i oddala (32–384 px), godzina pod kursorem zostaje; samo kółko przewija jak dotąd
- [x] Skala zapamiętana między uruchomieniami
- [x] Linie co pół godziny przy większej skali
- [x] Testy i dokumentacja zaktualizowane
- [ ] Sprawdzone przez użytkownika

## Kroki

- [x] `zoomed` w [core/calendar.py](../../../src/dk_tracker/core/calendar.py), `hourHeight` i `zoom` w
  [calendar_page.py](../../../src/dk_tracker/ui/main_window/calendar_page.py), `calendar_hour_height` w pamięci
- [x] `CalendarView.qml`: skala, Ctrl + kółko, start od 8:00, linie półgodzinne
- [x] Wydanie

## Materiały

![Przed: cała doba na ekranie](zrzuty/przed-caly-dzien.png)

Po zmianie (render offscreen, 1400 × 800; „teraz” 14:40, więc widok zaczyna się trochę później niż o 8:00):

![Po: skala domyślna](zrzuty/po-skala-domyslna.png)
![Po: Ctrl + kółko, dwa ząbki](zrzuty/po-przyblizeniu.png)

[Skrypt zrzutów](testy/zrzut-skali.py).

## Dziennik

### 2026-10-01 18:48

- Utworzono zadanie i od razu rozpoczęto. Skala w pamięci (`Memory.calendar_hour_height`), zmiana o ćwierć na
  ząbek. Testy: 763 zielone.

## Wynik

<!-- Wypełniane przy zamknięciu: co powstało, gdzie, co zostało na później. -->
