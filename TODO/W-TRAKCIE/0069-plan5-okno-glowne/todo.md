---
noteId: "219dea77a68845c5b0e2608a2847dc87"
tytul: "Plan 5: okno główne 0.10.0 — wykonanie"
numer: "0069"
status: w-trakcie
priorytet: p1
tags: [todo, ui, qml, okno-glowne, wydanie]
zalezy_od: ["0062-aplikacja-ws-tracker"]
utworzono: 2026-09-26 17:04
zaktualizowano: 2026-09-26 18:22
zamknieto:
---

# 0069 — Plan 5: okno główne 0.10.0 — wykonanie

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać [Plan 5](../../../docs/plany/2026-09-26-plan-5-okno-glowne.md) według
[specyfikacji 0.10](../../../docs/specyfikacja/2026-09-26-okno-glowne-0.10.md) i wydać 0.10.0.

## Kontekst

- Użytkownik (2026-09-26): „Potem możesz zabierać się za 0.10.0 samodzielnie” — wykonanie w tej sesji, na `main`,
  jedno zbiorcze zadanie zamiast dwunastu (rozstrzygnięcie przy starcie wykonania).
- Pomysł i zakres: [0062](../../DO-ZROBIENIA/0062-aplikacja-ws-tracker/todo.md).

## Kryteria akceptacji

- [x] Zadania 1–11 planu wykonane (TDD), cały zestaw testów zielony (575), ruff czysty
- [x] Testy kontraktowe na Kimai w Dockerze zielone (14)
- [x] Recenzja końcowa całości i poprawki (4 krytyczne, 6 ważnych — poprawione z testami; 7 drobnych odłożonych)
- [ ] Test na żywo z użytkownikiem, wydanie 0.10.0 za zgodą użytkownika (zadanie 12)

## Kroki

- [x] Zadanie 1: klient API
- [x] Zadanie 2: Tracker
- [x] Zadanie 3: ustawienia
- [x] Zadanie 4: lista tygodni
- [x] Zadanie 5: modele
- [x] Zadanie 6: MainBridge
- [x] Zadanie 7: okno w QML
- [x] Zadanie 8: kontroler
- [x] Zadanie 9: opcja tacki
- [x] Zadanie 10: testy kontraktowe
- [x] Zadanie 11: dokumentacja
- [ ] Zadanie 12: wersja i wydanie

## Materiały

Brak.

## Dziennik

### 2026-09-26

- **17:04** Utworzono i start.
- **17:23** Zadania 1–11 zrobione; recenzja końcowa: 4 krytyczne i 6 ważnych uwag poprawionych z testami,
  7 drobnych odłożonych (lista w dzienniku planu). Czeka: test na żywo z użytkownikiem i wydanie 0.10.0.
- **17:51** Test na żywo (użytkownik): ustawienia mają być stroną okna głównego; kolory — tekst zlewał się z tłem
  (na KDE styl `org.kde.desktop` zamiast Basic); pola nie były wyróżnione; „Duplikuj” zbędny. Poprawione: zawsze
  styl Basic, pola jak tekst z ramką po najechaniu, kolorowe ikony, projekt w kolorze projektu, kosz zamiast menu,
  dzień i godziny ręcznego wpisu w drugiej linii, ustawienia jako strona okna (bez osobnego okna). Worktree
  prototypu usunięty.
- **18:22** Drugi test na żywo: kursor rączki, zmiana rozmiaru po kliknięciu Ustawień (`show()` zdejmował
  maksymalizację), opis w wielu liniach (Shift+Enter), zaokrąglone kontrolki, okno edycji ze wszystkimi opcjami
  wpisu (tagi, stawki, pola dodatkowe). Na Kimai w Dockerze: nowy tag od zwykłego konta Kimai pomija bez błędu —
  aplikacja to wykrywa i mówi. Testy: 610 + 17 kontraktowych.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
