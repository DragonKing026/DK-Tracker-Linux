---
noteId: "ce20d9b12f1d4093906f58ad5b32edec"
tytul: "Plan 2 — rozpoznanie API integracji desktopowych"
numer: "0021"
status: zrobione
priorytet: p1
tags: [todo, plan-2, spike]
zalezy_od: ["0004"]
utworzono: 2026-09-25 20:46
zaktualizowano: 2026-09-25 21:06
zamknieto: 2026-09-25 21:06
---

# 0021 — Plan 2: rozpoznanie API integracji desktopowych

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Sprawdzić na żywo Secret Service, portal Notification i portal Background (host i Flatpak),
zanim powstanie Plan 2 z gotowym kodem.

## Kryteria akceptacji

- [x] Secret Service: pełny cykl, także z piaskownicy (z uprawnieniem i bez)
- [x] Notification: powiadomienie z przyciskami i powrót kliknięcia (host i Flatpak)
- [x] Background: RequestBackground i SetStatus (host i Flatpak), bez zmiany autostartu
- [x] Plan 2 napisany na podstawie wyników — [plan](../../../docs/plany/2026-09-25-plan-2-desktop.md), kod zweryfikowany
      ([raport](testy/weryfikacja-planu-2.md))

## Materiały

- [notatki/rozpoznanie.md](notatki/rozpoznanie.md) — wyniki
- [testy/weryfikacja-planu-2.md](testy/weryfikacja-planu-2.md) — kod Planu 2 uruchomiony: 206 testów + 3 na sesji D-Bus
- [prototyp/](prototyp/) — skrypty prób (do wyrzucenia)

## Dziennik

### 2026-09-25

- **20:46** Próby wykonane; użytkownik klikał przyciski powiadomień (host i Flatpak).
- **20:51** Plan 2 napisany i zweryfikowany (206 + 3 testy).
- **21:06** Zamknięte: rozpoznanie wykorzystane w Planie 2 (wykonany, zadania 0022–0026).

## Wynik

<!-- Wypełniane przy zamknięciu. -->
