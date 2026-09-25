---
noteId: "f3480932d7974c7883f3c1e0dc5cc63a"
tytul: "Struktura agenta i dokumentacji"
numer: "0001"
status: zrobione
priorytet: p0
tags: [todo, dokumentacja, agent]
zalezy_od: []
utworzono: 2026-09-25 17:23
zaktualizowano: 2026-09-25 17:56
zamknieto: 2026-09-25 17:23
---

# 0001 — Struktura agenta i dokumentacji

> [!info] Status
> **zrobione** · priorytet **p0** · [← tablica zadań](../../README.md)

## Cel

Przygotować repozytorium tak, aby każdy agent AI i człowiek mógł od razu pracować według
jednych zasad: reguły agenta, skille powtarzalnych zadań, system zadań, pełna dokumentacja
z integracjami — zanim powstanie jakikolwiek kod.

## Kontekst

- Prośba użytkownika (2026-09-25): aplikacja Flatpak w tacce (KDE + GNOME) działająca jak
  wtyczka [WS Tracker](../../../docs/integracje/kimai-ws-tracker.md); najpierw struktura agenta
  i dokumentacja, dopiero potem planowanie.
- Decyzja o formie dokumentacji: [ADR-0001](../../../docs/decyzje/0001-dokumentacja-w-repo-jako-vault-obsidian.md).

## Kryteria akceptacji

- [x] [AGENTS.md](../../../AGENTS.md) (kanoniczny) + [CLAUDE.md](../../../CLAUDE.md) (import)
- [x] Skille: `commit`, `nowe-zadanie`, `zamknij-zadanie`, `nowa-integracja`, `nowa-decyzja`
- [x] `TODO/` z tablicą, szablonem i zadaniami jako podfoldery
- [x] `docs/`: indeks, architektura (przegląd, funkcje, architektura, struktura, słownik),
      procesy, decyzje, integracje (jeden plik na integrację, z linkami)
- [x] Zrzuty wzorca UI w `docs/assets/referencja/`, diagramy mermaid w dokumentach
- [x] Linki zewnętrzne sprawdzone (HTTP 200), fakty z dokumentacji źródłowej
- [x] Małe commity po każdym kroku

## Diagramy i zrzuty

Wzorzec UI, do którego odnosi się dokumentacja:

![popup-bezczynny](../../../docs/assets/referencja/popup-bezczynny.png)

## Dziennik

### 2026-09-25
- Sklonowano i przeanalizowano wtyczkę kimai-ws-tracker 1.5.1 (api.js, validate.js,
  popup.js, options.js, background.js, i18n.js).
- Zrzuty wtyczki wykonane z kopii z atrapą `chrome.*` i Kimai API (dane fikcyjne).
- Zweryfikowano na stacji: Fedora 44, Plasma 6.7.5 Wayland, `org.kde.StatusNotifierWatcher`
  (kded6), portal Secret przez `kwallet.portal`/`ksecretd`, powiadomienia `plasmanotify`,
  Flatpak 1.18.2, flatpak-builder 1.4.10 (początkowo niewykryty — użytkownik doinstalował w trakcie sesji).
- Commity:
  - a0fdcb2 docs: dodaj AGENTS.md, CLAUDE.md i .gitignore
  - cf591f8 docs(procesy): opisz konwencję commitów
  - 931c407 docs(procesy): opisz zasady dokumentowania w stylu Obsidian
  - 97b0731 docs(procesy): opisz system zadań w folderze TODO
  - 073abac todo: dodaj tablicę zadań i szablon zadania
  - 16149d8 chore(skille): dodaj skill commit
  - 9c07a2c chore(skille): dodaj skill nowe-zadanie
  - 757db7b chore(skille): dodaj skill zamknij-zadanie
  - 9c2bbe2 chore(skille): dodaj skill nowa-integracja
  - fde5da2 chore(skille): dodaj skill nowa-decyzja (ADR)
  - d5c7cf3 docs: dodaj indeks dokumentacji (MOC)
  - 1938534 docs(architektura): opisz wizję, zakres i ograniczenia projektu
  - c006b0f docs(architektura): dodaj katalog funkcji F-01..F-24 na bazie wtyczki
  - 021360a docs(architektura): opisz strukturę repozytorium
  - 6a4ffdb docs(architektura): dodaj słownik pojęć
  - cf6f939 docs(architektura): szkic logicznej architektury i przepływów
  - b43bc41 docs(adr): dodaj rejestr decyzji i ADR-0001 (dokumentacja jako vault Obsidiana)
  - 46f5821 docs(assets): dodaj zrzuty wtyczki WS Tracker jako wzorzec UI
  - d5fc198 docs(integracje): opisz projekt referencyjny WS Tracker ze zrzutami
  - e64d442 docs(integracje): opisz Kimai REST API (auth, endpointy, daty, błędy)
  - 6a3b313 docs(integracje): opisz StatusNotifierItem (tacka przez D-Bus)
  - 61986f8 docs(integracje): opisz rozszerzenie AppIndicator dla GNOME i tryb bez tacki
  - 5759281 docs(integracje): opisz Flatpak (runtime'y, finish-args, budowanie, dystrybucja)
  - 50afb57 docs(integracje): opisz przechowywanie tokenu (Secret Service / portal Secret)
  - c7d0080 docs(integracje): opisz portale XDG (Background, Notification, OpenURI, skróty)
  - 7261ff2 docs(integracje): dodaj indeks integracji
  - bb23313 docs: dodaj README projektu

## Wynik

- Reguły: [AGENTS.md](../../../AGENTS.md), [CLAUDE.md](../../../CLAUDE.md); skille w [.claude/skills/](../../../.claude/skills).
- Dokumentacja: [indeks](../../../docs/README.md); katalog funkcji F-01…F-24; 7 dokumentów integracji.
- Na później: wybór stosu ([0003](../0003-wybor-stosu/todo.md)), specyfikacja ([0002](../../W-TRAKCIE/0002-specyfikacja-projektu/todo.md)), prototyp tacki ([0004](../../DO-ZROBIENIA/0004-prototyp-tacki-i-okna/todo.md)).
- Znaleziony drobny błąd we wtyczce (szara kropka projektu w stanie bezczynnym) —
  opisany w [WS Tracker](../../../docs/integracje/kimai-ws-tracker.md), nie powielamy go.
