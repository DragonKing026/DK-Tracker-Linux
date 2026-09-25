---
noteId: "c4042ac8ba424af58ad7fb0013d79cfb"
tytul: "Plan 1 · Zadanie 8: Ustawienia i pamięć aplikacji (`settings.py`)"
numer: "0012"
status: w-trakcie
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0011"]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
zamknieto:
---

# 0012 — Plan 1 · Zadanie 8: Ustawienia i pamięć aplikacji (`settings.py`)

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 8** z [Planu 1: Rdzeń](../../../docs/plany/2026-09-25-plan-1-rdzen.md)
(sekcja „Task 8: Ustawienia i pamięć aplikacji (`settings.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-1-rdzen.md](../../../docs/plany/2026-09-25-plan-1-rdzen.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Pliki:
- Create: `src/kimai_tray/core/settings.py`
- Test: `tests/core/test_settings.py`

## Kryteria akceptacji

- [ ] Każdy test z zadania napisany przed kodem i widziany jako padający
- [ ] `.venv/bin/pytest tests/core/test_settings.py -v` → 8 PASS.
- [ ] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [ ] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [ ] Step 1: Napisz testy (padające)
- [ ] Step 2: Uruchom — mają paść
- [ ] Step 3: Zaimplementuj `src/kimai_tray/core/settings.py`
- [ ] Step 4: Uruchom — mają przejść
- [ ] Step 5: Commit

## Materiały

- `testy/` — wynik końcowego przebiegu testów zadania

## Dziennik

### 2026-09-25
- Utworzono zadanie z Planu 1.
- Start wykonania.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
