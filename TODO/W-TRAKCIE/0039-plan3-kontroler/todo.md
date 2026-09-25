---
noteId: "c6c96eb07ed54d74bec84e16bde6aba1"
tytul: "Plan 3 · Zadanie 11: Kontroler aplikacji (`ui/app.py`)"
numer: "0039"
status: w-trakcie
priorytet: p1
tags: [todo, plan-3, ui]
zalezy_od: ["0038"]
utworzono: 2026-09-25 23:07
zaktualizowano: 2026-09-25 23:10
---

# 0039 — Plan 3 · Zadanie 11: Kontroler aplikacji (`ui/app.py`)

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 11** z [Planu 3: Interfejs Qt](../../../docs/plany/2026-09-25-plan-3-ui.md)
(sekcja „Task 11: Kontroler aplikacji (`ui/app.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-3-ui.md](../../../docs/plany/2026-09-25-plan-3-ui.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md); decyzje UI: [0028](../../ZROBIONE/0028-plan3-projekt-ui/todo.md).
- Pliki:
- Modify: `src/kimai_tray/core/settings.py` (`Memory.tray_hint_shown`), `src/kimai_tray/core/tracker.py` (`Tracker.remember`)
- Modify: `tests/core/test_tracker_refresh.py`
- Create: `src/kimai_tray/ui/app.py`
- Test: `tests/ui/test_app.py`

## Kryteria akceptacji

- [ ] Każdy test z zadania napisany przed kodem i widziany jako padający
- [ ] Wynik planu: 14 PASS, całość 328.
- [ ] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [ ] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [ ] Step 1: Napisz test rdzenia (padający)
- [ ] Step 2: Rdzeń
- [ ] Step 3: Napisz testy kontrolera (padające)
- [ ] Step 4: Uruchom — mają paść
- [ ] Step 5: Zaimplementuj
- [ ] Step 6: Uruchom — mają przejść
- [ ] Step 7: Commit

## Materiały

## Dziennik

### 2026-09-25
- **23:07** Utworzono zadanie z Planu 3.
- **23:10** Start wykonania.
