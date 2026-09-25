---
name: zamknij-zadanie
description: Use when a task in TODO/ is finished, abandoned or its status changes — updates the task's frontmatter, log and result section, moves it on the TODO/README.md board and commits.
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
5. **Tablica** `TODO/README.md`: przy zamknięciu przenieś wiersz z „Aktywne” do
   „Zakończone” (`| Nr | Zadanie | Status | Zamknięto |`); przy innej zmianie statusu —
   zaktualizuj kolumnę Status.
6. **Commit**: `todo: zamknij zadanie NNNN-slug` / `todo: zmień status NNNN-slug na w-toku`.
