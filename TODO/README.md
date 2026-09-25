---
noteId: "cac7a114c5cb4e29b37b72cfb350f540"
tytul: Tablica zadań
tags: [todo, tablica]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
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
| 0002 | [Specyfikacja projektu (design) i plan implementacji](W-TRAKCIE/0002-specyfikacja-projektu/todo.md) | 🔨 w-trakcie | p0 | — |
| 0005 | [Plan 1 · Zadanie 1: Szkielet projektu Python i test architektury](W-TRAKCIE/0005-plan1-szkielet-projektu-python-i-test/todo.md) | 🔨 w-trakcie | p1 | [0002](W-TRAKCIE/0002-specyfikacja-projektu/todo.md) |

## Do zrobienia

| Nr | Zadanie | Status | Priorytet | Zależy od |
|---|---|---|---|---|
| 0004 | [Prototyp: ikona w tacce i okno na KDE i GNOME we Flatpaku](DO-ZROBIENIA/0004-prototyp-tacki-i-okna/todo.md) | 📋 do-zrobienia | p1 | [0003](ZROBIONE/0003-wybor-stosu/todo.md) ✅ |
| 0006 | [Plan 1 · Zadanie 2: Błędy (`errors.py`)](DO-ZROBIENIA/0006-plan1-bledy/todo.md) | 📋 do-zrobienia | p1 | [0005](W-TRAKCIE/0005-plan1-szkielet-projektu-python-i-test/todo.md) |
| 0007 | [Plan 1 · Zadanie 3: Modele danych (`models.py`)](DO-ZROBIENIA/0007-plan1-modele-danych/todo.md) | 📋 do-zrobienia | p1 | [0006](DO-ZROBIENIA/0006-plan1-bledy/todo.md) |
| 0008 | [Plan 1 · Zadanie 4: Czas i strefy (`timefmt.py`)](DO-ZROBIENIA/0008-plan1-czas-i-strefy/todo.md) | 📋 do-zrobienia | p1 | [0007](DO-ZROBIENIA/0007-plan1-modele-danych/todo.md) |
| 0009 | [Plan 1 · Zadanie 5: Walidacja opisu (`validation.py`, F-11)](DO-ZROBIENIA/0009-plan1-walidacja-opisu/todo.md) | 📋 do-zrobienia | p1 | [0008](DO-ZROBIENIA/0008-plan1-czas-i-strefy/todo.md) |
| 0010 | [Plan 1 · Zadanie 6: Grupowanie list i reguły billable (`grouping.py`, `billable.py`, F-06/F-08/F-09)](DO-ZROBIENIA/0010-plan1-grupowanie-list-i-reguly-billable/todo.md) | 📋 do-zrobienia | p1 | [0009](DO-ZROBIENIA/0009-plan1-walidacja-opisu/todo.md) |
| 0011 | [Plan 1 · Zadanie 7: Klient Kimai API (`kimai_client.py`)](DO-ZROBIENIA/0011-plan1-klient-kimai-api/todo.md) | 📋 do-zrobienia | p1 | [0010](DO-ZROBIENIA/0010-plan1-grupowanie-list-i-reguly-billable/todo.md) |
| 0012 | [Plan 1 · Zadanie 8: Ustawienia i pamięć aplikacji (`settings.py`)](DO-ZROBIENIA/0012-plan1-ustawienia-i-pamiec-aplikacji/todo.md) | 📋 do-zrobienia | p1 | [0011](DO-ZROBIENIA/0011-plan1-klient-kimai-api/todo.md) |
| 0013 | [Plan 1 · Zadanie 9: Tłumaczenia PL/EN (`i18n.py`, `locales/`, F-13)](DO-ZROBIENIA/0013-plan1-tlumaczenia-pl-en/todo.md) | 📋 do-zrobienia | p1 | [0012](DO-ZROBIENIA/0012-plan1-ustawienia-i-pamiec-aplikacji/todo.md) |
| 0014 | [Plan 1 · Zadanie 10: Tracker — stan i odświeżanie (`tracker.py` część 1)](DO-ZROBIENIA/0014-plan1-tracker-stan-i-odswiezanie/todo.md) | 📋 do-zrobienia | p1 | [0013](DO-ZROBIENIA/0013-plan1-tlumaczenia-pl-en/todo.md) |
| 0015 | [Plan 1 · Zadanie 11: Tracker — akcje (`tracker.py` część 2, F-04…F-10)](DO-ZROBIENIA/0015-plan1-tracker-akcje/todo.md) | 📋 do-zrobienia | p1 | [0014](DO-ZROBIENIA/0014-plan1-tracker-stan-i-odswiezanie/todo.md) |
| 0016 | [Plan 1 · Zadanie 12: Polityka powiadomień (`notification_policy.py`, F-21)](DO-ZROBIENIA/0016-plan1-polityka-powiadomien/todo.md) | 📋 do-zrobienia | p1 | [0015](DO-ZROBIENIA/0015-plan1-tracker-akcje/todo.md) |
| 0017 | [Plan 1 · Zadanie 13: Testy kontraktowe na Kimai w Dockerze](DO-ZROBIENIA/0017-plan1-testy-kontraktowe-na-kimai-w/todo.md) | 📋 do-zrobienia | p1 | [0016](DO-ZROBIENIA/0016-plan1-polityka-powiadomien/todo.md) |
| 0018 | [Plan 1 · Zadanie 14: Komendy, pokrycie i dokumentacja rdzenia](DO-ZROBIENIA/0018-plan1-komendy-pokrycie-i-dokumentacja-rdzenia/todo.md) | 📋 do-zrobienia | p1 | [0017](DO-ZROBIENIA/0017-plan1-testy-kontraktowe-na-kimai-w/todo.md) |

## Zrobione

| Nr | Zadanie | Status | Zamknięto |
|---|---|---|---|
| 0001 | [Struktura agenta i dokumentacji](ZROBIONE/0001-struktura-agenta-i-dokumentacja/todo.md) | ✅ zrobione | 2026-09-25 |
| 0003 | [Wybór stosu technologicznego](ZROBIONE/0003-wybor-stosu/todo.md) | ✅ zrobione | 2026-09-25 |

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
