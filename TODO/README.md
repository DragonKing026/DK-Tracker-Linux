---
noteId: "cac7a114c5cb4e29b37b72cfb350f540"
tytul: Tablica zadań
tags: [todo, tablica]
utworzono: 2026-09-25 17:14
zaktualizowano: 2026-09-25 21:00
---

# Tablica zadań

Zasady: [Zadania w folderze TODO](../docs/procesy/zadania.md) · Szablon: [_szablon](_szablon/todo.md)

Zadania leżą w podfolderach według statusu. Przy zmianie statusu folder zadania jest
przenoszony (skill [zmien-status-zadania](../.claude/skills/zmien-status-zadania/SKILL.md)).

| Folder | Statusy |
|---|---|
| [DO-ZROBIENIA/](DO-ZROBIENIA) | 💡 `pomysl` · 📋 `do-zrobienia` |
| [W-TRAKCIE/](W-TRAKCIE) | 🔨 `w-trakcie` · ⛔ `zablokowane` |
| [ZROBIONE/](ZROBIONE) | ✅ `zrobione` · 🗑️ `porzucone` |

<!-- tablica:start -->

## W trakcie

| Nr | Zadanie | Status | Priorytet | Zależy od |
|---|---|---|---|---|
| 0021 | [Plan 2 — rozpoznanie API integracji desktopowych](W-TRAKCIE/0021-plan2-rozpoznanie-api-desktop/todo.md) | 🔨 w-trakcie | p1 | [0004](ZROBIONE/0004-prototyp-tacki-i-okna/todo.md) ✅ |
| 0023 | [Plan 2 · Zadanie 2: Token w magazynie sekretów (`desktop/secrets.py`)](W-TRAKCIE/0023-plan2-token-w-magazynie-sekretow/todo.md) | 🔨 w-trakcie | p1 | [0022](ZROBIONE/0022-plan2-szyna-dbus/todo.md) ✅ |

## Do zrobienia

| Nr | Zadanie | Status | Priorytet | Zależy od |
|---|---|---|---|---|
| 0020 | [Testy ręczne na GNOME (tacka, okno, Flatpak)](DO-ZROBIENIA/0020-testy-gnome/todo.md) | 📋 do-zrobienia | p2 | [0004](ZROBIONE/0004-prototyp-tacki-i-okna/todo.md) ✅ |
| 0024 | [Plan 2 · Zadanie 3: Powiadomienia — tekst w rdzeniu, wysyłka przez portal](DO-ZROBIENIA/0024-plan2-powiadomienia-przez-portal/todo.md) | 📋 do-zrobienia | p1 | [0022](ZROBIONE/0022-plan2-szyna-dbus/todo.md) ✅ |
| 0025 | [Plan 2 · Zadanie 4: Autostart i status w tle (`desktop/autostart.py`)](DO-ZROBIENIA/0025-plan2-autostart-i-status-w-tle/todo.md) | 📋 do-zrobienia | p1 | [0022](ZROBIONE/0022-plan2-szyna-dbus/todo.md) ✅ |
| 0026 | [Plan 2 · Zadanie 5: Testy na prawdziwej sesji i komendy](DO-ZROBIENIA/0026-plan2-testy-na-zywo-i-komendy/todo.md) | 📋 do-zrobienia | p1 | [0023](W-TRAKCIE/0023-plan2-token-w-magazynie-sekretow/todo.md), [0024](DO-ZROBIENIA/0024-plan2-powiadomienia-przez-portal/todo.md), [0025](DO-ZROBIENIA/0025-plan2-autostart-i-status-w-tle/todo.md) |

## Zrobione

