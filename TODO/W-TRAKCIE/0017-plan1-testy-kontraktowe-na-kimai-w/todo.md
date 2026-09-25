---
noteId: "a20771111ab44a1289820977eb8b8218"
tytul: "Plan 1 · Zadanie 13: Testy kontraktowe na Kimai w Dockerze"
numer: "0017"
status: w-trakcie
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0016"]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
zamknieto:
---

# 0017 — Plan 1 · Zadanie 13: Testy kontraktowe na Kimai w Dockerze

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 13** z [Planu 1: Rdzeń](../../../docs/plany/2026-09-25-plan-1-rdzen.md)
(sekcja „Task 13: Testy kontraktowe na Kimai w Dockerze”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-1-rdzen.md](../../../docs/plany/2026-09-25-plan-1-rdzen.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Pliki:
- Create: `tests/kimai/__init__.py` (pusty), `tests/kimai/conftest.py`, `tests/kimai/test_kontrakt.py`
- Modify: `docs/integracje/kimai-docker.md` (sekcja „Gdzie w kodzie”)

## Kryteria akceptacji

- [ ] Każdy test z zadania napisany przed kodem i widziany jako padający
- [ ] `.venv/bin/pytest -m kimai -v` → 8 PASS (pierwsze uruchomienie ~30 s na start Kimai). Kontenery są usuwane po testach.
- [ ] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [ ] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [ ] Step 1: Utwórz `tests/kimai/conftest.py`
- [ ] Step 2: Napisz testy `tests/kimai/test_kontrakt.py`
- [ ] Step 3: Sprawdź, że domyślny przebieg ich nie uruchamia
- [ ] Step 4: Uruchom testy kontraktowe (Docker)
- [ ] Step 5: Zaktualizuj `docs/integracje/kimai-docker.md`
- [ ] Step 6: Commit

## Materiały

- `testy/` — wynik końcowego przebiegu testów zadania

## Dziennik

### 2026-09-25
- Utworzono zadanie z Planu 1.
- Start wykonania.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
