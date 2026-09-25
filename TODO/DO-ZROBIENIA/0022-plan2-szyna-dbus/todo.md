---
noteId: "ca9fa6d8ee7b40dcb9d4047a17fddb99"
tytul: "Plan 2 · Zadanie 1: Szyna D-Bus (`desktop/bus.py`)"
numer: "0022"
status: do-zrobienia
priorytet: p1
tags: [todo, plan-2, desktop]
zalezy_od: []
utworzono: 2026-09-25 20:59
zaktualizowano: 2026-09-25 20:59
---

# 0022 — Plan 2 · Zadanie 1: Szyna D-Bus (`desktop/bus.py`)

> [!info] Status
> **do-zrobienia** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 1** z [Planu 2: Integracje desktopowe](../../../docs/plany/2026-09-25-plan-2-desktop.md)
(sekcja „Task 1: Szyna D-Bus (`desktop/bus.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-2-desktop.md](../../../docs/plany/2026-09-25-plan-2-desktop.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Rozpoznanie API: [rozpoznanie.md](../../W-TRAKCIE/0021-plan2-rozpoznanie-api-desktop/notatki/rozpoznanie.md).
- Pliki:
- Modify: `pyproject.toml` (zależność `jeepney`)
- Create: `src/kimai_tray/desktop/__init__.py`, `src/kimai_tray/desktop/bus.py`
- Create: `tests/desktop/__init__.py`, `tests/desktop/fakes.py`, `tests/desktop/test_bus.py`

## Kryteria akceptacji

- [ ] Każdy test z zadania napisany przed kodem i widziany jako padający
- [ ] Wynik planu: 5 PASS w `test_bus.py`.
- [ ] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [ ] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [ ] Step 1: Dodaj zależność
- [ ] Step 2: Utwórz pusty `tests/desktop/__init__.py`, a potem fałszywą szynę `tests/desktop/fakes.py`:
- [ ] Step 3: Napisz testy (padające) `tests/desktop/test_bus.py`
- [ ] Step 4: Uruchom — mają paść
- [ ] Step 5: Zaimplementuj `src/kimai_tray/desktop/__init__.py` i `src/kimai_tray/desktop/bus.py`
- [ ] Step 6: Uruchom — mają przejść
- [ ] Step 7: Commit

## Materiały

## Dziennik

### 2026-09-25
- **20:59** Utworzono zadanie z Planu 2.
