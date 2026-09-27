---
noteId: "c2288cb0e4434bc09f25e23ae16aea64"
tytul: "Plan 6: podsumowania 0.10.3 — wykonanie"
numer: "0070"
status: do-zrobienia
priorytet: p1
tags: [todo, ui, qml, okno-glowne, podsumowania, wydanie]
zalezy_od: ["0069-plan5-okno-glowne"]
utworzono: 2026-09-27 11:41
zaktualizowano: 2026-09-27 11:41
zamknieto:
---

# 0070 — Plan 6: podsumowania 0.10.3 — wykonanie

> [!info] Status
> **do-zrobienia** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Widok **Podsumowania** w oknie głównym według
[specyfikacji 0.10, sekcja 6](../../../docs/specyfikacja/2026-09-26-okno-glowne-0.10.md#6-podsumowania-0103)
i wydanie 0.10.3.

## Kontekst

- Użytkownik (2026-09-27): „Kontynuuj dalszy ciąg implementacji wersji 0.10” — po wydaniu
  [0.10.2](../../ZROBIONE/0069-plan5-okno-glowne/todo.md) kolejny krok to podsumowania.
- Plan: [Plan 6](../../../docs/plany/2026-09-27-plan-6-podsumowania.md).
- Wygląd z tych samych kolorów i kontrolek:
  [wygląd okna głównego](../../../docs/architektura/wyglad-okna-glownego.md).

## Kryteria akceptacji

- [ ] Okresy tydzień / miesiąc / rok / zakres, strzałki ◀ ▶, domyślnie bieżący tydzień
- [ ] Czas łączny, płatne/niepłatne (h i %), średnie na dzień / tydzień / miesiąc, dni z wpisami, norma
- [ ] Wykres słupkowy w kolorach projektów z normą i dymkiem; podział: wykres kołowy + tabela
  (projekt / klient / rodzaj pracy)
- [ ] Norma dzienna w ustawieniach (0 = bez normy)
- [ ] Wyniki zgodne z sumami Kimai dla tego samego okresu (test kontraktowy)
- [ ] Galeria zrzutów w obu motywach sprawdzona przed pokazaniem; PL/EN
- [ ] Testy i ruff czyste, dokumentacja zaktualizowana
- [ ] Test na żywo z użytkownikiem, wydanie 0.10.3 za zgodą użytkownika

## Kroki

- [ ] Plan 6
- [ ] `core/summary.py` — liczenie (TDD)
- [ ] Norma w ustawieniach
- [ ] Most i modele widoku
- [ ] Widok QML i pasek boczny
- [ ] Kontroler: wczytywanie okresu w tle
- [ ] Test kontraktowy
- [ ] Galeria zrzutów
- [ ] Dokumentacja
- [ ] Wersja i wydanie

## Materiały

Brak.

## Dziennik

### 2026-09-27

- **11:41** Utworzono zadanie.

## Wynik

<!-- Wypełniane przy zamknięciu: co powstało, gdzie, co zostało na później. -->
