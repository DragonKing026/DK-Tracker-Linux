---
noteId: "f415fb7f99f94a3e9173f2f08e203ad7"
tytul: "Kółko przewija kalendarz, Alt + kółko przybliża"
numer: "0089"
status: zrobione
priorytet: p2
tags: [todo, kalendarz]
zalezy_od: ["0079-skala-kalendarza"]
utworzono: 2026-11-20 12:55
zaktualizowano: 2026-11-20 12:58
zamknieto: 2026-11-20 12:58
---

# 0089 — Kółko przewija kalendarz, Alt + kółko przybliża

> [!info] Status
> **zrobione** · priorytet **p2** · [← tablica zadań](../../README.md)

## Cel

W kalendarzu samo kółko myszy (i przewijanie touchpadem) przesuwa godziny w górę i w dół, a przybliżanie i oddalanie
skali działa dopiero z Alt + kółko.

## Kontekst

- Prośba użytkownika (2026-11-20 12:55): samo kółko przybliżające przeszkadza — ma przewijać jak wszędzie indziej.
- Od [0079](../0079-skala-kalendarza/todo.md) (0.10.15) samo kółko przybliża, bo Ctrl + kółko nie
  działało wtedy na KDE.
- Opis funkcji: [F-37 Kalendarz](../../../docs/architektura/funkcje.md#f-37-kalendarz-0105),
  [wygląd okna głównego](../../../docs/architektura/wyglad-okna-glownego.md).

## Kryteria akceptacji

- [x] Kółko i touchpad bez modyfikatora przewijają siatkę godzin (bez zmiany skali).
- [x] Alt + kółko przybliża i oddala, godzina pod kursorem zostaje na miejscu (także gdy Qt poda Alt + kółko jako
  przewijanie poziome).
- [x] Prawy przycisk dalej przeciąga godziny.
- [x] Testy i dokumentacja zaktualizowane, wydanie dla `flatpak update`.

## Kroki

- [x] `CalendarView.qml`: `onWheel` — bez Alt przewija, z Alt przybliża.
- [x] Test w `tests/ui/main_window/test_window.py`.
- [x] Dokumentacja: F-37, wygląd okna, komentarze w kodzie.
- [x] Wydanie.

## Materiały

Brak.

## Dziennik

### 2026-11-20 12:55

- Utworzono zadanie.
- **12:56** Start pracy.
- **12:58** Kod (8ea8886), dokumentacja (fc1216c), wersja 0.10.22; pytest 867 zielonych.

## Wynik

- Kółko i touchpad przewijają siatkę (ząbek — pół godziny, co najmniej 48 px), Alt + kółko przybliża i oddala
  (obie osie): [CalendarView.qml](../../../src/dk_tracker/ui/main_window/qml/CalendarView.qml), commit `8ea8886`.
- Test `test_the_wheel_scrolls_the_calendar_alt_wheel_zooms_and_the_right_button_drags`
  w [test_window.py](../../../tests/ui/main_window/test_window.py); opis w
  [F-37](../../../docs/architektura/funkcje.md#f-37-kalendarz-0105) (`fc1216c`).
- Wydanie 0.10.22.
