---
noteId: "0ccfc23427934c40af9f26a3d726fe41"
tytul: "Plan 3 · Zadanie 8: Okno szybkiej obsługi i jego miejsce (`ui/popup.py`, `ui/placement.py`)"
numer: "0036"
status: w-trakcie
priorytet: p1
tags: [todo, plan-3, ui]
zalezy_od: ["0035"]
utworzono: 2026-09-25 23:07
zaktualizowano: 2026-09-25 23:09
---

# 0036 — Plan 3 · Zadanie 8: Okno szybkiej obsługi i jego miejsce (`ui/popup.py`, `ui/placement.py`)

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 8** z [Planu 3: Interfejs Qt](../../../docs/plany/2026-09-25-plan-3-ui.md)
(sekcja „Task 8: Okno szybkiej obsługi i jego miejsce (`ui/popup.py`, `ui/placement.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-3-ui.md](../../../docs/plany/2026-09-25-plan-3-ui.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md); decyzje UI: [0028](../../ZROBIONE/0028-plan3-projekt-ui/todo.md).
- Pliki:
- Create: `src/kimai_tray/ui/popup.py`, `src/kimai_tray/ui/placement.py`
- Test: `tests/ui/test_popup.py`
- Modify: `docs/integracje/layer-shell-qt.md` („Gdzie w kodzie”, „Pułapki”)

## Kryteria akceptacji

- [ ] Każdy test z zadania napisany przed kodem i widziany jako padający
- [ ] Wynik planu: 16 PASS + 1 SKIP, całość 301.
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
- **23:09** Start wykonania.
