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
| [DO-ZROBIENIA/](DO-ZROBIENIA/) | 💡 `pomysl` · 📋 `do-zrobienia` |
| [W-TRAKCIE/](W-TRAKCIE/) | 🔨 `w-trakcie` · ⛔ `zablokowane` |
| [ZROBIONE/](ZROBIONE/) | ✅ `zrobione` · 🗑️ `porzucone` |

<!-- tablica:start -->

## W trakcie

| Nr | Zadanie | Status | Priorytet | Zależy od |
|---|---|---|---|---|
| 0002 | [Specyfikacja projektu (design) i plan implementacji](W-TRAKCIE/0002-specyfikacja-projektu/todo.md) | 🔨 w-trakcie | p0 | — |

## Do zrobienia

| Nr | Zadanie | Status | Priorytet | Zależy od |
|---|---|---|---|---|
| 0004 | [Prototyp: ikona w tacce i okno na KDE i GNOME we Flatpaku](DO-ZROBIENIA/0004-prototyp-tacki-i-okna/todo.md) | 📋 do-zrobienia | p1 | [0003](ZROBIONE/0003-wybor-stosu/todo.md) ✅ |

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
