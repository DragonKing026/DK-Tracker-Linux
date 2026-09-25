---
noteId: "977ffd4e05cc4a778ade9e8e29f5eb81"
tytul: Konwencja commitów
tags: [proces, git]
utworzono: 2026-09-25 17:13
zaktualizowano: 2026-09-25 17:47
---

# Konwencja commitów

Historia gita jest **dziennikiem projektu**. Dlatego commitujemy często i małymi krokami —
każdy commit ma dać się przeczytać, zrozumieć i w razie potrzeby cofnąć osobno.

## Zasady

1. **Jedna mała zmiana = jeden commit.** Przykłady jednostek: jeden plik dokumentacji,
   jedno nowe zadanie w `TODO/`, jedna funkcja z testem, jedna poprawka.
2. **Commit po każdym ukończonym kroku**, nie na koniec dnia.
3. **Nie przepisujemy historii** (`rebase`, `commit --amend`, `push --force`) na gałęzi
   `main` — historia ma zostać zapisana tak, jak powstawała.
4. Commit zawsze zostawia repozytorium w spójnym stanie (linki w docs działają, kod się
   buduje, testy przechodzą).
5. Zmiana kodu, która zmienia zachowanie → w tym samym commicie lub zaraz po nim
   aktualizacja `docs/`.

## Format — Conventional Commits po polsku

```text
<typ>(<zakres opcjonalny>): <krótki opis w trybie rozkazującym, małą literą>

<opcjonalne ciało: DLACZEGO, nie CO — co widać w diffie>

Refs: TODO/0005-klient-api-kimai
```

| Typ | Kiedy |
| --- | --- |
| `feat` | nowa funkcja aplikacji |
| `fix` | poprawka błędu |
| `docs` | tylko dokumentacja (`docs/`, `README`, `AGENTS.md`) |
| `todo` | zmiany w `TODO/` (nowe zadanie, zmiana statusu) |
| `refactor` | zmiana kodu bez zmiany zachowania |
| `test` | testy |
| `build` | Flatpak, zależności, skrypty budowania |
| `ci` | automatyzacja CI |
| `chore` | porządki, konfiguracja narzędzi, skille agenta |

### Przykłady

```text
docs(integracje): opisz Kimai REST API
todo: dodaj zadanie 0005-klient-api-kimai
feat(tray): pokaż czas trwającego wpisu w podpowiedzi ikony
fix(api): wysyłaj datę rozpoczęcia bez strefy czasowej
chore(skille): dodaj skill nowa-integracja
```

## Stopka

Commity tworzone przez agenta kończą się linią `Co-Authored-By:` wskazaną przez środowisko.

## Powiązane

- [Zadania w TODO](zadania.md)
- [Dokumentowanie](dokumentowanie.md)
- Skill: `.claude/skills/commit/SKILL.md`
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/pl/v1.0.0/)
