---
noteId: "e5b29f7ef4944b8eb1d5876bd560ddd1"
tytul: "Plan 4 · Zadanie 2: MetaInfo (AppStream) i plik `.desktop`"
numer: "0047"
status: zrobione
priorytet: p1
tags: [todo, plan-4, flatpak]
zalezy_od: ["0046"]
utworzono: 2026-09-26 11:28
zaktualizowano: 2026-09-26 11:48
zamknieto: 2026-09-26 11:48
---

# 0047 — Plan 4 · Zadanie 2: MetaInfo (AppStream) i plik `.desktop`

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 2** z [Planu 4: Flatpak i wydanie](../../../docs/plany/2026-09-26-plan-4-flatpak.md)
(sekcja „Task 2: MetaInfo (AppStream) i plik `.desktop`”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-26-plan-4-flatpak.md](../../../docs/plany/2026-09-26-plan-4-flatpak.md) — kod, testy i komendy każdego
  kroku.
- Specyfikacja: [WS Tracker Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md); decyzje:
  [0045](../../W-TRAKCIE/0045-plan4-projekt-flatpak/todo.md).
- Pliki:

- Create: `data/pl.websystems.WsTrackerTray.metainfo.xml`
- Modify: `tests/test_pakiet.py`
- Uses: `data/pl.websystems.WsTrackerTray.desktop`, `docs/assets/zrzuty/okno-ciemny-motyw.png` (już w repozytorium)

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] Wynik planu: 403 passed, 1 skipped.
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
  `403 passed, 1 skipped, 12 deselected in 2.44s`

## Dziennik

### 2026-09-26

- **11:28** Utworzono zadanie z Planu 4.
- **11:30** Start wykonania.
- **11:48** Zamknięte: 403 passed, 1 skipped, 12 deselected in 2.44s, commity na main.

## Wynik

[MetaInfo](../../../data/pl.websystems.WsTrackerTray.metainfo.xml) (PL/EN, wydanie 0.9.0, zrzut z repozytorium) i testy
w [test_pakiet.py](../../../tests/test_pakiet.py). Po zadaniu zmiana nazwy na WS Tracker Tray
([0055](../0055-zmiana-nazwy-ws-tracker-tray/todo.md)).
