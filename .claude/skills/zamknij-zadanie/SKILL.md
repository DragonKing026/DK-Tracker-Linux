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
4. **Materiały**: wszystko, co powstało w ramach zadania (zrzuty, raporty testów, logi,
   prototyp, notatki), leży w podfolderach folderu zadania (`zrzuty/`, `testy/`,
   `prototyp/`…) i jest podlinkowane w sekcji „Materiały”. Nic nie leży luzem poza nim.
   Sprawdź: `git status` i `find TODO/NNNN-slug -type f`.
5. **Wynik**: co powstało (ścieżki plików, linki do docs), co świadomie zostało
   na później (i ewentualnie nowe zadania dla tego — skill `nowe-zadanie`).
6. **Przeniesienie do DONE** (tylko `zrobione` / `porzucone`) — skryptem ze skilla
   [sprawdz-linki](../sprawdz-linki/SKILL.md), który przenosi folder przez `git mv`
   i sam poprawia wszystkie linki (do zadania i w jego plikach):
   ```bash
   python3 .claude/skills/sprawdz-linki/linki.py przenies TODO/NNNN-slug TODO/DONE/NNNN-slug
   ```
   Wynik musi kończyć się „Wszystkie linki OK.”. Nie używaj samego `git mv`.
7. **Tablica** [TODO/README.md](../../../TODO/README.md): przy zamknięciu przenieś wiersz z „Aktywne” do
   „Zakończone” z linkiem `[Tytuł](DONE/NNNN-slug/todo.md)`
   (`| Nr | Zadanie | Status | Zamknięto |`); przy innej zmianie statusu —
   zaktualizuj kolumnę Status. W „Aktywne” zostają wyłącznie zadania leżące w `TODO/`.
8. **Commit**: `todo: zamknij zadanie NNNN-slug i przenieś do DONE` / `todo: zmień status NNNN-slug na w-toku`.
