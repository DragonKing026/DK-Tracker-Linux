---
noteId: "df9d20ca04ba457db62171868387c014"
tytul: "Własna ikona i nazwa „WS Tracker” w 0.9.1"
numer: "0063"
status: zrobione
priorytet: p1
tags: [todo, ikona, nazwa, wydanie]
zalezy_od: ["0062"]
utworzono: 2026-09-26 13:45
zaktualizowano: 2026-09-26 13:59
zamknieto: 2026-09-26 13:59
---

# 0063 — Własna ikona i nazwa „WS Tracker” w 0.9.1

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Zastąpić logo Kimai własną ikoną i zmienić nazwę wyświetlaną na **WS Tracker** już w wydaniu 0.9.1.

## Kontekst

- [Zasady znaku towarowego Kimai](https://www.kimai.org/en/trademark-policy.html): logo wolno pokazać jako „działa z
  Kimai”, ale nie wolno sprawiać wrażenia oficjalnej aplikacji ani powiązania; użycie komercyjne wymaga zgody. Dotąd
  logo Kimai było ikoną aplikacji (menu, pasek tytułu, Discover, nagłówek okna).
- Decyzje użytkownika (2026-09-26 13:45): wariant **C** (ciemny kafel, zielony pierścień postępu, „WS”); nazwa „WS
  Tracker” już
  teraz. Identyfikator, pakiet i komenda zostają do decyzji właściciela
  ([0056](../../W-TRAKCIE/0056-identyfikator-i-wydawca/todo.md),
  [0062](../../DO-ZROBIENIA/0062-aplikacja-ws-tracker/todo.md)).
- Poprawki wariantu C: litery zamienione na krzywe (bez zależności od czcionek), jaśniejsza obwódka kafla (widoczność
  na ciemnym pulpicie).

| Wariant | Podgląd (16–256 px, jasne i ciemne tło) |
| --- | --- |
| A — Stoper | ![A](zrzuty/podglad-a-stoper.png) |
| B — Kafel | ![B](zrzuty/podglad-b-kafel.png) |
| C — WS | ![C](zrzuty/podglad-c-ws.png) |
| **C — wersja końcowa** | ![C końcowa](zrzuty/podglad-c-ws-final.png) |

## Kryteria akceptacji

- [x] Ikona: źródło [data/icons/ws-tracker.svg](../../../data/icons/ws-tracker.svg), PNG 512 px w pakiecie, Flatpak i
  wersja deweloperska; logo Kimai usunięte
- [x] Nazwa „WS Tracker” w oknie, menu, powiadomieniach, portfelu, `.desktop`, MetaInfo, stronie repozytorium, README
- [x] Test ikony (TDD), pełny zestaw kontroli z CI

## Kroki

- [x] Projekt wariantów i wybór
- [x] Ikona i nazwa w kodzie
- [x] Dokumentacja

## Materiały

- Wynik: wydanie v0.9.1 z ikoną WS i nazwą WS Tracker

## Dziennik

### 2026-09-26

- **13:45** Warianty A, B, C; użytkownik wybrał C i nazwę „WS Tracker” w 0.9.1.
- **13:59** Zamknięte: wydanie v0.9.1 z ikoną WS i nazwą WS Tracker, commity na main.

## Wynik

Ikona [ws-tracker.svg](../../../data/icons/ws-tracker.svg) (wariant C, litery jako krzywe) zamiast logo Kimai; nazwa „WS
Tracker” w aplikacji, `.desktop`, MetaInfo, stronie repozytorium i README (z informacją, że to niezależny projekt).
Wydane w [v0.9.1](https://github.com/DragonKing026/WS-Tracker-Linux/releases/tag/v0.9.1); u użytkownika aktualizacja z
nowego adresu repozytorium.
