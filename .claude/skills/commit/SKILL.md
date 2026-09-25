---
name: commit
description: Use after every small completed change in this repo (one doc file, one TODO task, one function) to create a single small Conventional Commit in Polish. Use instead of batching changes.
---

# commit — mały commit zgodny z konwencją

Konwencja: [docs/procesy/commity.md](../../../docs/procesy/commity.md).

## Kroki

1. `git status --short` i `git diff` — sprawdź, co faktycznie się zmieniło.
2. Jeśli zmiany dotyczą **kilku niezależnych rzeczy** — rozdziel je na kilka commitów
   (`git add <konkretne pliki>`), nigdy `git add -A` na ślepo.
3. Sprawdź, czy zmiana kodu wymaga aktualizacji `docs/` — jeśli tak, zrób to najpierw
   albo od razu w następnym commicie.
4. Jeśli zmieniłeś plik w `docs/` lub `TODO/` — podbij pole `zaktualizowano:` we frontmatterze.
5. Jeśli zmiana dotyka `docs/`, `TODO/` lub plików `.md` — sprawdź linki:
   `python3 .claude/skills/sprawdz-linki/linki.py sprawdz` (musi być „Wszystkie linki OK.”)
   i frontmatter: `python3 .claude/skills/frontmatter/frontmatter.py sprawdz`,
   potem markdownlint (skill [markdownlint](../markdownlint/SKILL.md)):
   `mdfix.py napraw <zmienione .md>` i `mdfix.py sprawdz` → „markdownlint OK.”
6. Dobierz typ: `feat` `fix` `docs` `todo` `refactor` `test` `build` `ci` `chore`.
7. Commit:

   ```bash
   git commit -m "<typ>(<zakres>): <opis w trybie rozkazującym, małą literą>

   <dlaczego — opcjonalnie>

   Refs: TODO/<NNNN-slug>        # jeśli dotyczy zadania

   Co-Authored-By: <linia z system-reminder środowiska>"
   ```

8. Jeśli commit dotyczy zadania — dopisz w jego `todo.md` w sekcji **Dziennik** skrót
   hasha i opis (`git log -1 --format=%h`), i zacommituj to razem z następną zmianą.

## Nie rób

- `--amend`, `rebase`, `push --force` na `main` — historia ma zostać taka, jak powstała.
- `--no-verify`.
- Push bez prośby użytkownika.
