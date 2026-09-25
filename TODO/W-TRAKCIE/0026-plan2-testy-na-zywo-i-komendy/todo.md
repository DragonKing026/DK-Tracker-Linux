---
noteId: "51d0d91f2b0040b481aff5ee331921d1"
tytul: "Plan 2 · Zadanie 5: Testy na prawdziwej sesji i komendy"
numer: "0026"
status: w-trakcie
priorytet: p1
tags: [todo, plan-2, desktop]
zalezy_od: ["0023", "0024", "0025"]
utworzono: 2026-09-25 20:59
zaktualizowano: 2026-09-25 21:02
---

# 0026 — Plan 2 · Zadanie 5: Testy na prawdziwej sesji i komendy

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 5** z [Planu 2: Integracje desktopowe](../../../docs/plany/2026-09-25-plan-2-desktop.md)
(sekcja „Task 5: Testy na prawdziwej sesji i komendy”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-2-desktop.md](../../../docs/plany/2026-09-25-plan-2-desktop.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Rozpoznanie API: [rozpoznanie.md](../0021-plan2-rozpoznanie-api-desktop/notatki/rozpoznanie.md).
- Pliki:
- Create: `tests/desktop/test_na_zywo.py`
- Modify: `AGENTS.md` (sekcja „Komendy”)

## Kryteria akceptacji

- [ ] Każdy test z zadania napisany przed kodem i widziany jako padający
- [ ] Wynik planu: 3 PASS (`pytest -m desktop`).
- [ ] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [ ] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [ ] Step 1: Napisz testy `tests/desktop/test_na_zywo.py`
- [ ] Step 2: Uruchom testy na sesji
- [ ] Step 3: `AGENTS.md` → „Komendy”
- [ ] Step 4: Commit

## Materiały

## Dziennik

### 2026-09-25
- **20:59** Utworzono zadanie z Planu 2.
- **21:02** Start wykonania.
