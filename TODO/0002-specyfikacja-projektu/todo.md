---
tytul: "Specyfikacja projektu (design) i plan implementacji"
numer: "0002"
status: w-toku
priorytet: p0
tagi: [todo, planowanie, spec]
zalezy_od: []
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
zamknieto:
---

# 0002 — Specyfikacja projektu i plan implementacji

> [!info] Status
> **w-toku** · priorytet **p0** · [← tablica zadań](../README.md)

## Cel

Razem z użytkownikiem doprecyzować, co dokładnie budujemy w wersji 1.0, i zapisać
zatwierdzoną specyfikację, a potem szczegółowy plan implementacji w małych krokach.

## Kontekst

- Punkt wyjścia: [Przegląd](../../docs/architektura/przeglad.md), [Katalog funkcji](../../docs/architektura/funkcje.md),
  [szkic architektury](../../docs/architektura/architektura-aplikacji.md).
- Proces: pytania → 2–3 podejścia → projekt w sekcjach → spec → akceptacja → plan.

## Kryteria akceptacji

- [x] Ustalony zakres 1.0: F-20, F-21, F-22 wchodzą; F-23, F-24 później
- [x] Zatwierdzony stos ([0003](../DONE/0003-wybor-stosu/todo.md) → [ADR-0002](../../docs/decyzje/0002-stos-python-pyside6.md): Python + PySide6)
- [x] Zatwierdzona forma okna na Waylandzie ([ADR-0003](../../docs/decyzje/0003-okno-szybkiej-obslugi-na-wayland.md))
- [ ] Spec zapisana w `docs/specyfikacja/` i zaakceptowana przez użytkownika
- [ ] Sekcja „Komendy” w [AGENTS.md](../../AGENTS.md) zaplanowana (uzupełniana przy szkielecie projektu)
- [ ] Plan implementacji zapisany i zaakceptowany; kolejne zadania TODO z planu utworzone

## Kroki

- [ ] Pytania o cel i zakres (jedno na raz)
- [ ] Propozycje podejść z rekomendacją
- [ ] Projekt w sekcjach: architektura, komponenty, przepływ danych, błędy, testy
- [ ] Spec + samoprzegląd
- [ ] Plan implementacji

## Dziennik

### 2026-09-25
- Utworzono zadanie.
- Rozpoczęto brainstorming. Pytanie 1 (stos) → Python + PySide6 ([ADR-0002](../../docs/decyzje/0002-stos-python-pyside6.md)).
- Pytanie 2 (okno) → wariant A + menu kontekstowe, B do prototypu ([ADR-0003](../../docs/decyzje/0003-okno-szybkiej-obslugi-na-wayland.md), [0004](../0004-prototyp-tacki-i-okna/todo.md)).
- Pytanie 3 (zakres) → autostart i powiadomienia w 1.0; bezczynność i skrót później.
- Pytanie 4 (powiadomienia) → długi timer, utrata połączenia, potwierdzenie z menu.

## Wynik
