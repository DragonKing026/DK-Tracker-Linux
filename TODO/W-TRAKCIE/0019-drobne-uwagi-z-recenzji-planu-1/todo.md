---
noteId: "bcf5beb0ad794d21b3b5bcbd8c8eb137"
tytul: "Drobne uwagi z recenzji Planu 1 (rdzeń)"
numer: "0019"
status: w-trakcie
priorytet: p3
tags: [todo, core, recenzja]
zalezy_od: ["0018"]
utworzono: 2026-09-25 19:15
zaktualizowano: 2026-09-25 19:44
zamknieto:
---

# 0019 — Drobne uwagi z recenzji Planu 1 (rdzeń)

> [!info] Status
> **w-trakcie** · priorytet **p3** · [← tablica zadań](../../README.md)

## Cel

Zdecydować, które drobne uwagi z końcowej recenzji Planu 1 poprawić (w Planie 2/3 albo
osobno). Recenzja: model opus, cała gałąź `feat/plan-1-rdzen`, werdykt „With fixes”.
Uwagi ważne zostały już poprawione. Poniżej są tylko uwagi odłożone.

## Kontekst

- [Plan 1](../../../docs/plany/2026-09-25-plan-1-rdzen.md), [specyfikacja](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md)
- Kod: [src/kimai_tray/core/](../../../src/kimai_tray/core/)

## Kryteria akceptacji

- [ ] Każda uwaga: poprawiona (test RED→GREEN) albo świadomie odrzucona z uzasadnieniem w dzienniku

## Kroki (uwagi odłożone)

- [x] Pusta/brakująca strefa w `User.from_api` daje "UTC" — **poprawione**: odczyt z `preferences`, potem strefa systemu + ostrzeżenie `warnTimezoneMissing` (decyzja użytkownika: opcja 1 + komunikat)
- [x] ~~Zapasowa strefa to stałe przesunięcie, bez zmiany czasu~~ — **odrzucone z notatką**: ścieżka działa tylko, gdy serwer nie zwraca strefy (Kimai firmy 2.65.0 zwraca); skutek to co najwyżej suma tygodnia przesunięta o godzinę raz w roku. Gdyby aplikacja miała obsługiwać inne serwery: odczytać strefę z dowiązania `/etc/localtime` (np. `Europe/Warsaw`) zamiast stałego przesunięcia z `datetime.now().astimezone()`.
- [x] ~~Uzgodnienie po timeoucie startu nie porównuje minuty początku~~ — **odrzucone z notatką**: wymaga naraz utraconego POST i identycznego wpisu już trwającego (inny klient lub limit > 1); skutek nieszkodliwy — czas liczy się dalej w tamtym wpisie, nic się nie dubluje. Gdyby jednak: w `Tracker._started_anyway` porównać też minutę `begin` z wysłaną (tolerancja na zaokrąglanie Kimai do minut).
- [x] `OSError` przy zapisie pamięci (pełny dysk) wychodzi z odświeżania/startu — **poprawione**: `Tracker._update_memory` loguje ostrzeżenie i trzyma stan w RAM (test `test_memory_that_cannot_be_saved_never_fails_an_action`)
- [x] Każdy 403 traktowany jak zły token — **potwierdzone i poprawione**: Kimai 2.65 zwraca 403 przy edycji wpisu wyeksportowanego i cudzego; 403 → `FORBIDDEN` (`errForbidden`), `Entry.exported` + blokada billable na wyeksportowanym (`errExported`); test kontraktowy na 2.65.0 i 2.67.0
- [x] Przekierowanie 3xx (http→https) pokazywane jako „błąd 301” — **poprawione (wariant b)**: `ErrorKind.REDIRECT` z adresem bazowym z `Location`, komunikat `errRedirect`; bez automatycznego podążania (token nie idzie drugi raz). Plan 3: przycisk „Użyj tego adresu” w ustawieniach
- [x] Sumy na żywo — **poprawione**: (7a) trwający wpis liczony do dnia rozpoczęcia, jak w Kimai; (7b) lekkie odświeżenie przelicza sumy, gdy zmieni się zestaw trwających wpisów
- [ ] Powiadomienie N-01 ma wspólny identyfikator dla kilku długich timerów
- [ ] Nowe (z testów na 2.65.0): preferencja `first_weekday` — sumy tygodnia zawsze od poniedziałku, a konto może mieć niedzielę
- [ ] [funkcje.md](../../../docs/architektura/funkcje.md) F-12 opisuje stronicowanie 100×3, kod używa 500×10

## Materiały

## Dziennik

### 2026-09-25 19:15
- Utworzono z listy „minor (deferred)” końcowej recenzji Planu 1.
- **19:20** Przegląd uwag z użytkownikiem, po kolei.
- **19:26** Uwaga 1: poprawiona (commit „fix(core): brak strefy z Kimai…”). Kimai firmy 2.65.0 — testy kontraktowe 8/8 na tej wersji; znaleziono `first_weekday`.
- **19:30** Uwaga 2: odrzucona z notatką (decyzja użytkownika) — nie dotyczy serwera firmy.
- **19:32** Uwaga 3: odrzucona z notatką (decyzja użytkownika).
- **19:34** Uwaga 4: poprawiona (TDD, 159 testów zielonych).
- **19:37** Uwaga 5: sprawdzona na Kimai 2.65.0 w Dockerze (403 dla wyeksportowanego i cudzego wpisu, 401 dla złego tokenu) i poprawiona.
- **19:39** Uwaga 6: poprawiona wariantem (b) — rozpoznanie przekierowania i podanie nowego adresu.
- **19:44** Uwaga 7: poprawiona (obie części), 170 testów zielonych.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
