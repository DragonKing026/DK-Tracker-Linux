---
noteId: "5117ce2da6fb45e692d21f2b5fe80086"
tytul: Struktura repozytorium
tags: [architektura, repozytorium]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
---

# Struktura repozytorium

> [!note] Stan na fazę 0
> Opisane są katalogi dokumentacji, agenta i środowiska testowego. Katalogi kodu (`src/`, `flatpak/`)
> zostaną dopisane po zatwierdzeniu stosu technologicznego — patrz
> [Decyzje](../decyzje/README.md).

```
.
├── AGENTS.md                  reguły dla agentów AI (kanoniczne)
├── CLAUDE.md                  import AGENTS.md + specyfika Claude Code
├── README.md                  opis dla ludzi: co to jest, jak zainstalować
├── .gitignore
├── tests/
│   └── kimai/                 lokalny Kimai w Dockerze do testów (compose, kimai-testowe.sh)
├── .claude/
│   └── skills/                skille projektu — powtarzalne zadania agenta
│       ├── commit/            mały commit zgodny z konwencją
│       ├── nowe-zadanie/      nowe zadanie w TODO/ z szablonu
│       ├── zmien-status-zadania/  zmiana statusu, przeniesienie między folderami
│       ├── nowa-integracja/   dokument integracji w docs/integracje/
│       ├── nowa-decyzja/      ADR w docs/decyzje/
│       ├── frontmatter/       noteId + tags w każdym dokumencie (frontmatter.py)
│       └── sprawdz-linki/     sprawdzanie/naprawa linków, przenoszenie plików (linki.py)
├── docs/
│   ├── README.md              indeks (MOC) dokumentacji
│   ├── architektura/          przegląd, funkcje, architektura aplikacji, słownik, ta strona
│   ├── specyfikacja/          zatwierdzane specyfikacje wersji (RRRR-MM-DD-temat.md)
│   ├── decyzje/               ADR: NNNN-slug.md + README (rejestr)
│   ├── integracje/            jeden plik na integrację + README (indeks)
│   ├── procesy/               commity, dokumentowanie, zadania
│   └── assets/                obrazy współdzielone przez dokumenty
│       └── referencja/        zrzuty wtyczki WS Tracker (wzorzec UI)
└── TODO/
    ├── README.md              tablica: linki do wszystkich zadań
    ├── _szablon/todo.md       szablon zadania
    ├── DO-ZROBIENIA/          pomysl, do-zrobienia
    ├── W-TRAKCIE/             w-trakcie, zablokowane
    │   └── NNNN-slug/         jedno zadanie — wszystkie jego materiały w środku
    │       ├── todo.md        opis zadania
    │       ├── zrzuty/        zrzuty ekranu
    │       ├── diagramy/      diagramy eksportowane i źródła
    │       ├── testy/         raporty, logi, testy ręczne
    │       ├── prototyp/      kod roboczy / spike
    │       ├── notatki/       notatki badawcze
    │       └── dane/          przykładowe dane
    └── ZROBIONE/              zrobione, porzucone
```

## Opis elementów

### [AGENTS.md](../../AGENTS.md) / [CLAUDE.md](../../CLAUDE.md)
Jedno źródło prawdy dla reguł pracy agentów. `CLAUDE.md` zawiera `@AGENTS.md`, więc
Claude Code wczytuje oba; inne narzędzia (Codex, Gemini) czytają `AGENTS.md` bezpośrednio.

### `.claude/skills/`
Każdy skill to folder z `SKILL.md` (frontmatter `name`, `description` + instrukcja krok po
kroku). Claude Code wykrywa je automatycznie jako skille projektu.
Dokumentacja: [Claude Code — Skills](https://docs.claude.com/en/docs/claude-code/skills).

### `docs/`
Pełna dokumentacja — zasady w [Zasady dokumentowania](../procesy/dokumentowanie.md).

### `TODO/`
System zadań — zasady w [Zadania w folderze TODO](../procesy/zadania.md).
Zadania leżą w podfolderach według statusu: `DO-ZROBIENIA/`, `W-TRAKCIE/`, `ZROBIONE/`.

## Powiązane

- [Indeks dokumentacji](../README.md)
