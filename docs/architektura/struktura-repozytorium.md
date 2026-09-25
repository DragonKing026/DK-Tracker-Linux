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
> [Decyzje](../decyzje/README.md).

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
│       ├── nowa-decyzja/      ADR w docs/decyzje/
│       └── sprawdz-linki/     sprawdzanie/naprawa linków, przenoszenie plików (linki.py)
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
    ├── NNNN-slug/             jedno zadanie aktywne — wszystkie jego materiały w środku
    │   ├── todo.md            opis zadania
    │   ├── zrzuty/            zrzuty ekranu
    │   ├── diagramy/          diagramy eksportowane i źródła
    │   ├── testy/             raporty, logi, testy ręczne
    │   ├── prototyp/          kod roboczy / spike
    │   ├── notatki/           notatki badawcze
    │   └── dane/              przykładowe dane
    └── DONE/                  zadania zakończone (zrobione / porzucone)
        └── NNNN-slug/
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
Aktywne zadania leżą bezpośrednio w `TODO/`, zakończone są przenoszone do `TODO/DONE/`.

## Powiązane

- [Indeks dokumentacji](../README.md)
