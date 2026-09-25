---
noteId: "0f0a60889e0d4cefb062b8d4b17b9e45"
tytul: "Plan 2 · Zadanie 2: Token w magazynie sekretów (`desktop/secrets.py`)"
numer: "0023"
status: do-zrobienia
priorytet: p1
tags: [todo, plan-2, desktop]
zalezy_od: ["0022"]
utworzono: 2026-09-25 20:59
zaktualizowano: 2026-09-25 20:59
---

# 0023 — Plan 2 · Zadanie 2: Token w magazynie sekretów (`desktop/secrets.py`)

> [!info] Status
> **do-zrobienia** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 2** z [Planu 2: Integracje desktopowe](../../../docs/plany/2026-09-25-plan-2-desktop.md)
(sekcja „Task 2: Token w magazynie sekretów (`desktop/secrets.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-2-desktop.md](../../../docs/plany/2026-09-25-plan-2-desktop.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Rozpoznanie API: [rozpoznanie.md](../../W-TRAKCIE/0021-plan2-rozpoznanie-api-desktop/notatki/rozpoznanie.md).
- Pliki:
- Create: `src/kimai_tray/desktop/secrets.py`
- Test: `tests/desktop/test_secrets.py`
- Modify: `docs/integracje/jeepney.md`, `docs/integracje/secret-service.md` (sekcje „Gdzie w kodzie”)

## Kryteria akceptacji

- [ ] Każdy test z zadania napisany przed kodem i widziany jako padający
- [ ] Wynik planu: 12 PASS w `test_secrets.py`.
- [ ] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [ ] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [ ] Step 1: Napisz testy (padające) `tests/desktop/test_secrets.py`
- [ ] Step 2: Uruchom — mają paść
- [ ] Step 3: Zaimplementuj `src/kimai_tray/desktop/secrets.py`
- [ ] Step 4: Uruchom — mają przejść
- [ ] Step 5: Dokumentacja
- [ ] Step 6: Commit

## Materiały

## Dziennik

### 2026-09-25
- **20:59** Utworzono zadanie z Planu 2.
