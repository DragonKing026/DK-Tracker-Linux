---
noteId: "b5fbe898f17d42b2b9914b094254556e"
tytul: "Plan 4 · Zadanie 3: Manifest Flatpaka i zależności Pythona"
numer: "0048"
status: zrobione
priorytet: p1
tags: [todo, plan-4, flatpak]
zalezy_od: ["0047"]
utworzono: 2026-09-26 11:28
zaktualizowano: 2026-09-26 11:48
zamknieto: 2026-09-26 11:48
---

# 0048 — Plan 4 · Zadanie 3: Manifest Flatpaka i zależności Pythona

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

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

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] Wynik planu: 408 passed, 1 skipped.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające)
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Zaimplementuj
- [x] Step 4: Uruchom — mają przejść
- [x] Step 5: Commit

## Materiały

- [testy/pytest-2026-09-26.txt](testy/pytest-2026-09-26.txt) — końcowy przebieg:
  `408 passed, 1 skipped, 12 deselected in 2.55s`

## Dziennik

### 2026-09-26

- **11:28** Utworzono zadanie z Planu 4.
- **11:48** Start wykonania.
- **11:48** Zamknięte: 408 passed, 1 skipped, 12 deselected in 2.55s, commity na main.

## Wynik

[Manifest](../../../flatpak/io.github.dragonking026.DK-Tracker-Linux.yml) (KDE 6.11, baza PySide, layer-shell-qt 6.7.5,
uprawnienia
ze
specyfikacji) i [zależności Pythona](../../../flatpak/python3-deps.yaml); testy w
[test_pakiet.py](../../../tests/test_pakiet.py). Bez odchyleń od planu.
