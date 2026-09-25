---
noteId: "766cfe9359684511bdaaf081c236f659"
tytul: "Plan 3 · Zadanie 1: Zależności UI, testy Qt i teksty interfejsu"
numer: "0029"
status: w-trakcie
priorytet: p1
tags: [todo, plan-3, ui]
zalezy_od: ["0028"]
utworzono: 2026-09-25 23:07
zaktualizowano: 2026-09-25 23:07
---

# 0029 — Plan 3 · Zadanie 1: Zależności UI, testy Qt i teksty interfejsu

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 1** z [Planu 3: Interfejs Qt](../../../docs/plany/2026-09-25-plan-3-ui.md)
(sekcja „Task 1: Zależności UI, testy Qt i teksty interfejsu”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-3-ui.md](../../../docs/plany/2026-09-25-plan-3-ui.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md); decyzje UI: [0028](../../ZROBIONE/0028-plan3-projekt-ui/todo.md).
- Pliki:
- Modify: `pyproject.toml`
- Modify: `src/kimai_tray/core/locales/pl.json`, `src/kimai_tray/core/locales/en.json`
- Modify: `tests/core/test_i18n.py` (wzorzec kluczy), `tests/test_architektura.py`
- Create: `tests/ui/__init__.py`, `tests/ui/conftest.py`, `tests/ui/test_i18n_ui.py`

## Kryteria akceptacji

- [ ] Każdy test z zadania napisany przed kodem i widziany jako padający
- [ ] Wynik planu: 227 passed.
- [ ] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [ ] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [ ] Step 1: `pyproject.toml`
- [ ] Step 2: Napisz testy (padające)
- [ ] Step 3: Uruchom — mają paść
- [ ] Step 4: Dopisz teksty
- [ ] Step 5: Uruchom — mają przejść
- [ ] Step 6: Commit

## Materiały

## Dziennik

### 2026-09-25
- **23:07** Utworzono zadanie z Planu 3.
- **23:07** Start wykonania (Native, na main).
