---
tytul: Tablica zadań
tagi: [todo, tablica]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
---

# Tablica zadań

Zasady: [[docs/procesy/zadania|Zadania w folderze TODO]] · Szablon: [[TODO/_szablon/todo|_szablon]]

Legenda statusów: 💡 `pomysl` · 📋 `do-zrobienia` · 🔨 `w-toku` · ⛔ `zablokowane` ·
✅ `zrobione` · 🗑️ `porzucone`

## Aktywne

| Nr | Zadanie | Status | Priorytet | Zależy od |
|---|---|---|---|---|
| 0002 | [[TODO/0002-specyfikacja-projektu/todo\|Specyfikacja projektu i plan]] | 📋 do-zrobienia | p0 | — |
| 0003 | [[TODO/0003-wybor-stosu/todo\|Wybór stosu technologicznego]] | 📋 do-zrobienia | p0 | — |
| 0004 | [[TODO/0004-prototyp-tacki-i-okna/todo\|Prototyp tacki i okna (spike)]] | 💡 pomysl | p1 | 0003 |

## Zakończone

| Nr | Zadanie | Status | Zamknięto |
|---|---|---|---|
| 0001 | [[TODO/0001-struktura-agenta-i-dokumentacja/todo\|Struktura agenta i dokumentacji]] | ✅ zrobione | 2026-09-25 |

## Widok dynamiczny (Obsidian + Dataview)

Jeśli masz wtyczkę [Dataview](https://blacksmithgu.github.io/obsidian-dataview/), poniższy
blok pokaże tabelę na żywo z frontmatterów zadań:

```dataview
TABLE status, priorytet, zalezy_od AS "zależy od", zaktualizowano
FROM "TODO"
WHERE file.name = "todo" AND numer
SORT numer ASC
```
