---
tytul: Tablica zadań
tagi: [todo, tablica]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
---

# Tablica zadań

Zasady: [Zadania w folderze TODO](../docs/procesy/zadania.md) · Szablon: [_szablon](_szablon/todo.md)

Aktywne zadania leżą bezpośrednio w `TODO/`, zakończone (`zrobione` / `porzucone`)
są przenoszone do [`TODO/DONE/`](DONE/).

Legenda statusów: 💡 `pomysl` · 📋 `do-zrobienia` · 🔨 `w-toku` · ⛔ `zablokowane` ·
✅ `zrobione` · 🗑️ `porzucone`

## Aktywne

| Nr | Zadanie | Status | Priorytet | Zależy od |
|---|---|---|---|---|
| 0002 | [Specyfikacja projektu i plan](0002-specyfikacja-projektu/todo.md) | 📋 do-zrobienia | p0 | — |
| 0003 | [Wybór stosu technologicznego](0003-wybor-stosu/todo.md) | 📋 do-zrobienia | p0 | — |
| 0004 | [Prototyp tacki i okna (spike)](0004-prototyp-tacki-i-okna/todo.md) | 💡 pomysl | p1 | 0003 |

## Zakończone (`TODO/DONE/`)

| Nr | Zadanie | Status | Zamknięto |
|---|---|---|---|
| 0001 | [Struktura agenta i dokumentacji](DONE/0001-struktura-agenta-i-dokumentacja/todo.md) | ✅ zrobione | 2026-09-25 |

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
