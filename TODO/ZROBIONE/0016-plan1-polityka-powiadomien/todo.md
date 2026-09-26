---
noteId: "334617b0cc8843ec8aa4f7b49acb3c3b"
tytul: "Plan 1 · Zadanie 12: Polityka powiadomień (`notification_policy.py`, F-21)"
numer: "0016"
status: zrobione
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0015"]
utworzono: 2026-09-25 18:58
zaktualizowano: 2026-09-25 19:03
zamknieto: 2026-09-25 19:03
---

# 0016 — Plan 1 · Zadanie 12: Polityka powiadomień (`notification_policy.py`, F-21)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 12** z [Planu 1: Rdzeń](../../../docs/plany/2026-09-25-plan-1-rdzen.md)
(sekcja „Task 12: Polityka powiadomień (`notification_policy.py`, F-21)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-1-rdzen.md](../../../docs/plany/2026-09-25-plan-1-rdzen.md) — kod, testy i komendy każdego
  kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Pliki:
- Create: `src/kimai_tray/core/notification_policy.py`
- Test: `tests/core/test_notification_policy.py`

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] `.venv/bin/pytest tests/core/test_notification_policy.py -v` → 9 PASS. Uruchom też `tests/core/test_i18n.py` —
      nowe klucze (`notif…`) muszą istnieć w locales (są od zadania 9).
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające) `tests/core/test_notification_policy.py`
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Zaimplementuj `src/kimai_tray/core/notification_policy.py`
- [x] Step 4: Uruchom — mają przejść
- [x] Step 5: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg: `144 passed in 0.11s`

## Dziennik

### 2026-09-25

- Utworzono zadanie z Planu 1.
- Start wykonania.
- Zamknięte: testy zielone, commity w gałęzi feat/plan-1-rdzen.

## Wynik

[src/kimai_tray/core/notification_policy.py](../../../src/ws_tracker_tray/core/notification_policy.py): N-01 długi timer
(próg + co godzinę), N-02/N-02b połączenie (3 błędy lub od razu przy 401), N-03 potwierdzenie akcji z menu. Czysta
funkcja — bez D-Bus. Testy: [tests/core/test_notification_policy.py](../../../tests/core/test_notification_policy.py) —
9 zielonych. Bez odchyleń.
