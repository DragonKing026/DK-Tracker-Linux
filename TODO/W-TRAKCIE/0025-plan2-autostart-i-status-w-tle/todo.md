---
noteId: "e710c5dd027342bb8c2ebfaae3d8bdcb"
tytul: "Plan 2 · Zadanie 4: Autostart i status w tle (`desktop/autostart.py`)"
numer: "0025"
status: w-trakcie
priorytet: p1
tags: [todo, plan-2, desktop]
zalezy_od: ["0022"]
utworzono: 2026-09-25 20:59
zaktualizowano: 2026-09-25 21:01
---

# 0025 — Plan 2 · Zadanie 4: Autostart i status w tle (`desktop/autostart.py`)

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

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

- [ ] Każdy test z zadania napisany przed kodem i widziany jako padający
- [ ] Wynik planu: 6 PASS.
- [ ] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [ ] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [ ] Step 1: Napisz testy (padające) `tests/desktop/test_autostart.py`
- [ ] Step 2: Uruchom — mają paść
- [ ] Step 3: Zaimplementuj `src/kimai_tray/desktop/autostart.py`
- [ ] Step 4: Uruchom — mają przejść
- [ ] Step 5: Dokumentacja
- [ ] Step 6: Commit

## Materiały

## Dziennik

### 2026-09-25
- **20:59** Utworzono zadanie z Planu 2.
- **21:01** Start wykonania.
