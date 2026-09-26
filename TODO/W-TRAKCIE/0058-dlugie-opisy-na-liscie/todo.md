---
noteId: "e7c381289b2d47b39a7f1bbda6303b95"
tytul: "Długie opisy na liście ostatnich wpisów: 2,5 linii i rozwijanie kliknięciem"
numer: "0058"
status: w-trakcie
priorytet: p1
tags: [todo, ui, lista-wpisow]
zalezy_od: []
utworzono: 2026-09-26 13:16
zaktualizowano: 2026-09-26 13:16
zamknieto:
---

# 0058 — Długie opisy na liście ostatnich wpisów: 2,5 linii i rozwijanie kliknięciem

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Długi opis wpisu na liście ([F-08](../../../docs/architektura/funkcje.md#f-08-lista-ostatnich-wpisów)) ma pokazywać
pierwsze 2,5 linii od góry, a kliknięcie w wiersz — rozwijać cały tekst (drugie kliknięcie zwija).

## Kontekst

- Test na żywo wersji 0.9.0 ([0053](../0053-plan4-pierwsze-wydanie/todo.md)): opisy ucięte z góry i z dołu — etykieta ma
  stałą wysokość dwóch linii, a tekst jest wyśrodkowany w pionie.
- Wtyczka ([kimai-ws-tracker](../../../docs/integracje/kimai-ws-tracker.md), `popup.css` `.entry .desc`): dwie linie
  (`-webkit-line-clamp: 2`), pełny tekst w dymku, bez rozwijania. Rozwijanie to prośba użytkownika.

Zrzut od użytkownika nie trafia do repozytorium — pokazuje prawdziwe firmowe wpisy, a repozytorium jest publiczne.

## Kryteria akceptacji

- [ ] Opis wyrównany do góry, widoczne najwyżej 2,5 linii
- [ ] Kliknięcie w wiersz rozwija i zwija opis; stan przetrwa odświeżenie listy
- [ ] Testy (TDD), dokumentacja F-08, pełny zestaw kontroli z CI

## Kroki

- [ ] Testy padające
- [ ] Implementacja w `ui/recent.py`
- [ ] Dokumentacja

## Materiały

Brak (zrzut zgłoszenia zawiera firmowe dane — poza repozytorium).

## Dziennik

### 2026-09-26

- **13:16** Utworzono i start.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
