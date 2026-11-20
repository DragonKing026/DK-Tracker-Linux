---
noteId: "f415fb7f99f94a3e9173f2f08e203ad7"
tytul: "Kółko przewija kalendarz, Alt + kółko przybliża"
numer: "0089"
status: do-zrobienia
priorytet: p2
tags: [todo, kalendarz]
zalezy_od: ["0079-skala-kalendarza"]
utworzono: 2026-11-20 12:55
zaktualizowano: 2026-11-20 12:55
zamknieto:
---

# 0089 — Kółko przewija kalendarz, Alt + kółko przybliża

> [!info] Status
> **do-zrobienia** · priorytet **p2** · [← tablica zadań](../../README.md)

## Cel

W kalendarzu samo kółko myszy (i przewijanie touchpadem) przesuwa godziny w górę i w dół, a przybliżanie i oddalanie
skali działa dopiero z Alt + kółko.

## Kontekst

- Prośba użytkownika (2026-11-20 12:55): samo kółko przybliżające przeszkadza — ma przewijać jak wszędzie indziej.
- Od [0079](../../ZROBIONE/0079-skala-kalendarza/todo.md) (0.10.15) samo kółko przybliża, bo Ctrl + kółko nie
  działało wtedy na KDE.
- Opis funkcji: [F-37 Kalendarz](../../../docs/architektura/funkcje.md#f-37-kalendarz-0105),
  [wygląd okna głównego](../../../docs/architektura/wyglad-okna-glownego.md).

## Kryteria akceptacji

- [ ] Kółko i touchpad bez modyfikatora przewijają siatkę godzin (bez zmiany skali).
- [ ] Alt + kółko przybliża i oddala, godzina pod kursorem zostaje na miejscu (także gdy Qt poda Alt + kółko jako
  przewijanie poziome).
- [ ] Prawy przycisk dalej przeciąga godziny.
- [ ] Testy i dokumentacja zaktualizowane, wydanie dla `flatpak update`.

## Kroki

- [ ] `CalendarView.qml`: `onWheel` — bez Alt przewija, z Alt przybliża.
- [ ] Test w `tests/ui/main_window/test_window.py`.
- [ ] Dokumentacja: F-37, wygląd okna, komentarze w kodzie.
- [ ] Wydanie.

## Materiały

Brak.

## Dziennik

### 2026-11-20 12:55

- Utworzono zadanie.

## Wynik

<!-- Wypełniane przy zamknięciu: co powstało, gdzie, co zostało na później. -->
