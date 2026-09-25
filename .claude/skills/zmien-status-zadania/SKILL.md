---
name: zmien-status-zadania
description: Use whenever a TODO task changes status — starting work, blocking, unblocking, finishing or abandoning — updates the task's front matter, log and result, moves its folder between TODO/DO-ZROBIENIA, TODO/W-TRAKCIE and TODO/ZROBIONE with automatic link fixing, updates the TODO/README.md board and commits.
---

# zmien-status-zadania — zmiana statusu, przeniesienie, zamknięcie

Proces: [docs/procesy/zadania.md](../../../docs/procesy/zadania.md).

## Status → folder

| Status | Folder |
|---|---|
| `pomysl`, `do-zrobienia` | `TODO/DO-ZROBIENIA/` |
| `w-trakcie`, `zablokowane` | `TODO/W-TRAKCIE/` |
| `zrobione`, `porzucone` | `TODO/ZROBIONE/` |

## Kroki

1. **Przy zamknięciu (`zrobione`) zweryfikuj** kryteria akceptacji w `todo.md`. Każde
   odhaczone `- [x]` musi być faktycznie spełnione (uruchom testy lub komendy, jeśli
   dotyczy). Niespełnione kryterium oznacza, że zadanie nie jest `zrobione`.
2. **Frontmatter**: `status`, `zaktualizowano`; przy zamknięciu `zamknieto: <data ISO>`.
   Zaktualizuj callout „Status” na górze pliku.
3. **Dziennik**: wpis z datą — co się zmieniło i dlaczego, kluczowe commity
   (`git log --oneline`).
4. **Materiały** (przy zamknięciu): wszystko, co powstało w zadaniu, leży w podfolderach
   jego folderu (`zrzuty/`, `testy/`, `prototyp/`…) i jest podlinkowane w sekcji
   „Materiały”. Sprawdź: `git status` i `find <folder zadania> -type f`.
5. **Wynik** (przy zamknięciu): co powstało (linki), co świadomie zostało na później.
   Jeśli coś zostało na później, utwórz nowe zadanie skillem `nowe-zadanie`.
6. **Przeniesienie**, gdy nowy status należy do innego folderu. Tylko skryptem, który
   robi `git mv` i poprawia wszystkie linki:
   ```bash
   python3 .claude/skills/sprawdz-linki/linki.py przenies \
     TODO/DO-ZROBIENIA/NNNN-slug TODO/W-TRAKCIE/NNNN-slug
   ```
   Wynik musi kończyć się „Wszystkie linki OK.”. Nie używaj samego `git mv`.
7. **Tablica** [TODO/README.md](../../../TODO/README.md): przenieś wiersz do sekcji
   odpowiadającej folderowi („Do zrobienia” / „W trakcie” / „Zrobione”) i zaktualizuj
   kolumnę Status. Linki w wierszach poprawia skrypt z kroku 6. Wiersze sortuj po numerze.
8. **Kontrola**: `linki.py sprawdz` i `frontmatter.py sprawdz`.
9. **Commit**: `todo: rozpocznij NNNN-slug` / `todo: zablokuj NNNN-slug` /
   `todo: zamknij NNNN-slug` / `todo: porzuć NNNN-slug`.
