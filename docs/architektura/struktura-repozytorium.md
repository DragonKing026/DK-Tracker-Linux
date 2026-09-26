---
noteId: "5117ce2da6fb45e692d21f2b5fe80086"
tytul: Struktura repozytorium
tags: [architektura, repozytorium]
utworzono: 2026-09-25 17:17
zaktualizowano: 2026-09-26 11:59
---

# Struktura repozytorium

> [!note] Stan po Planie 4
> Opisane są katalogi dokumentacji, agenta, rdzenia, integracji desktopowych, interfejsu, testów i paczki Flatpak
> ([plany](../plany/README.md)).

```text
.
├── AGENTS.md                  reguły dla agentów AI (kanoniczne)
├── CLAUDE.md                  import AGENTS.md + specyfika Claude Code
├── README.md                  opis dla ludzi: co to jest, jak zainstalować
├── LICENSE                    AGPL-3.0-or-later
├── .github/
│   ├── README.md              strona repozytorium na GitHubie (bez frontmattera, treść jak README.md)
│   └── workflows/             testy.yml (każdy push), wydanie.yml (tag v<wersja> → Flatpak, Pages)
├── .gitignore
├── pyproject.toml             pakiet ws-tracker-tray, zależności, pytest, ruff
├── data/                      .desktop i MetaInfo (AppStream) aplikacji — host i Flatpak
├── flatpak/                   manifest, python3-deps.yaml, buduj.sh, publikuj.sh + pages.py (Pages), klucz-gpg.sh
├── dist/                      paczki .flatpak z buduj.sh (poza gitem)
├── scripts/                   instaluj-dev.sh — .desktop i ikona na hoście na czas rozwoju
├── src/ws_tracker_tray/
│   ├── __main__.py            `python -m ws_tracker_tray [--hidden]`
│   ├── core/                  rdzeń bez Qt i D-Bus (plan 1)
│   ├── desktop/               D-Bus na jeepney bez Qt: sekrety, powiadomienia, autostart (plan 2)
│   └── ui/                    Qt Widgets: tacka, okno, ustawienia, kontroler (plan 3)
├── tests/
│   ├── core/                  testy rdzenia (pytest, MockTransport, FakeClient)
│   ├── desktop/               testy D-Bus (FakeBus) + `-m desktop` na prawdziwej sesji
│   ├── kimai/                 Kimai w Dockerze + testy kontraktowe
│   ├── ui/                    testy interfejsu (pytest-qt, `offscreen`)
│   ├── test_architektura.py   zakazane importy między warstwami
│   ├── test_pakiet.py         spójność paczki: wersja, licencja, MetaInfo, manifest, workflowy
│   ├── test_strona_repo.py    pliki strony repozytorium Flatpaka
│   └── test_readme.py         oba README z tą samą treścią
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
│   ├── plany/                 plany implementacji (jeden na podsystem)
│   ├── specyfikacja/          zatwierdzane specyfikacje wersji (RRRR-MM-DD-temat.md)
│   ├── decyzje/               ADR: NNNN-slug.md + README (rejestr)
│   ├── integracje/            jeden plik na integrację + README (indeks)
│   ├── procesy/               commity, dokumentowanie, zadania, wydania
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
