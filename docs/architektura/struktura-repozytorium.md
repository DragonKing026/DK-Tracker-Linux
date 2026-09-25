---
tytul: Struktura repozytorium
tagi: [architektura, repozytorium]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
---

# Struktura repozytorium

> [!note] Stan na fazę 0
> Opisane są katalogi dokumentacji i agenta. Katalogi kodu (`src/`, `tests/`, `flatpak/`)
> zostaną dopisane po zatwierdzeniu stosu technologicznego — patrz
> [[docs/decyzje/README|Decyzje]].

```
.
├── AGENTS.md                  reguły dla agentów AI (kanoniczne)
├── CLAUDE.md                  import AGENTS.md + specyfika Claude Code
├── README.md                  opis dla ludzi: co to jest, jak zainstalować
├── .gitignore
├── .claude/
│   └── skills/                skille projektu — powtarzalne zadania agenta
│       ├── commit/            mały commit zgodny z konwencją
│       ├── nowe-zadanie/      nowe zadanie w TODO/ z szablonu
│       ├── zamknij-zadanie/   zmiana statusu / zamknięcie zadania
│       ├── nowa-integracja/   dokument integracji w docs/integracje/
│       └── nowa-decyzja/      ADR w docs/decyzje/
├── docs/
│   ├── README.md              indeks (MOC) dokumentacji
│   ├── architektura/          przegląd, funkcje, architektura aplikacji, słownik, ta strona
│   ├── decyzje/               ADR: NNNN-slug.md + README (rejestr)
│   ├── integracje/            jeden plik na integrację + README (indeks)
│   ├── procesy/               commity, dokumentowanie, zadania
│   └── assets/                obrazy współdzielone przez dokumenty
│       └── referencja/        zrzuty wtyczki WS Tracker (wzorzec UI)
└── TODO/
    ├── README.md              tablica: linki do zadań aktywnych i zakończonych
    ├── _szablon/todo.md       szablon zadania
    ├── NNNN-slug/             jedno zadanie aktywne
    │   ├── todo.md
    │   └── assets/            zrzuty i diagramy zadania (opcjonalnie)
    └── DONE/                  zadania zakończone (zrobione / porzucone)
        └── NNNN-slug/
```

## Opis elementów

### `AGENTS.md` / `CLAUDE.md`
Jedno źródło prawdy dla reguł pracy agentów. `CLAUDE.md` zawiera `@AGENTS.md`, więc
Claude Code wczytuje oba; inne narzędzia (Codex, Gemini) czytają `AGENTS.md` bezpośrednio.

### `.claude/skills/`
Każdy skill to folder z `SKILL.md` (frontmatter `name`, `description` + instrukcja krok po
kroku). Claude Code wykrywa je automatycznie jako skille projektu.
Dokumentacja: [Claude Code — Skills](https://docs.claude.com/en/docs/claude-code/skills).

### `docs/`
Pełna dokumentacja — zasady w [[docs/procesy/dokumentowanie|Zasady dokumentowania]].

### `TODO/`
System zadań — zasady w [[docs/procesy/zadania|Zadania w folderze TODO]].
Aktywne zadania leżą bezpośrednio w `TODO/`, zakończone są przenoszone do `TODO/DONE/`.

## Powiązane

- [[docs/README|Indeks dokumentacji]]
