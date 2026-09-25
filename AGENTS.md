---
noteId: "89dff851412245e891d8c9747315e23d"
tags: []
---

# AGENTS.md — instrukcje dla agentów AI

> Plik kanoniczny dla wszystkich agentów (Claude Code, Codex, Gemini itp.).
> [CLAUDE.md](CLAUDE.md) importuje ten plik — **zmiany reguł wprowadzaj tutaj**, nie w [CLAUDE.md](CLAUDE.md).

## 1. Czym jest ten projekt

**Kimai Tray** (nazwa robocza) — natywna aplikacja desktopowa na Linuksa, dystrybuowana jako
**Flatpak**, która siedzi w **tacce systemowej** (KDE Plasma i GNOME) i pozwala zarządzać
czasem pracy w firmowym **Kimai** bez otwierania przeglądarki.

Funkcjonalnie odwzorowuje wtyczkę przeglądarkową
[kimai-ws-tracker](https://github.com/websystemspl/kimai-ws-tracker) (Web Systems):
start/stop timera, lista ostatnich wpisów, wznawianie, edycja trwającego wpisu, flaga
„billable”, sumy dzienne/tygodniowe, walidacja jakości opisu.
Szczegóły: [docs/integracje/kimai-ws-tracker.md](docs/integracje/kimai-ws-tracker.md).

Status: **faza 1 — specyfikacja i planowanie**.
Stos: **Python + PySide6 (Qt 6), Flatpak na `org.kde.Platform` 6.11** —
[ADR-0002](docs/decyzje/0002-stos-python-pyside6.md).

## 2. Mapa repozytorium

```
AGENTS.md              ← ten plik (reguły dla agentów)
CLAUDE.md              ← import AGENTS.md + specyfika Claude Code
README.md              ← opis dla ludzi
.claude/skills/        ← skille projektu (powtarzalne zadania)
docs/                  ← pełna dokumentacja projektu (Obsidian vault-friendly)
  README.md            ← indeks (MOC) dokumentacji
  architektura/        ← jak działa aplikacja, komponenty, przepływy
  decyzje/             ← ADR — rejestr decyzji architektonicznych
  integracje/          ← jeden plik .md na każdą integrację zewnętrzną + linki
  procesy/             ← workflow: commity, TODO, dokumentowanie, wydania
  assets/              ← zrzuty ekranu, diagramy wyeksportowane, obrazy
TODO/                  ← zadania aktywne; każde zadanie = podfolder z plikiem todo.md
  README.md            ← tablica: linki do zadań aktywnych i zakończonych
  _szablon/            ← szablon nowego zadania
  DONE/                ← zadania zakończone (przenoszone przez skill zamknij-zadanie)
```

Pełny opis struktury: [docs/architektura/struktura-repozytorium.md](docs/architektura/struktura-repozytorium.md).

## 3. Złote zasady (obowiązkowe)

1. **Język**: dokumentacja, TODO, commity i komunikacja — **po polsku**. Identyfikatory
   w kodzie, nazwy plików kodu i komentarze w kodzie — po angielsku.
2. **Małe commity, często.** Każda logiczna, mała zmiana = osobny commit (jeden plik docs,
   jedno zadanie TODO, jedna funkcja). Nie zbieraj wielu zmian w jeden commit.
   Format: [docs/procesy/commity.md](docs/procesy/commity.md) (Conventional Commits po polsku).
3. **Dokumentacja na bieżąco.** Zmiana w kodzie, która zmienia zachowanie, strukturę
   albo integrację, **musi** w tym samym lub następnym commicie zaktualizować `docs/`.
   Kod bez dokumentacji = zadanie nieskończone.
4. **Każde zadanie ma folder w `TODO/`.** Zanim zaczniesz pracę — utwórz/zaktualizuj
   zadanie (skill `nowe-zadanie`). Po skończeniu — zmień status, opisz wynik i przenieś
   folder do [TODO/DONE/](TODO/DONE) (skill `zamknij-zadanie`). [TODO/README.md](TODO/README.md) zawsze linkuje
   do każdego aktywnego zadania.
5. **Każda integracja ma plik w `docs/integracje/`** z linkami do oficjalnej dokumentacji
   (skill `nowa-integracja`). Nie wolno dodać zależności zewnętrznej bez tego pliku.
6. **Decyzje architektoniczne zapisuj jako ADR** w `docs/decyzje/` (skill `nowa-decyzja`).
7. **Weryfikuj fakty o bibliotekach** przez Context7 / oficjalną dokumentację — nie
   z pamięci. Linki w docs muszą prowadzić do źródeł.
8. **Obrazy i diagramy**: diagramy jako bloki ` ```mermaid ` bezpośrednio w `.md`
   (Obsidian i GitHub je renderują).
9. **Materiały zadania w folderze zadania.** Wszystko, co powstaje przy zadaniu, trafia
   do jego folderu, w podfolder według rodzaju: `zrzuty/`, `diagramy/`, `testy/`
   (raporty, logi, testy ręczne), `prototyp/`, `notatki/`, `dane/`. Każdy plik jest
   podlinkowany w `todo.md`. Do `docs/assets/` trafiają tylko obrazy wspólne dla
   dokumentacji. Szczegóły: [docs/procesy/zadania.md](docs/procesy/zadania.md).
10. **Sekrety**: token API Kimai nigdy nie trafia do repo, logów ani plików konfiguracyjnych
   w czystym tekście — tylko do magazynu sekretów systemu (Secret Service / portal).
11. **Bez telemetrii.** Aplikacja łączy się wyłącznie z adresem Kimai podanym przez użytkownika.

## 4. Konwencje dokumentów (Obsidian)

- Każdy plik `.md` w `docs/` i `TODO/` zaczyna się od **frontmatter YAML**
  (`noteId`, `tytul`, `tags`, `utworzono`, `zaktualizowano`, dla zadań także `status`,
  `priorytet`). `noteId` i `tags` są obowiązkowe we **wszystkich** plikach `.md` poza
  `.claude/`, bo inaczej dopisuje je rozszerzenie VS Code *notebook*. Skill
  [frontmatter](.claude/skills/frontmatter/SKILL.md): `frontmatter.py sprawdz` przed commitem.
- Linki wewnętrzne: **względne linki markdown** `[etykieta](../ścieżka/plik.md)`, działają
  w VS Code, Obsidianie i na GitHubie. **Wikilinki `[[...]]` są zakazane.** Każde odwołanie
  do zadania, ADR, dokumentu czy pliku jest linkiem, nie zwykłym tekstem.
- Pliki `.md` przenosimy tylko przez `linki.py przenies`. Przed commitem uruchamiamy
  `linki.py sprawdz` (skill [sprawdz-linki](.claude/skills/sprawdz-linki/SKILL.md)).
- Linki zewnętrzne: zwykły markdown, sprawdzone (HTTP 200).
- Uwagi: callouty Obsidiana — `> [!note]`, `> [!warning]`, `> [!tip]`, `> [!todo]`.
- Listy zadań: `- [ ]` / `- [x]`.
- Daty w formacie ISO: `2026-09-25`.

Szczegóły: [docs/procesy/dokumentowanie.md](docs/procesy/dokumentowanie.md).

## 5. Skille projektu (`.claude/skills/`)

| Skill | Kiedy użyć |
|---|---|
| [nowe-zadanie](.claude/skills/nowe-zadanie/SKILL.md) | tworzenie zadania w `TODO/` z szablonu |
| [zamknij-zadanie](.claude/skills/zamknij-zadanie/SKILL.md) | zamknięcie zadania: status, wynik, przeniesienie do `TODO/DONE/`, tablica, commit |
| [nowa-integracja](.claude/skills/nowa-integracja/SKILL.md) | dodanie pliku integracji w `docs/integracje/` |
| [nowa-decyzja](.claude/skills/nowa-decyzja/SKILL.md) | zapis decyzji architektonicznej (ADR) |
| [frontmatter](.claude/skills/frontmatter/SKILL.md) | `noteId` + `tags` w każdym dokumencie; naprawa i nowy `noteId` |
| [sprawdz-linki](.claude/skills/sprawdz-linki/SKILL.md) | sprawdzenie i naprawa linków, przenoszenie plików `.md` z poprawą linków |
| [commit](.claude/skills/commit/SKILL.md) | przygotowanie małego commita zgodnego z konwencją |

## 6. Workflow pracy agenta

```mermaid
flowchart LR
    A[Prośba użytkownika] --> B{Jest zadanie w TODO?}
    B -- nie --> C[skill: nowe-zadanie]
    B -- tak --> D[Status: w-toku]
    C --> D
    D --> E[Praca w małych krokach]
    E --> F[Aktualizacja docs/]
    F --> L[skill: sprawdz-linki]
    L --> G[skill: commit]
    G --> H{Zadanie skończone?}
    H -- nie --> E
    H -- tak --> I[skill: zamknij-zadanie]
```

## 7. Komendy

> [!todo] Uzupełnić przy szkielecie projektu (zadanie [0002](TODO/W-TRAKCIE/0002-specyfikacja-projektu/todo.md)).
> Tu trafią: uruchomienie w trybie dev, testy (pytest, pytest-qt), lint, budowa Flatpaka.