| Nr | Zadanie | Status | Zamknięto |
|---|---|---|---|
| 0001 | [Struktura agenta i dokumentacji](ZROBIONE/0001-struktura-agenta-i-dokumentacja/todo.md) | ✅ zrobione | 2026-09-25 17:23 |
| 0002 | [Specyfikacja projektu (design) i plan implementacji](ZROBIONE/0002-specyfikacja-projektu/todo.md) | ✅ zrobione | 2026-09-25 19:15 |
| 0003 | [Wybór stosu technologicznego](ZROBIONE/0003-wybor-stosu/todo.md) | ✅ zrobione | 2026-09-25 17:29 |
| 0004 | [Prototyp: ikona w tacce i okno na KDE i GNOME we Flatpaku](ZROBIONE/0004-prototyp-tacki-i-okna/todo.md) | ✅ zrobione | 2026-09-25 20:39 |
| 0005 | [Plan 1 · Zadanie 1: Szkielet projektu Python i test architektury](ZROBIONE/0005-plan1-szkielet-projektu-python-i-test/todo.md) | ✅ zrobione | 2026-09-25 19:01 |
| 0006 | [Plan 1 · Zadanie 2: Błędy (`errors.py`)](ZROBIONE/0006-plan1-bledy/todo.md) | ✅ zrobione | 2026-09-25 19:01 |
| 0007 | [Plan 1 · Zadanie 3: Modele danych (`models.py`)](ZROBIONE/0007-plan1-modele-danych/todo.md) | ✅ zrobione | 2026-09-25 19:01 |
| 0008 | [Plan 1 · Zadanie 4: Czas i strefy (`timefmt.py`)](ZROBIONE/0008-plan1-czas-i-strefy/todo.md) | ✅ zrobione | 2026-09-25 19:02 |
| 0009 | [Plan 1 · Zadanie 5: Walidacja opisu (`validation.py`, F-11)](ZROBIONE/0009-plan1-walidacja-opisu/todo.md) | ✅ zrobione | 2026-09-25 19:02 |
| 0010 | [Plan 1 · Zadanie 6: Grupowanie list i reguły billable (`grouping.py`, `billable.py`, F-06/F-08/F-09)](ZROBIONE/0010-plan1-grupowanie-list-i-reguly-billable/todo.md) | ✅ zrobione | 2026-09-25 19:02 |
| 0011 | [Plan 1 · Zadanie 7: Klient Kimai API (`kimai_client.py`)](ZROBIONE/0011-plan1-klient-kimai-api/todo.md) | ✅ zrobione | 2026-09-25 19:02 |
| 0012 | [Plan 1 · Zadanie 8: Ustawienia i pamięć aplikacji (`settings.py`)](ZROBIONE/0012-plan1-ustawienia-i-pamiec-aplikacji/todo.md) | ✅ zrobione | 2026-09-25 19:02 |
| 0013 | [Plan 1 · Zadanie 9: Tłumaczenia PL/EN (`i18n.py`, `locales/`, F-13)](ZROBIONE/0013-plan1-tlumaczenia-pl-en/todo.md) | ✅ zrobione | 2026-09-25 19:03 |
| 0014 | [Plan 1 · Zadanie 10: Tracker — stan i odświeżanie (`tracker.py` część 1)](ZROBIONE/0014-plan1-tracker-stan-i-odswiezanie/todo.md) | ✅ zrobione | 2026-09-25 19:03 |
| 0015 | [Plan 1 · Zadanie 11: Tracker — akcje (`tracker.py` część 2, F-04…F-10)](ZROBIONE/0015-plan1-tracker-akcje/todo.md) | ✅ zrobione | 2026-09-25 19:03 |
| 0016 | [Plan 1 · Zadanie 12: Polityka powiadomień (`notification_policy.py`, F-21)](ZROBIONE/0016-plan1-polityka-powiadomien/todo.md) | ✅ zrobione | 2026-09-25 19:03 |
| 0017 | [Plan 1 · Zadanie 13: Testy kontraktowe na Kimai w Dockerze](ZROBIONE/0017-plan1-testy-kontraktowe-na-kimai-w/todo.md) | ✅ zrobione | 2026-09-25 19:04 |
| 0018 | [Plan 1 · Zadanie 14: Komendy, pokrycie i dokumentacja rdzenia](ZROBIONE/0018-plan1-komendy-pokrycie-i-dokumentacja-rdzenia/todo.md) | ✅ zrobione | 2026-09-25 19:05 |
| 0019 | [Drobne uwagi z recenzji Planu 1 (rdzeń)](ZROBIONE/0019-drobne-uwagi-z-recenzji-planu-1/todo.md) | ✅ zrobione | 2026-09-25 19:55 |
| 0022 | [Plan 2 · Zadanie 1: Szyna D-Bus (`desktop/bus.py`)](ZROBIONE/0022-plan2-szyna-dbus/todo.md) | ✅ zrobione | 2026-09-25 21:00 |

<!-- tablica:end -->

## Widok dynamiczny (Obsidian + Dataview)

Jeśli masz wtyczkę [Dataview](https://blacksmithgu.github.io/obsidian-dataview/), te
bloki pokażą tabele na żywo z frontmatterów zadań:

```dataview
TABLE status, priorytet, zalezy_od AS "zależy od", zaktualizowano
FROM "TODO/W-TRAKCIE" OR "TODO/DO-ZROBIENIA"
WHERE file.name = "todo"
SORT numer ASC
```

```dataview
TABLE status, zamknieto
FROM "TODO/ZROBIONE"
WHERE file.name = "todo"
SORT numer ASC
```
