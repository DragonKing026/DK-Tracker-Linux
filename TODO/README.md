---
noteId: "cac7a114c5cb4e29b37b72cfb350f540"
tytul: Tablica zadań
tags: [todo, tablica]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
---

# Tablica zadań

Zasady: [Zadania w folderze TODO](../docs/procesy/zadania.md) · Szablon: [_szablon](_szablon/todo.md)

Aktywne zadania leżą bezpośrednio w `TODO/`, zakończone (`zrobione` / `porzucone`)
są przenoszone do [`TODO/DONE/`](ZROBIONE).

Legenda statusów: 💡 `pomysl` · 📋 `do-zrobienia` · 🔨 `w-toku` · ⛔ `zablokowane` ·
✅ `zrobione` · 🗑️ `porzucone`

## Aktywne

| Nr | Zadanie | Status | Priorytet | Zależy od |
|---|---|---|---|---|
| 0002 | [Specyfikacja projektu i plan](W-TRAKCIE/0002-specyfikacja-projektu/todo.md) | 🔨 w-toku | p0 | — |
| 0004 | [Prototyp tacki i okna (spike)](DO-ZROBIENIA/0004-prototyp-tacki-i-okna/todo.md) | 📋 do-zrobienia | p1 | [0003](ZROBIONE/0003-wybor-stosu/todo.md) ✅ |

## Zakończone (`TODO/DONE/`)

| Nr | Zadanie | Status | Zamknięto |
|---|---|---|---|
| 0001 | [Struktura agenta i dokumentacji](ZROBIONE/0001-struktura-agenta-i-dokumentacja/todo.md) | ✅ zrobione | 2026-09-25 |
| 0003 | [Wybór stosu technologicznego](ZROBIONE/0003-wybor-stosu/todo.md) | ✅ zrobione | 2026-09-25 |

## Widok dynamiczny (Obsidian + Dataview)

Jeśli masz wtyczkę [Dataview](https://blacksmithgu.github.io/obsidian-dataview/), poniższy
blok pokaże tabelę na żywo z frontmatterów zadań:

```dataview
TABLE status, priorytet, zalezy_od AS "zależy od", zaktualizowano
FROM "TODO" AND -"TODO/DONE"
WHERE file.name = "todo" AND numer
SORT numer ASC
```

Zakończone zadania (Dataview):

```dataview
TABLE status, zamknieto
FROM "TODO/DONE"
WHERE file.name = "todo"
SORT numer ASC
```
