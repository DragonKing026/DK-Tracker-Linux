---
name: frontmatter
description: Use when creating any new .md file in this repo, before committing docs/ or TODO/ changes, or when a Markdown file shows up modified with an added noteId — ensures every document has YAML front matter with a unique noteId and tags so the VS Code notebook extension does not rewrite files.
---

# frontmatter — noteId i tags w każdym dokumencie

Rozszerzenie VS Code **notebook** (eighthundreds) po otwarciu pliku `.md` bez `noteId`
dopisuje `noteId` i `tags: []`. Plik staje się wtedy „zmieniony” w gicie. Dlatego każdy
dokument ma je od początku.

Wymagane minimum we frontmatterze:

```yaml
---
noteId: "32 znaki hex, unikalne"   # python3 .claude/skills/frontmatter/frontmatter.py noteid
tags: [obszar, temat]              # nie „tagi”
---
```

## Komendy

```bash
python3 .claude/skills/frontmatter/frontmatter.py sprawdz   # raport, kod wyjścia 1 = problemy
python3 .claude/skills/frontmatter/frontmatter.py napraw    # dopisz brakujące noteId/tags, tagi → tags
python3 .claude/skills/frontmatter/frontmatter.py noteid    # nowy noteId do nowego pliku
```

## Kiedy

- **Nowy plik `.md`** → od razu z `noteId` (komenda `noteid`) i `tags`.
- **Przed commitem** zmian w `docs/`, `TODO/` lub plików `.md` w katalogu głównym → `sprawdz`.
- `git status` pokazuje zmieniony `.md` z dopisanym `noteId` → `napraw` (albo zostaw
  dopisany `noteId`) i **zacommituj**. Nie zostawiaj takiej zmiany niezacommitowanej.

## Szablony

[TODO/_szablon/todo.md](../../../TODO/_szablon/todo.md) ma `noteId: "{{NOTEID}}"`.
Skill `nowe-zadanie` zamienia go na świeży identyfikator. Kopie nigdy nie mogą
dzielić jednego `noteId`.

Pliki w `.claude/` (skille) są pomijane — ich frontmatter czyta Claude Code.
