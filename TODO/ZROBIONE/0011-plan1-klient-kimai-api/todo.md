---
noteId: "1e38a0c0d3ef45f7906f7c801d1f2a66"
tytul: "Plan 1 · Zadanie 7: Klient Kimai API (`kimai_client.py`)"
numer: "0011"
status: zrobione
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0010"]
utworzono: 2026-09-25 19:02
zaktualizowano: 2026-09-25 19:02
zamknieto: 2026-09-25 19:02
---

# 0011 — Plan 1 · Zadanie 7: Klient Kimai API (`kimai_client.py`)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 7** z [Planu 1: Rdzeń](../../../docs/plany/2026-09-25-plan-1-rdzen.md)
(sekcja „Task 7: Klient Kimai API (`kimai_client.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-1-rdzen.md](../../../docs/plany/2026-09-25-plan-1-rdzen.md) — kod, testy i komendy każdego
  kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Pliki:
- Create: `src/kimai_tray/core/kimai_client.py`
- Test: `tests/core/test_kimai_client.py`
- Modify: `docs/integracje/kimai-api.md` (sekcja „Gdzie w kodzie”), `docs/integracje/httpx.md` (sekcja „Gdzie w kodzie”
  — dopisz)

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] `.venv/bin/pytest tests/core/test_kimai_client.py -v` → 12 PASS.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające)
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Zaimplementuj `src/kimai_tray/core/kimai_client.py`
- [x] Step 4: Uruchom — mają przejść
- [x] Step 5: Zaktualizuj dokumentację integracji
- [x] Step 6: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg: `76 passed in 0.06s`

## Dziennik

### 2026-09-25

- Utworzono zadanie z Planu 1.
- Start wykonania.
- Zamknięte: testy zielone, commity w gałęzi feat/plan-1-rdzen.

## Wynik

[src/kimai_tray/core/kimai_client.py](../../../src/ws_tracker/core/kimai_client.py): wszystkie endpointy aplikacji,
błędy jako `ApiError`, stronicowanie po `X-Total-Pages` z obsługą 404, `billable` wysyłane tylko gdy podane. Testy:
[tests/core/test_kimai_client.py](../../../tests/core/test_kimai_client.py) — 12 zielonych. Dokumentacja integracji
(kimai-api, httpx) uzupełniona o „Gdzie w kodzie”, status w-uzyciu.
