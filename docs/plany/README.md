---
noteId: "e06027921ce84d1abaad7deec408b097"
tytul: Plany implementacji — indeks
tags: [plan, indeks]
utworzono: 2026-09-25 18:49
zaktualizowano: 2026-09-27 13:15
---

# Plany implementacji

Specyfikacja: [DK Tracker 1.0](../specyfikacja/2026-09-25-kimai-tray-1.0.md). Każdy plan daje
działające, przetestowane oprogramowanie i jest wykonywany zadanie po zadaniu (TDD).

| Plan | Zakres | Stan |
| --- | --- | --- |
| [Plan 1: Rdzeń](2026-09-25-plan-1-rdzen.md) | `core/`: klient API, walidacja, billable, czas i strefy, tracker, polityka powiadomień, PL/EN, testy kontraktowe | **wykonany** (zadania 0005–0018, poprawki 0019) ([raport](../../TODO/ZROBIONE/0002-specyfikacja-projektu/testy/weryfikacja-planu-1-2026-09-25.md)) |
| [Plan 2: Integracje desktopowe](2026-09-25-plan-2-desktop.md) | `desktop/`: sekrety (jeepney), portal Notification, portal Background | **wykonany** (zadania [0022](../../TODO/ZROBIONE/0022-plan2-szyna-dbus/todo.md)–[0026](../../TODO/ZROBIONE/0026-plan2-testy-na-zywo-i-komendy/todo.md), uwagi z recenzji rozstrzygnięte: [0027](../../TODO/ZROBIONE/0027-drobne-uwagi-z-recenzji-planu-2/todo.md)) |
| [Plan 3: Interfejs Qt](2026-09-25-plan-3-ui.md) | `ui/`: tacka (wariant C), okno przy tacce, ustawienia, kontroler, start | **wykonany** (zadania [0029](../../TODO/ZROBIONE/0029-plan3-zaleznosci-i-teksty-ui/todo.md)–[0041](../../TODO/ZROBIONE/0041-plan3-test-na-zywo/todo.md), poprawki z testu na żywo [0042](../../TODO/ZROBIONE/0042-poprawki-po-tescie-na-zywo/todo.md), uwagi z recenzji: [0044](../../TODO/ZROBIONE/0044-drobne-uwagi-z-recenzji-planu-3/todo.md)) |
| [Plan 4: Flatpak i wydanie](2026-09-26-plan-4-flatpak.md) | manifest, MetaInfo, budowa w kontenerze, repozytorium Flatpak na GitHub Pages, GitHub Actions, wydanie 0.9.0 | **wykonany** (zadania [0046](../../TODO/ZROBIONE/0046-plan4-wersja-licencja/todo.md)–[0053](../../TODO/ZROBIONE/0053-plan4-pierwsze-wydanie/todo.md), uwagi z recenzji [0057](../../TODO/ZROBIONE/0057-drobne-uwagi-z-recenzji-planu-4/todo.md); wydania 0.9.0 i 0.9.1) |
| [Plan 5: Okno główne (0.10.0)](2026-09-26-plan-5-okno-glowne.md) | `core/`: wpisy okresu, ręczny wpis, edycja, usuwanie, lista tygodni; `ui/main_window/`: okno główne w QML; start, tacka, zamykanie; testy kontraktowe; wydanie 0.10.0 | **wykonany** (zadanie [0069](../../TODO/ZROBIONE/0069-plan5-okno-glowne/todo.md), poprawki z testów na żywo; wydanie 0.10.0) |
| [Plan 6: Podsumowania (0.10.3)](2026-09-27-plan-6-podsumowania.md) | `core/summary.py`: okresy, średnie, norma, podział; widok „Podsumowania” w QML z wykresami; norma w ustawieniach; test kontraktowy sum; wydanie 0.10.3 | **wykonany** (zadanie [0070](../../TODO/ZROBIONE/0070-plan6-podsumowania/todo.md)) |
| [Plan 7: Kalendarz (0.10.5)](2026-09-27-plan-7-kalendarz.md) | `core/calendar.py`: dni, bloki, przyciąganie; `Tracker.reschedule`; widok „Kalendarz” w QML z przeciąganiem i dymkiem; wydanie 0.10.5 | **w trakcie** (zadanie [0073](../../TODO/W-TRAKCIE/0073-plan7-kalendarz/todo.md)) |

Kolejność: Plan 1 i prototyp 0004 mogą iść równolegle → Plan 2 → Plan 3 → Plan 4 → Plan 5 → Plan 6 → Plan 7
([specyfikacja 0.10](../specyfikacja/2026-09-26-okno-glowne-0.10.md)).
