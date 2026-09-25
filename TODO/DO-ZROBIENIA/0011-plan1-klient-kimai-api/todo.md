---
noteId: "1e38a0c0d3ef45f7906f7c801d1f2a66"
tytul: "Plan 1 · Zadanie 7: Klient Kimai API (`kimai_client.py`)"
numer: "0011"
status: do-zrobienia
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0010"]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
zamknieto:
---

# 0011 — Plan 1 · Zadanie 7: Klient Kimai API (`kimai_client.py`)

> [!info] Status
> **do-zrobienia** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 7** z [Planu 1: Rdzeń](../../../docs/plany/2026-09-25-plan-1-rdzen.md)
(sekcja „Task 7: Klient Kimai API (`kimai_client.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-1-rdzen.md](../../../docs/plany/2026-09-25-plan-1-rdzen.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Pliki:
- Create: `src/kimai_tray/core/kimai_client.py`
- Test: `tests/core/test_kimai_client.py`
- Modify: `docs/integracje/kimai-api.md` (sekcja „Gdzie w kodzie”), `docs/integracje/httpx.md` (sekcja „Gdzie w kodzie” — dopisz)

## Kryteria akceptacji

- [ ] Każdy test z zadania napisany przed kodem i widziany jako padający
- [ ] `.venv/bin/pytest tests/core/test_kimai_client.py -v` → 12 PASS.
- [ ] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [ ] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [ ] Step 1: Napisz testy (padające)
- [ ] Step 2: Uruchom — mają paść
- [ ] Step 3: Zaimplementuj `src/kimai_tray/core/kimai_client.py`
- [ ] Step 4: Uruchom — mają przejść
- [ ] Step 5: Zaktualizuj dokumentację integracji
- [ ] Step 6: Commit

## Materiały

- `testy/` — wynik końcowego przebiegu testów zadania

## Dziennik

### 2026-09-25
- Utworzono zadanie z Planu 1.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
