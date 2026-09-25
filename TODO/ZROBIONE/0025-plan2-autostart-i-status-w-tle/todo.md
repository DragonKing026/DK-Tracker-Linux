---
noteId: "e710c5dd027342bb8c2ebfaae3d8bdcb"
tytul: "Plan 2 · Zadanie 4: Autostart i status w tle (`desktop/autostart.py`)"
numer: "0025"
status: zrobione
priorytet: p1
tags: [todo, plan-2, desktop]
zalezy_od: ["0022"]
utworzono: 2026-09-25 20:59
zaktualizowano: 2026-09-25 21:02
zamknieto: 2026-09-25 21:02
---

# 0025 — Plan 2 · Zadanie 4: Autostart i status w tle (`desktop/autostart.py`)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 4** z [Planu 2: Integracje desktopowe](../../../docs/plany/2026-09-25-plan-2-desktop.md)
(sekcja „Task 4: Autostart i status w tle (`desktop/autostart.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-2-desktop.md](../../../docs/plany/2026-09-25-plan-2-desktop.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Rozpoznanie API: [rozpoznanie.md](../0021-plan2-rozpoznanie-api-desktop/notatki/rozpoznanie.md).
- Pliki:
- Create: `src/kimai_tray/desktop/autostart.py`
- Test: `tests/desktop/test_autostart.py`
- Modify: `docs/integracje/xdg-portale.md` („Gdzie w kodzie”)

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] Wynik planu: 6 PASS.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające) `tests/desktop/test_autostart.py`
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Zaimplementuj `src/kimai_tray/desktop/autostart.py`
- [x] Step 4: Uruchom — mają przejść
- [x] Step 5: Dokumentacja
- [x] Step 6: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg: `206 passed, 9 deselected in 0.14s`

## Dziennik

### 2026-09-25
- **20:59** Utworzono zadanie z Planu 2.
- **21:01** Start wykonania.
- **21:02** Zamknięte: testy zielone (206 passed, 9 deselected in 0.14s), commity na main.

## Wynik

[src/kimai_tray/desktop/autostart.py](../../../src/kimai_tray/desktop/autostart.py): `BackgroundPortal` (`request` przez Request/Response, `set_status` z limitem `STATUS_MAX` = 96 i ignorowaniem odmowy poza piaskownicą), `BackgroundResult`. Testy: [tests/desktop/test_autostart.py](../../../tests/desktop/test_autostart.py) — 6 zielonych. Dokumentacja: [portale XDG](../../../docs/integracje/xdg-portale.md). Bez odchyleń od planu.
