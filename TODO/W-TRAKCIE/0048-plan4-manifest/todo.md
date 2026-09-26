---
noteId: "b5fbe898f17d42b2b9914b094254556e"
tytul: "Plan 4 · Zadanie 3: Manifest Flatpaka i zależności Pythona"
numer: "0048"
status: w-trakcie
priorytet: p1
tags: [todo, plan-4, flatpak]
zalezy_od: ["0047"]
utworzono: 2026-09-26 11:28
zaktualizowano: 2026-09-26 11:48
zamknieto:
---

# 0048 — Plan 4 · Zadanie 3: Manifest Flatpaka i zależności Pythona

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 3** z [Planu 4: Flatpak i wydanie](../../../docs/plany/2026-09-26-plan-4-flatpak.md)
(sekcja „Task 3: Manifest Flatpaka i zależności Pythona”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-26-plan-4-flatpak.md](../../../docs/plany/2026-09-26-plan-4-flatpak.md) — kod, testy i komendy każdego
  kroku.
- Specyfikacja: [WS Tracker Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md); decyzje:
  [0045](../0045-plan4-projekt-flatpak/todo.md).
- Pliki:

- Create: `flatpak/pl.websystems.WsTrackerTray.yml`, `flatpak/python3-deps.yaml`
- Modify: `tests/test_pakiet.py`

## Kryteria akceptacji

- [ ] Każdy test z zadania napisany przed kodem i widziany jako padający
- [ ] Wynik planu: 408 passed, 1 skipped.
- [ ] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [ ] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [ ] Step 1: Napisz testy (padające)
- [ ] Step 2: Uruchom — mają paść
- [ ] Step 3: Zaimplementuj
- [ ] Step 4: Uruchom — mają przejść
- [ ] Step 5: Commit

## Materiały

Brak (materiały pojawią się w podfolderach przy wykonaniu).

## Dziennik

### 2026-09-26

- **11:28** Utworzono zadanie z Planu 4.
- **11:48** Start wykonania.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
