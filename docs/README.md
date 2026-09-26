---
noteId: "0011a9e6b88646238c8e2c7b3f01fddc"
tytul: Dokumentacja — indeks
tags: [indeks, moc]
utworzono: 2026-09-25 17:15
zaktualizowano: 2026-09-25 18:49
---

# Dokumentacja WS Tracker Tray

Mapa treści (MOC) całej dokumentacji. Repozytorium można otworzyć jako vault Obsidiana.

## Start

- [Przegląd projektu](architektura/przeglad.md) — co budujemy, dla kogo, zakres
- [Katalog funkcji](architektura/funkcje.md) — każda funkcja opisana szczegółowo
- [Słownik pojęć](architektura/slownik.md) — Kimai, SNI, portal, billable…
- [Podobne aplikacje](architektura/podobne-aplikacje.md) — KimaiTray i KimTrack: różnice i co warto przejąć

## Specyfikacja

- [Specyfikacja WS Tracker Tray 1.0](specyfikacja/2026-09-25-kimai-tray-1.0.md) — zakres, architektura, przepływ, błędy,
  testy (zaakceptowana 2026-09-25)

## Plany implementacji

- [Indeks planów](plany/README.md) — Plan 1: rdzeń (do akceptacji), plany 2–4

## Architektura

- [Struktura repozytorium](architektura/struktura-repozytorium.md)
- [Architektura aplikacji](architektura/architektura-aplikacji.md) — warstwy, komponenty, przepływy

## Decyzje (ADR)

- [Rejestr decyzji](decyzje/README.md)

## Integracje

- [Indeks integracji](integracje/README.md) — Kimai API, Flatpak, tacka systemowa,
  GNOME, sekrety, portale, projekt referencyjny

## Procesy

- [Konwencja commitów](procesy/commity.md)
- [Zasady dokumentowania](procesy/dokumentowanie.md)
- [Zadania w folderze TODO](procesy/zadania.md)
- [Wydania i instalacja](procesy/wydania.md) — klucz, tag, GitHub Actions, instalacja z repozytorium Flatpaka

## Zadania

- [Tablica zadań](../TODO/README.md)

## Dla agentów AI

- [AGENTS.md](../AGENTS.md) — reguły pracy (kanoniczne)
- [CLAUDE.md](../CLAUDE.md) — dodatki dla Claude Code
- [.claude/skills/](../.claude/skills) — skille powtarzalnych zadań: [commit](../.claude/skills/commit/SKILL.md),
  [nowe-zadanie](../.claude/skills/nowe-zadanie/SKILL.md),
  [zmien-status-zadania](../.claude/skills/zmien-status-zadania/SKILL.md),
  [nowa-integracja](../.claude/skills/nowa-integracja/SKILL.md),
  [nowa-decyzja](../.claude/skills/nowa-decyzja/SKILL.md), [sprawdz-linki](../.claude/skills/sprawdz-linki/SKILL.md)
