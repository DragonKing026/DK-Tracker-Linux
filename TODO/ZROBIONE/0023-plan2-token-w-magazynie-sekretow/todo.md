---
noteId: "0f0a60889e0d4cefb062b8d4b17b9e45"
tytul: "Plan 2 · Zadanie 2: Token w magazynie sekretów (`desktop/secrets.py`)"
numer: "0023"
status: zrobione
priorytet: p1
tags: [todo, plan-2, desktop]
zalezy_od: ["0022"]
utworzono: 2026-09-25 20:59
zaktualizowano: 2026-09-25 21:01
zamknieto: 2026-09-25 21:01
---

# 0023 — Plan 2 · Zadanie 2: Token w magazynie sekretów (`desktop/secrets.py`)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 2** z [Planu 2: Integracje desktopowe](../../../docs/plany/2026-09-25-plan-2-desktop.md)
(sekcja „Task 2: Token w magazynie sekretów (`desktop/secrets.py`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-2-desktop.md](../../../docs/plany/2026-09-25-plan-2-desktop.md) — kod, testy i komendy każdego
  kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Rozpoznanie API: [rozpoznanie.md](../0021-plan2-rozpoznanie-api-desktop/notatki/rozpoznanie.md).
- Pliki:
- Create: `src/kimai_tray/desktop/secrets.py`
- Test: `tests/desktop/test_secrets.py`
- Modify: `docs/integracje/jeepney.md`, `docs/integracje/secret-service.md` (sekcje „Gdzie w kodzie”)

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] Wynik planu: 12 PASS w `test_secrets.py`.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające) `tests/desktop/test_secrets.py`
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Zaimplementuj `src/kimai_tray/desktop/secrets.py`
- [x] Step 4: Uruchom — mają przejść
- [x] Step 5: Dokumentacja
- [x] Step 6: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg: `192 passed, 9 deselected in 0.13s`

## Dziennik

### 2026-09-25

- **20:59** Utworzono zadanie z Planu 2.
- **21:00** Start wykonania.
- **21:01** Zamknięte: testy zielone (192 passed, 9 deselected in 0.13s), commity na main.

## Wynik

[src/kimai_tray/desktop/secrets.py](../../../src/ws_tracker_tray/desktop/secrets.py): `SecretServiceStore`
(get/set/delete,
sesja plain, kolekcja `default`, odblokowanie przez prompt), `SecretsUnavailable`, `SecretsLocked`. Testy:
[tests/desktop/test_secrets.py](../../../tests/desktop/test_secrets.py) — 12 zielonych. Dokumentacja:
[jeepney](../../../docs/integracje/jeepney.md), [Secret Service](../../../docs/integracje/secret-service.md). Bez
odchyleń od planu.
