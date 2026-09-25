---
noteId: "b5b81172d3604cc59bc28254eef151bb"
tytul: "Plan 2 · Zadanie 3: Powiadomienia — tekst w rdzeniu, wysyłka przez portal"
numer: "0024"
status: zrobione
priorytet: p1
tags: [todo, plan-2, desktop]
zalezy_od: ["0022"]
utworzono: 2026-09-25 20:59
zaktualizowano: 2026-09-25 21:01
zamknieto: 2026-09-25 21:01
---

# 0024 — Plan 2 · Zadanie 3: Powiadomienia — tekst w rdzeniu, wysyłka przez portal

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 3** z [Planu 2: Integracje desktopowe](../../../docs/plany/2026-09-25-plan-2-desktop.md)
(sekcja „Task 3: Powiadomienia — tekst w rdzeniu, wysyłka przez portal”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-25-plan-2-desktop.md](../../../docs/plany/2026-09-25-plan-2-desktop.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md).
- Rozpoznanie API: [rozpoznanie.md](../../W-TRAKCIE/0021-plan2-rozpoznanie-api-desktop/notatki/rozpoznanie.md).
- Pliki:
- Modify: `src/kimai_tray/core/notification_policy.py` (dopisz `RenderedNotification`, `render`, `entry_id_from`)
- Create: `src/kimai_tray/desktop/notifications.py`
- Test: `tests/core/test_notification_render.py`, `tests/desktop/test_notifications.py`

## Kryteria akceptacji

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] Wynik planu: 8 PASS.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Napisz testy (padające)
- [x] Step 2: Uruchom — mają paść
- [x] Step 3: Dopisz do `src/kimai_tray/core/notification_policy.py`
- [x] Step 4: Utwórz `src/kimai_tray/desktop/notifications.py`
- [x] Step 5: Uruchom — mają przejść
- [x] Step 6: Commit

## Materiały

- [testy/pytest-2026-09-25.txt](testy/pytest-2026-09-25.txt) — końcowy przebieg: `200 passed, 9 deselected in 0.14s`

## Dziennik

### 2026-09-25
- **20:59** Utworzono zadanie z Planu 2.
- **21:01** Start wykonania.
- **21:01** Zamknięte: testy zielone (200 passed, 9 deselected in 0.14s), commity na main.

## Wynik

Rdzeń: [notification_policy.py](../../../src/kimai_tray/core/notification_policy.py) — `RenderedNotification`, `render()`, `entry_id_from()`, `ACTION_LABELS`. Pulpit: [notifications.py](../../../src/kimai_tray/desktop/notifications.py) — `PortalNotifier` (show/withdraw/listen/parse), `NotificationAction`. Testy: [test_notification_render.py](../../../tests/core/test_notification_render.py), [test_notifications.py](../../../tests/desktop/test_notifications.py) — 8 zielonych. Bez odchyleń od planu.
