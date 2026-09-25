---
noteId: "e06027921ce84d1abaad7deec408b097"
tytul: Plany implementacji — indeks
tags: [plan, indeks]
utworzono: 2026-09-25 18:49
zaktualizowano: 2026-09-25 22:58
---

# Plany implementacji

Specyfikacja: [Kimai Tray 1.0](../specyfikacja/2026-09-25-kimai-tray-1.0.md). Każdy plan daje
działające, przetestowane oprogramowanie i jest wykonywany zadanie po zadaniu (TDD).

| Plan | Zakres | Stan |
|---|---|---|
| [Plan 1: Rdzeń](2026-09-25-plan-1-rdzen.md) | `core/`: klient API, walidacja, billable, czas i strefy, tracker, polityka powiadomień, PL/EN, testy kontraktowe | **wykonany** (zadania 0005–0018, poprawki 0019) ([raport](../../TODO/ZROBIONE/0002-specyfikacja-projektu/testy/weryfikacja-planu-1-2026-09-25.md)) |
| [Plan 2: Integracje desktopowe](2026-09-25-plan-2-desktop.md) | `desktop/`: sekrety (jeepney), portal Notification, portal Background | **wykonany** (zadania [0022](../../TODO/ZROBIONE/0022-plan2-szyna-dbus/todo.md)–[0026](../../TODO/ZROBIONE/0026-plan2-testy-na-zywo-i-komendy/todo.md), uwagi z recenzji rozstrzygnięte: [0027](../../TODO/ZROBIONE/0027-drobne-uwagi-z-recenzji-planu-2/todo.md)) |
| [Plan 3: Interfejs Qt](2026-09-25-plan-3-ui.md) | `ui/`: tacka (wariant C), okno przy tacce, ustawienia, kontroler, start | do akceptacji — kod zweryfikowany ([raport](../../TODO/ZROBIONE/0028-plan3-projekt-ui/testy/weryfikacja-planu-3.md)) |
| Plan 4: Flatpak i wydanie | manifest, zależności pip, .desktop, MetaInfo, testy ręczne | do napisania |

Kolejność: Plan 1 i prototyp 0004 mogą iść równolegle → Plan 2 → Plan 3 → Plan 4.
