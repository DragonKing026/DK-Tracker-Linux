---
noteId: "a20771111ab44a1289820977eb8b8218"
tytul: "Plan 1 · Zadanie 13: Testy kontraktowe na Kimai w Dockerze"
numer: "0017"
status: zrobione
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0016"]
utworzono: 2026-09-25 19:04
zaktualizowano: 2026-09-25 19:04
zamknieto: 2026-09-25 19:04
---

# 0017 — Plan 1 · Zadanie 13: Testy kontraktowe na Kimai w Dockerze

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 13** z [Planu 1: Rdzeń](../../../docs/plany/2026-09-25-plan-1-rdzen.md)
(sekcja „Task 13: Testy kontraktowe na Kimai w Dockerze”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-1-rdzen.md](../../../docs/plany/2026-09-25-plan-1-rdzen.md) — kod, testy i komendy każdego
  kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Pliki:
- Create: `tests/kimai/__init__.py` (pusty), `tests/kimai/conftest.py`, `tests/kimai/test_kontrakt.py`
- Modify: `docs/integracje/kimai-docker.md` (sekcja „Gdzie w kodzie”)

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] `.venv/bin/pytest -m kimai -v` → 8 PASS (pierwsze uruchomienie ~30 s na start Kimai). Kontenery są usuwane po
      testach.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Utwórz `tests/kimai/conftest.py`
- [x] Step 2: Napisz testy `tests/kimai/test_kontrakt.py`
- [x] Step 3: Sprawdź, że domyślny przebieg ich nie uruchamia
- [x] Step 4: Uruchom testy kontraktowe (Docker)
- [x] Step 5: Zaktualizuj `docs/integracje/kimai-docker.md`
- [x] Step 6: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg: `144 passed, 8 deselected in 0.11s`
- [testy/pytest-kimai-2026-09-25.log](testy/pytest-kimai-2026-09-25.log) — testy kontraktowe na Kimai 2.67 w Dockerze: 8
  passed w 36,6 s

## Dziennik

### 2026-09-25

- Utworzono zadanie z Planu 1.
- Start wykonania.
- Zamknięte: testy zielone, commity w gałęzi feat/plan-1-rdzen.

## Wynik

[tests/kimai/conftest.py](../../../tests/kimai/conftest.py) (fixture uruchamia Kimai skryptem, trackery
ROLE_USER/ROLE_TEAMLEAD) i [tests/kimai/test_kontrakt.py](../../../tests/kimai/test_kontrakt.py): 8/8 zielonych na
prawdziwym Kimai — strefa czasowa, billable z blokadą, teamlead, auto-stop, sumy, idempotentny stop. Ruling: bez fazy
RED (testy kontraktowe istniejącego kodu).
