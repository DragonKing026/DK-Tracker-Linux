---
noteId: "e06027921ce84d1abaad7deec408b097"
tytul: Plany implementacji — indeks
tags: [plan, indeks]
utworzono: 2026-09-25 18:49
zaktualizowano: 2026-09-25 21:00
---

# Plany implementacji

Specyfikacja: [Kimai Tray 1.0](../specyfikacja/2026-09-25-kimai-tray-1.0.md). Każdy plan daje
działające, przetestowane oprogramowanie i jest wykonywany zadanie po zadaniu (TDD).

| Plan | Zakres | Stan |
|---|---|---|
| [Plan 1: Rdzeń](2026-09-25-plan-1-rdzen.md) | `core/`: klient API, walidacja, billable, czas i strefy, tracker, polityka powiadomień, PL/EN, testy kontraktowe | **wykonany** (zadania 0005–0018, poprawki 0019) ([raport](../../TODO/ZROBIONE/0002-specyfikacja-projektu/testy/weryfikacja-planu-1-2026-09-25.md)) |
| [Plan 2: Integracje desktopowe](2026-09-25-plan-2-desktop.md) | `desktop/`: sekrety (jeepney), portal Notification, portal Background | zaakceptowany, w realizacji (zadania [0022](../../TODO/ZROBIONE/0022-plan2-szyna-dbus/todo.md)–[0026](../../TODO/ZROBIONE/0026-plan2-testy-na-zywo-i-komendy/todo.md)) — kod zweryfikowany ([raport](../../TODO/W-TRAKCIE/0021-plan2-rozpoznanie-api-desktop/testy/weryfikacja-planu-2.md)) |
| Plan 3: Interfejs Qt | `ui/`: tacka, okno, ustawienia, worker; po [prototypie 0004](../../TODO/ZROBIONE/0004-prototyp-tacki-i-okna/todo.md) | do napisania |
| Plan 4: Flatpak i wydanie | manifest, zależności pip, .desktop, MetaInfo, testy ręczne | do napisania |

Kolejność: Plan 1 i prototyp 0004 mogą iść równolegle → Plan 2 → Plan 3 → Plan 4.
