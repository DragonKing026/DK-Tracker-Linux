---
noteId: "37a127515a764085977469140214ca1b"
tytul: "Zmiana nazwy na WS Tracker Tray"
numer: "0055"
status: w-trakcie
priorytet: p1
tags: [todo, nazwa, flatpak]
zalezy_od: ["0054"]
utworzono: 2026-09-26 11:46
zaktualizowano: 2026-09-26 11:46
zamknieto:
---

# 0055 — Zmiana nazwy na WS Tracker Tray

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

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

- [ ] Kod, testy, dane (`.desktop`, MetaInfo), skrypty i żywa dokumentacja używają nowej nazwy
- [ ] Plan 4 opisuje nowe nazwy plików i identyfikator
- [ ] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag, linki i markdownlint OK

## Kroki

- [ ] Przenieść `src/kimai_tray` i pliki `data/` (`linki.py przenies`)
- [ ] Zamienić nazwy w kodzie, testach i dokumentacji
- [ ] Przeinstalować pakiet w `.venv`, testy

## Materiały

Brak.

## Dziennik

### 2026-09-26

- **11:46** Utworzono zadanie i start.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
