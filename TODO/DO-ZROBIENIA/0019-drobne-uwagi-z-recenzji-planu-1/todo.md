---
noteId: "bcf5beb0ad794d21b3b5bcbd8c8eb137"
tytul: "Drobne uwagi z recenzji Planu 1 (rdzeń)"
numer: "0019"
status: pomysl
priorytet: p3
tags: [todo, core, recenzja]
zalezy_od: ["0018"]
utworzono: 2026-09-25 19:15
zaktualizowano: 2026-09-25 19:15
zamknieto:
---

# 0019 — Drobne uwagi z recenzji Planu 1 (rdzeń)

> [!info] Status
> **pomysl** · priorytet **p3** · [← tablica zadań](../../README.md)

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

- [ ] Pusta/brakująca strefa w `User.from_api` daje "UTC" zamiast strefy systemu + flagi różnicy (niespójność w planie; Kimai zawsze wysyła strefę)
- [ ] Zapasowa strefa to stałe przesunięcie, bez zmiany czasu (tylko gdy strefa Kimai nieznana) — np. `ZoneInfo("localtime")`
- [ ] Uzgodnienie po timeoucie startu porównuje projekt/czynność/opis, ale nie minutę początku
- [ ] `OSError` przy zapisie pamięci (pełny dysk) wychodzi z odświeżania/startu
- [ ] Każdy 403 traktowany jak zły token — sprawdzić na Kimai w Dockerze 403 przy edycji zablokowanego/wyeksportowanego wpisu
- [ ] Przekierowanie 3xx (http→https) pokazywane jako „błąd 301”
- [ ] Sumy na żywo: cały czas trwającego wpisu dodawany do „dziś/tydzień”, nawet gdy zaczął się wczoraj; `refresh_active` nie przelicza sum
- [ ] Powiadomienie N-01 ma wspólny identyfikator dla kilku długich timerów
- [ ] [funkcje.md](../../../docs/architektura/funkcje.md) F-12 opisuje stronicowanie 100×3, kod używa 500×10

## Materiały

## Dziennik

### 2026-09-25 19:15
- Utworzono z listy „minor (deferred)” końcowej recenzji Planu 1.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
