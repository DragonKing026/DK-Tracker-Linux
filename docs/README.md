---
noteId: "0011a9e6b88646238c8e2c7b3f01fddc"
tytul: Dokumentacja — indeks
tags: [indeks, moc]
utworzono: 2026-09-25 17:15
zaktualizowano: 2026-09-27 14:25
---

# Dokumentacja DK Tracker

Mapa treści (MOC) całej dokumentacji. Repozytorium można otworzyć jako vault Obsidiana.

DK Tracker to klient Kimai na pulpit Linuksa: okno główne z wpisami, podsumowaniami i kalendarzem oraz — gdy pulpit
ma tackę — ikona z czasem trwającego wpisu i okienko do szybkiego startu i stopu.

## Start

- [Przegląd projektu](architektura/przeglad.md) — czym jest aplikacja, jak z niej korzystać, zakres i co zostało do 1.0
- [Katalog funkcji](architektura/funkcje.md) — każda funkcja opisana szczegółowo
- [Słownik pojęć](architektura/slownik.md) — Kimai, SNI, portal, billable…
- [Podobne aplikacje](architektura/podobne-aplikacje.md) — KimaiTray i KimTrack: różnice i co warto przejąć

## Specyfikacja

- [Specyfikacja 0.10 — okno główne](specyfikacja/2026-09-26-okno-glowne-0.10.md) — pełny klient Kimai na wzór Toggl:
  Wpisy, Podsumowania, Kalendarz (wydane 0.10.0–0.10.5)
- [Specyfikacja DK Tracker 1.0](specyfikacja/2026-09-25-kimai-tray-1.0.md) — pierwszy etap: parytet z wtyczką WS
  Tracker (tacka, okienko, ustawienia, powiadomienia, Flatpak; wydane jako 0.9.x); dalej obowiązują jej zasady błędów,
  sekretów i testów

## Plany implementacji

- [Indeks planów](plany/README.md) — plany 1–7: rdzeń, integracje, interfejs, Flatpak, okno główne, podsumowania,
  kalendarz (wszystkie wykonane)

## Architektura

- [Struktura repozytorium](architektura/struktura-repozytorium.md)
- [Architektura aplikacji](architektura/architektura-aplikacji.md) — warstwy, komponenty, przepływy
- [Wygląd okna głównego](architektura/wyglad-okna-glownego.md) — kolory obu motywów, kontrolki i ich stany, układ
  widoków

## Decyzje (ADR)

- [Rejestr decyzji](decyzje/README.md)

## Integracje

- [Indeks integracji](integracje/README.md) — Kimai API, Qt / QML, Flatpak, tacka systemowa, GNOME, sekrety,
  portale, projekt referencyjny

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
