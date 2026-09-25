---
name: zamknij-zadanie
description: Use when a task in TODO/ is finished, abandoned or its status changes — updates the task's frontmatter, log and result section, moves finished/abandoned task folders to TODO/DONE/, updates the TODO/README.md board links and commits.
---

# zamknij-zadanie — zmiana statusu / zamknięcie zadania

## Kroki

1. **Zweryfikuj** kryteria akceptacji w `TODO/NNNN-slug/todo.md` — każde odhaczone
   `- [x]` musi być faktycznie spełnione (uruchom testy/komendy, jeśli dotyczy).
   Niespełnione kryterium = zadanie nie jest `zrobione`.
2. **Frontmatter**: `status` (`zrobione` / `porzucone` / inny), `zaktualizowano`,
   przy zamknięciu `zamknieto: <data ISO>`. Zaktualizuj callout „Status” na górze.
3. **Dziennik**: wpis z datą — co zrobiono, kluczowe commity (`git log --oneline`
   z ostatnich zmian zadania).
4. **Wynik**: co powstało (ścieżki plików, linki do docs), co świadomie zostało
   na później (i ewentualnie nowe zadania dla tego — skill `nowe-zadanie`).
5. **Przeniesienie do DONE** (tylko `zrobione` / `porzucone`):
   ```bash
   git mv "TODO/NNNN-slug" "TODO/DONE/NNNN-slug"
   ```
   Następnie popraw wszystkie odwołania do starej ścieżki:
   ```bash
   grep -rn "TODO/NNNN-slug" --include=*.md . | grep -v '^./.git'
   ```
   (wikilinki `[[TODO/NNNN-slug/...` → `[[TODO/DONE/NNNN-slug/...`).
6. **Tablica** `TODO/README.md`: przy zamknięciu przenieś wiersz z „Aktywne” do
   „Zakończone” z linkiem `[Tytuł](DONE/NNNN-slug/todo.md)`
   (`| Nr | Zadanie | Status | Zamknięto |`); przy innej zmianie statusu —
   zaktualizuj kolumnę Status. W „Aktywne” zostają wyłącznie zadania leżące w `TODO/`.
7. **Commit**: `todo: zamknij zadanie NNNN-slug i przenieś do DONE` / `todo: zmień status NNNN-slug na w-toku`.
