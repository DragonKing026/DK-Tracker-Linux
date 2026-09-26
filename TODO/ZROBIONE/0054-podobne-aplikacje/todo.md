---
noteId: "c7b6c55bc941405a9f383c055fd209e4"
tytul: "Podobne aplikacje: KimaiTray i KimTrack w dokumentacji"
numer: "0054"
status: zrobione
priorytet: p2
tags: [todo, dokumentacja, konkurencja]
zalezy_od: []
utworzono: 2026-09-26 11:42
zaktualizowano: 2026-09-26 11:43
zamknieto: 2026-09-26 11:43
---

# 0054 — Podobne aplikacje: KimaiTray i KimTrack w dokumentacji

> [!info] Status
> **zrobione** · priorytet **p2** · [← tablica zadań](../../README.md)

## Cel

Opisać w dokumentacji istniejące aplikacje tackowe dla Kimai, różnice względem naszej i funkcje, które warto przejąć.

## Kontekst

- Użytkownik znalazł [KimaiTray](https://github.com/Engazan/KimaiTray) w trakcie Planu 4
  ([0047](../../W-TRAKCIE/0047-plan4-metainfo/todo.md)); nazwa „Kimai Tray” zlewa się z ich nazwą.
- Decyzja użytkownika: nie porzucamy projektu ani nie forkujemy KimaiTray; kontynuujemy Plan 4 pod nową nazwą.

## Kryteria akceptacji

- [x] [Podobne aplikacje](../../../docs/architektura/podobne-aplikacje.md): licencja, technologia, paczki, różnice,
  ograniczenia na KDE/Wayland (z kodu)
- [x] Kandydaci F-25…F-32 w [katalogu funkcji](../../../docs/architektura/funkcje.md)
- [x] Link w [indeksie dokumentacji](../../../docs/README.md)

## Kroki

- [x] Sklonować KimaiTray do scratchpada, przejrzeć README i kod (`platform.rs`, `tray/`, `idle.rs`)
- [x] Sprawdzić wydania KimaiTray i KimTrack
- [x] Napisać dokument i dopisać kandydatów

## Materiały

- Wynik: dokument i kandydaci F-25…F-32

## Dziennik

### 2026-09-26

- **11:42** Utworzono zadanie i start.
- **11:43** Zamknięte: dokument i kandydaci F-25…F-32, commity na main.

## Wynik

[Podobne aplikacje](../../../docs/architektura/podobne-aplikacje.md): KimaiTray (MIT, Tauri, deb/rpm/AppImage,
bez polskiego, na Waylandzie środkowy klik i brak pozycjonowania) i KimTrack (zamknięty, płatny). Kandydaci F-25…F-32 w
[katalogu funkcji](../../../docs/architektura/funkcje.md).
