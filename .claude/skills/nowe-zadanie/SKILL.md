---
name: nowe-zadanie
description: Use before starting any new piece of work in this repo, or when the user asks to add/plan a task — creates a numbered task folder in TODO/DO-ZROBIENIA/ from the template and registers it on the TODO/README.md board.
---

# nowe-zadanie — nowe zadanie w `TODO/DO-ZROBIENIA/`

Proces: [docs/procesy/zadania.md](../../../docs/procesy/zadania.md). Szablon: [TODO/_szablon/todo.md](../../../TODO/_szablon/todo.md).

## Kroki

1. **Numer** — następny wolny, licząc zadania we wszystkich folderach statusów:
   ```bash
   ls TODO/DO-ZROBIENIA TODO/W-TRAKCIE TODO/ZROBIONE | grep -E '^[0-9]{4}-' | sort | tail -1
   ```
   Nowy numer = ostatni + 1, dopełniony zerami do 4 cyfr. Numerów nie używamy ponownie.
2. **Slug** — krótki, małe litery, myślniki, bez polskich znaków (`klient-api-kimai`).
3. **Utwórz folder i plik**:
   ```bash
   mkdir -p "TODO/DO-ZROBIENIA/NNNN-slug"
   cp TODO/_szablon/todo.md "TODO/DO-ZROBIENIA/NNNN-slug/todo.md"
   ```
4. **Wypełnij** wszystkie `{{...}}`: `{{NOTEID}}` (świeży: `python3 .claude/skills/frontmatter/frontmatter.py noteid`), `{{NNNN}}`, `{{TYTUL}}`, `{{DATA}}` (dzisiejsza ISO),
   `{{STATUS}}`, `{{PRIORYTET}}`. Uzupełnij pola frontmattera `status`, `priorytet`,
   `tags`, `zalezy_od` (lista nazw folderów, np. `["0003-wybor-stosu"]`).
5. **Treść** — rzetelnie: Cel, Kontekst (z linkami markdown do docs/integracji/ADR/zadań — każde odwołanie jest linkiem),
   sprawdzalne Kryteria akceptacji, Kroki. Jeśli pomaga — diagram `mermaid`.
   **Wszystkie materiały zadania** w jego folderze, w podfolderach według rodzaju
   (tworzonych, gdy jest co położyć): `zrzuty/`, `diagramy/`, `testy/`, `prototyp/`,
   `notatki/`, `dane/`. Każdy materiał podlinkuj/osadź w sekcji „Materiały” todo.md,
   np. `![opis](zrzuty/plik.png)`, `[raport](testy/raport.md)`. Zasady: [docs/procesy/zadania.md](../../../docs/procesy/zadania.md).
6. **Tablica** — dodaj wiersz z **linkiem** w sekcji „Do zrobienia” w `TODO/README.md`
   (zależności też jako linki):
   ```markdown
   | 0005 | [Klient API Kimai](DO-ZROBIENIA/0005-klient-api-kimai/todo.md) | 📋 do-zrobienia | p1 | [0003](ZROBIONE/0003-wybor-stosu/todo.md) |
   ```
   Link markdown ze ścieżką względną (działa w Obsidianie i na GitHubie).
   Wiersze sortuj po numerze.
7. **Kontrola**: `python3 .claude/skills/sprawdz-linki/linki.py sprawdz` → „Wszystkie linki OK.”
   i `python3 .claude/skills/frontmatter/frontmatter.py sprawdz` → „Frontmatter OK.”
8. **Commit** (skill `commit`): `todo: dodaj zadanie NNNN-slug`.
9. Jeśli od razu zaczynasz pracę — skill `zmien-status-zadania` (przeniesie do `W-TRAKCIE/`).

## Sprawdź przed commitem

- [ ] brak pozostałych `{{` w pliku (`grep -n '{{' TODO/DO-ZROBIENIA/NNNN-slug/todo.md`)
- [ ] wiersz na tablicy, link działa
