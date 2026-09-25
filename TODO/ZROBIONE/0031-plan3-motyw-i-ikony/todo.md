---
noteId: "fa2b80e9295c475a83706cfadca938e2"
tytul: "Plan 3 · Zadanie 3: Motyw i ikony (`ui/theme.py`, `ui/icons.py`)"
numer: "0031"
status: zrobione
priorytet: p1
tags: [todo, plan-3, ui]
zalezy_od: ["0030"]
utworzono: 2026-09-25 23:07
zaktualizowano: 2026-09-25 23:08
zamknieto: 2026-09-25 23:08
---

# 0031 — Plan 3 · Zadanie 3: Motyw i ikony (`ui/theme.py`, `ui/icons.py`)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 3** z [Planu 3: Interfejs Qt](../../../docs/plany/2026-09-25-plan-3-ui.md)
(sekcja „Task 3: Motyw i ikony (`ui/theme.py`, `ui/icons.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-3-ui.md](../../../docs/plany/2026-09-25-plan-3-ui.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md); decyzje UI:
  [0028](../0028-plan3-projekt-ui/todo.md).
- Pliki:
- Create: `src/kimai_tray/ui/__init__.py`, `src/kimai_tray/ui/theme.py`, `src/kimai_tray/ui/icons.py`
- Modify: `pyproject.toml` (wyjątek E501 dla danych SVG/QSS)
- Test: `tests/ui/test_theme_icons.py`

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] Wynik planu: 9 PASS, całość 246.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające)
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Zaimplementuj
- [x] Step 4: Uruchom — mają przejść
- [x] Step 5: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg: `246 passed, 12 deselected in 0.22s`

## Dziennik

### 2026-09-25

- **23:07** Utworzono zadanie z Planu 3.
- **23:08** Start wykonania.
- **23:08** Zamknięte: testy zielone (246 passed, 12 deselected in 0.22s), commity na main.

## Wynik

[theme.py](../../../src/kimai_tray/ui/theme.py) (palety z popup.css, QSS),
[icons.py](../../../src/kimai_tray/ui/icons.py) (ikona tacki — wariant C, glify SVG). Testy:
[test_theme_icons.py](../../../tests/ui/test_theme_icons.py) — 9 zielonych. Bez odchyleń od planu.
