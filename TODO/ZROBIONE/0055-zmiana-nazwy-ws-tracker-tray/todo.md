---
noteId: "37a127515a764085977469140214ca1b"
tytul: "Zmiana nazwy na WS Tracker Tray"
numer: "0055"
status: zrobione
priorytet: p1
tags: [todo, nazwa, flatpak]
zalezy_od: ["0054"]
utworzono: 2026-09-26 11:46
zaktualizowano: 2026-09-26 11:48
zamknieto: 2026-09-26 11:48
---

# 0055 — Zmiana nazwy na WS Tracker Tray

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Zmienić nazwę aplikacji przed wydaniem 0.9.0, bo „Kimai Tray” zlewa się z istniejącą aplikacją KimaiTray
([podobne aplikacje](../../../docs/architektura/podobne-aplikacje.md)). Nowa nazwa nawiązuje do wtyczki
[kimai-ws-tracker](../../../docs/integracje/kimai-ws-tracker.md), na której się wzorujemy.

## Kontekst

Decyzje użytkownika (2026-09-26 11:45):

| Co | Było | Jest |
| --- | --- | --- |
| Nazwa | Kimai Tray | **WS Tracker Tray** |
| Identyfikator | `pl.websystems.KimaiTray` | `pl.websystems.WsTrackerTray` |
| Komenda, katalogi, dystrybucja | `kimai-tray` | `ws-tracker-tray` |
| Pakiet Pythona | `kimai_tray` | `ws_tracker_tray` |

Nazwa repozytorium na GitHubie (`Kimai-App--Linux-`) zostaje.

## Kryteria akceptacji

- [x] Kod, testy, dane (`.desktop`, MetaInfo), skrypty i żywa dokumentacja używają nowej nazwy
- [x] Plan 4 opisuje nowe nazwy plików i identyfikator
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag, linki i markdownlint OK

## Kroki

- [x] Przenieść `src/kimai_tray` i pliki `data/` (`linki.py przenies`)
- [x] Zamienić nazwy w kodzie, testach i dokumentacji
- [x] Przeinstalować pakiet w `.venv`, testy

## Materiały

- [testy/pytest-2026-09-26.txt](testy/pytest-2026-09-26.txt) — końcowy przebieg:
  `403 passed, 1 skipped, 12 deselected in 2.44s`

## Dziennik

### 2026-09-26

- **11:46** Utworzono zadanie i start.
- **11:48** Zamknięte: 403 passed, 1 skipped, 12 deselected in 2.44s, commity na main.

## Wynik

Kod, testy, dane, skrypty, Plan 4 i żywa dokumentacja pod nazwą **WS Tracker Tray**: pakiet
[ws_tracker_tray](../../../src/dk_tracker/__init__.py),
[.desktop](../../../data/io.github.dragonking026.DK-Tracker-Linux.desktop),
[MetaInfo](../../../data/io.github.dragonking026.DK-Tracker-Linux.metainfo.xml). Historia (zamknięte zadania, plany 1–3,
prototypy
w 0045) zostaje ze starą nazwą; nazwa pliku specyfikacji też. Stary Kimai testowy w Dockerze działa pod projektem
`kimai-tray-test` — usunąć raz: `docker compose -p kimai-tray-test down -v`.
