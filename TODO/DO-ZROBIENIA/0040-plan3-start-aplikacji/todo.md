---
noteId: "5e43b98d47d14c3dbc337af588bf9fe6"
tytul: "Plan 3 · Zadanie 12: Start aplikacji (`ui/main.py`, `__main__.py`)"
numer: "0040"
status: do-zrobienia
priorytet: p1
tags: [todo, plan-3, ui]
zalezy_od: ["0039"]
utworzono: 2026-09-25 23:07
zaktualizowano: 2026-09-25 23:07
---

# 0040 — Plan 3 · Zadanie 12: Start aplikacji (`ui/main.py`, `__main__.py`)

> [!info] Status
> **do-zrobienia** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 12** z [Planu 3: Interfejs Qt](../../../docs/plany/2026-09-25-plan-3-ui.md)
(sekcja „Task 12: Start aplikacji (`ui/main.py`, `__main__.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-3-ui.md](../../../docs/plany/2026-09-25-plan-3-ui.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md); decyzje UI: [0028](../../ZROBIONE/0028-plan3-projekt-ui/todo.md).
- Pliki:
- Create: `src/kimai_tray/ui/main.py`, `src/kimai_tray/__main__.py`
- Test: `tests/ui/test_main.py`
- Modify: `docs/integracje/qt-pyside6.md` („Gdzie w kodzie”), `docs/architektura/architektura-aplikacji.md`, `docs/architektura/struktura-repozytorium.md`, `AGENTS.md` („Komendy”)

## Kryteria akceptacji

- [ ] Każdy test z zadania napisany przed kodem i widziany jako padający
- [ ] Wynik planu: 6 PASS, całość 334.
- [ ] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [ ] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [ ] Step 1: Napisz testy (padające)
- [ ] Step 2: Uruchom — mają paść
- [ ] Step 3: Zaimplementuj
- [ ] Step 4: Uruchom — mają przejść
- [ ] Step 5: Dokumentacja
- [ ] Step 6: Commit

## Materiały

## Dziennik

### 2026-09-25
- **23:07** Utworzono zadanie z Planu 3.
