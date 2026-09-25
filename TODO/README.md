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

## Zakończone

| Nr | Zadanie | Status | Zamknięto |
|---|---|---|---|

## Widok dynamiczny (Obsidian + Dataview)

Jeśli masz wtyczkę [Dataview](https://blacksmithgu.github.io/obsidian-dataview/), poniższy
blok pokaże tabelę na żywo z frontmatterów zadań:

```dataview
TABLE status, priorytet, zalezy_od AS "zależy od", zaktualizowano
FROM "TODO"
WHERE file.name = "todo" AND numer
SORT numer ASC
```
