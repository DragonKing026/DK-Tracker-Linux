---
noteId: "ed06088ede9b4cd6bde08145e4692135"
tytul: "Plan 3 · Zadanie 9: Ustawienia (`ui/settings_dialog.py`)"
numer: "0037"
status: zrobione
priorytet: p1
tags: [todo, plan-3, ui]
zalezy_od: ["0036"]
utworzono: 2026-09-25 23:07
zaktualizowano: 2026-09-25 23:10
zamknieto: 2026-09-25 23:10
---

# 0037 — Plan 3 · Zadanie 9: Ustawienia (`ui/settings_dialog.py`)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 9** z [Planu 3: Interfejs Qt](../../../docs/plany/2026-09-25-plan-3-ui.md)
(sekcja „Task 9: Ustawienia (`ui/settings_dialog.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-3-ui.md](../../../docs/plany/2026-09-25-plan-3-ui.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md); decyzje UI:
  [0028](../0028-plan3-projekt-ui/todo.md).
- Pliki:
- Create: `src/kimai_tray/ui/settings_dialog.py`
- Test: `tests/ui/test_settings_dialog.py`

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] Wynik planu: 9 PASS, całość 310.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające)
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Zaimplementuj
- [x] Step 4: Uruchom — mają przejść
- [x] Step 5: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg:
  `310 passed, 1 skipped, 12 deselected in 0.74s`

## Dziennik

### 2026-09-25

- **23:07** Utworzono zadanie z Planu 3.
- **23:10** Start wykonania.
- **23:10** Zamknięte: testy zielone (310 passed, 1 skipped, 12 deselected in 0.74s), commity na main.

## Wynik

[settings_dialog.py](../../../src/ws_tracker_tray/ui/settings_dialog.py): `SettingsDialog`. Testy:
[test_settings_dialog.py](../../../tests/ui/test_settings_dialog.py) — 9 zielonych. Bez odchyleń od planu.
