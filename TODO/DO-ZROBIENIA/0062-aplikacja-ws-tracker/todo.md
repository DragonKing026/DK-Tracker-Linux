---
noteId: "75c0a97a82984fe68a7831e3c92c54a9"
tytul: "0.9.2: pełna aplikacja „DK Tracker”, tacka jako opcja — do omówienia"
numer: "0062"
status: pomysl
priorytet: p2
tags: [todo, pomysl, nazwa, ui, wydanie]
zalezy_od: ["0056"]
utworzono: 2026-09-26 13:32
zaktualizowano: 2026-09-26 16:48
zamknieto:
---

# 0062 — 0.9.2: pełna aplikacja „DK Tracker”, tacka jako opcja — do omówienia

> [!info] Status
> **pomysl** · priorytet **p2** · [← tablica zadań](../../README.md)

## Cel

Pomysł użytkownika (2026-09-26 13:32): od wersji 0.9.2 aplikacja ma być przede wszystkim **aplikacją dla Kimai** (okno w
menu i
na pasku zadań), a tacka — opcją. Nazwa bez „Tray”: **DK Tracker**.

## Kontekst

- Zmiana nazwy łączy się z identyfikatorem i wydawcą ([0056](../../ZROBIONE/0056-identyfikator-i-wydawca/todo.md)):
  najlepiej jedna zmiana (nazwa + identyfikator), jedna ponowna instalacja u użytkowników.
- „WS Tracker” to też nazwa wtyczki ([kimai-ws-tracker](../../../docs/integracje/kimai-ws-tracker.md)) — do rozważenia
  przy decyzji (spójność vs pomylenie).
- Pomysły z [podobnych aplikacji](../../../docs/architektura/podobne-aplikacje.md) (F-25…F-32) jako kandydaci do
  „wersji głównej”.

## Do omówienia z użytkownikiem

- [ ] Co ma być w głównym oknie aplikacji (zakres „wersji głównej”)
- [ ] Wzorzec („tak jak w …” — którą aplikację użytkownik miał na myśli)
- [ ] Tacka: domyślnie włączona czy wyłączona; co gdy okno zamknięte
- [ ] Nazwa „DK Tracker” i identyfikator (razem z 0056)

## Minutnik (decyzja użytkownika 2026-09-26)

Wzór: „pigułka” z ikoną i czasem, np. `⏸ 00:02` (jak wskaźnik nagrywania w panelu KDE). W 0.9.2:

- [ ] **GNOME:** czas jako napis przy ikonie w tacce (AppIndicator `XAyatanaLabel` — GNOME/Ubuntu go pokazują).
- [ ] **KDE:** tacka zostaje jak dziś (kwadratowa ikona z czasem — Plasma nie pokazuje napisu SNI, brak
  `XAyatanaLabel` w plasma-workspace). Dodatkowo **widżet panelu** (plasmoid) z pigułką `⏸ 00:02` — to nie opcja w
  aplikacji: użytkownik sam dodaje widżet do panelu (poprawka użytkownika). Do rozważenia: czy przy widżecie da się
  ukryć ikonę w tacce.
- [ ] Sprawdzić: jak widżet dostaje stan z aplikacji we Flatpaku (D-Bus) i jak się go instaluje.

## Kryteria akceptacji

- [ ] Zakres zapisany jako specyfikacja i plan (brainstorming → spec → plan)

## Kroki

- [ ] Rozmowa o zakresie

## Materiały

- [Specyfikacja 0.10](../../../docs/specyfikacja/2026-09-26-okno-glowne-0.10.md)
- [Plan 5: okno główne (0.10.0)](../../../docs/plany/2026-09-26-plan-5-okno-glowne.md)

## Dziennik

### 2026-09-26

- **13:32** Zapisano pomysł użytkownika do omówienia po wydaniu 0.9.1.
- **16:48** Plan 5 (0.10.0) napisany z prototypu (554 testy, 14 kontraktowych) — do akceptacji.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
