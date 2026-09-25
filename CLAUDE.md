# CLAUDE.md

@AGENTS.md

## Specyfika Claude Code

- Wszystkie reguły projektu są w [AGENTS.md](AGENTS.md) (zaimportowany powyżej). Tu tylko to,
  co dotyczy wyłącznie Claude Code.
- Skille projektu leżą w `.claude/skills/` — używaj ich zamiast robić powtarzalne kroki
  ręcznie (tworzenie zadania, integracji, ADR, commit).
- Dokumentację bibliotek pobieraj przez Context7 MCP (`resolve-library-id` → `query-docs`).
- Pliki tymczasowe (klony repo referencyjnych, zrzuty robocze) trzymaj w scratchpadzie
  sesji, nie w repozytorium. Do repo trafiają tylko zrzuty osadzone w dokumentacji.
- Po każdej małej zmianie — commit (skill `commit`). Nie pytaj o zgodę na commit
  w obrębie tego repozytorium; nie pushuj bez prośby użytkownika.
