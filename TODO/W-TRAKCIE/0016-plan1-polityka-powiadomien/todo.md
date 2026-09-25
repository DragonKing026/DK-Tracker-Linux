---
noteId: "334617b0cc8843ec8aa4f7b49acb3c3b"
tytul: "Plan 1 · Zadanie 12: Polityka powiadomień (`notification_policy.py`, F-21)"
numer: "0016"
status: w-trakcie
priorytet: p1
tags: [todo, plan-1, core]
zalezy_od: ["0015"]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
zamknieto:
---

# 0016 — Plan 1 · Zadanie 12: Polityka powiadomień (`notification_policy.py`, F-21)

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 12** z [Planu 1: Rdzeń](../../../docs/plany/2026-09-25-plan-1-rdzen.md)
(sekcja „Task 12: Polityka powiadomień (`notification_policy.py`, F-21)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-1-rdzen.md](../../../docs/plany/2026-09-25-plan-1-rdzen.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Pliki:
- Create: `src/kimai_tray/core/notification_policy.py`
- Test: `tests/core/test_notification_policy.py`

## Kryteria akceptacji

- [ ] Każdy test z zadania napisany przed kodem i widziany jako padający
- [ ] `.venv/bin/pytest tests/core/test_notification_policy.py -v` → 9 PASS. Uruchom też `tests/core/test_i18n.py` — nowe klucze (`notif…`) muszą istnieć w locales (są od zadania 9).
- [ ] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [ ] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [ ] Step 1: Napisz testy (padające) `tests/core/test_notification_policy.py`
- [ ] Step 2: Uruchom — mają paść
- [ ] Step 3: Zaimplementuj `src/kimai_tray/core/notification_policy.py`
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
