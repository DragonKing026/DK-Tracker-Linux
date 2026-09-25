---
name: nowe-zadanie
description: Use before starting any new piece of work in this repo, or when the user asks to add/plan a task — creates a numbered task folder in TODO/ from the template and registers it on the TODO/README.md board.
---

# nowe-zadanie — nowe zadanie w `TODO/`

Proces: `docs/procesy/zadania.md`. Szablon: `TODO/_szablon/todo.md`.

## Kroki

1. **Numer** — następny wolny, licząc też zakończone w `TODO/DONE/`:
   ```bash
   ls TODO TODO/DONE | grep -E '^[0-9]{4}-' | sort | tail -1
   ```
   Nowy numer = ostatni + 1, dopełniony zerami do 4 cyfr. Numerów nie używamy ponownie.
2. **Slug** — krótki, małe litery, myślniki, bez polskich znaków (`klient-api-kimai`).
3. **Utwórz folder i plik**:
   ```bash
   mkdir -p "TODO/NNNN-slug"
   cp TODO/_szablon/todo.md "TODO/NNNN-slug/todo.md"
   ```
4. **Wypełnij** wszystkie `{{...}}`: `{{NNNN}}`, `{{TYTUL}}`, `{{DATA}}` (dzisiejsza ISO),
   `{{STATUS}}`, `{{PRIORYTET}}`. Uzupełnij pola frontmattera `status`, `priorytet`,
   `tagi`, `zalezy_od` (lista nazw folderów, np. `["0003-wybor-stosu"]`).
5. **Treść** — rzetelnie: Cel, Kontekst (z wikilinkami do docs/integracji/ADR),
   sprawdzalne Kryteria akceptacji, Kroki. Jeśli pomaga — diagram `mermaid`.
   Zrzuty i obrazy do `TODO/NNNN-slug/assets/`, osadzone `![[plik.png]]`.
6. **Tablica** — dodaj wiersz z **linkiem** w sekcji „Aktywne” w `TODO/README.md`:
   ```markdown
   | 0005 | [Klient API Kimai](0005-klient-api-kimai/todo.md) | 📋 do-zrobienia | p1 | 0003 |
   ```
   Link markdown ze ścieżką względną (działa w Obsidianie i na GitHubie).
   Wiersze sortuj po numerze.
7. **Commit** (skill `commit`): `todo: dodaj zadanie NNNN-slug`.

## Sprawdź przed commitem

- [ ] brak pozostałych `{{` w pliku (`grep -n '{{' TODO/NNNN-slug/todo.md`)
- [ ] wiersz na tablicy, link działa
