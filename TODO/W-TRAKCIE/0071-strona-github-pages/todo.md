---
noteId: "0aa1cca8835b43f7a7b6b2785ac30284"
tytul: "Strona projektu na GitHub Pages — nowy wygląd i workflow „Strona”"
numer: "0071"
status: w-trakcie
priorytet: p2
tags: [todo, strona, github-pages, flatpak]
zalezy_od: []
utworzono: 2026-09-27 11:53
zaktualizowano: 2026-09-27 11:53
zamknieto:
---

# 0071 — Strona projektu na GitHub Pages — nowy wygląd i workflow „Strona”

> [!info] Status
> **w-trakcie** · priorytet **p2** · [← tablica zadań](../../README.md)

## Cel

Zamiast surowej strony z jedną komendą — prawdziwa strona projektu
([dragonking026.github.io/DK-Tracker-Linux](https://dragonking026.github.io/DK-Tracker-Linux/)): czym jest DK Tracker,
zrzut okna, funkcje, instalacja w jednym kroku, konfiguracja; po polsku i angielsku. Strona ma się dać
opublikować bez wydawania nowej wersji aplikacji.

## Kontekst

- Dziś stronę generuje [flatpak/pages.py](../../../flatpak/pages.py) (`index_html`), a publikuje ją tylko
  [wydanie.yml](../../../.github/workflows/wydanie.yml) przy tagu `v*`.
- Pages to jedno wdrożenie: strona **i** repozytorium Flatpaka
  ([ADR-0007](../../../docs/decyzje/0007-dystrybucja-repozytorium-flatpak-na-github-pages.md),
  [GitHub Pages](../../../docs/integracje/github-pages.md)). Każda publikacja podmienia całość — publikacja samej
  strony musi więc zabrać ze sobą działające, podpisane repozytorium.
- Decyzje użytkownika (2026-09-27 11:53): osobny workflow „Strona” (kopiuje opublikowane repozytorium
  `ostree pull --mirror`, podpisuje summary tym samym kluczem, wdraża z nową stroną); strona PL + EN
  z przełącznikiem.
- Proces wydań: [docs/procesy/wydania.md](../../../docs/procesy/wydania.md).

## Kryteria akceptacji

- [ ] Strona statyczna (bez zewnętrznych skryptów i czcionek — zgodnie z brakiem telemetrii), jasny i ciemny motyw,
  działa na telefonie
- [ ] PL i EN z przełącznikiem; domyślnie według języka przeglądarki
- [ ] Komenda instalacji z przyciskiem „kopiuj”, link do `.flatpakref` i `.flatpakrepo`
- [ ] `pages.py` i wydanie publikują nową stronę tak jak dotąd (te same pliki `.flatpakref` / `.flatpakrepo`)
- [ ] Workflow „Strona” publikuje stronę bez wydania; repozytorium Flatpaka po nim działa (`flatpak remote-ls`,
  `flatpak update`)
- [ ] Dokumentacja zaktualizowana ([wydania](../../../docs/procesy/wydania.md),
  [GitHub Pages](../../../docs/integracje/github-pages.md))
- [ ] Zmiany zacommitowane małymi krokami

## Kroki

- [ ] Projekt strony: tokeny, sekcje, oba motywy, szerokość telefonu
- [ ] Szablon strony w repozytorium + `pages.py` go używa, testy
- [ ] Workflow `strona.yml` (mirror repozytorium, podpis summary, wdrożenie)
- [ ] Dokumentacja
- [ ] Publikacja i sprawdzenie na żywo

## Materiały

<!-- Zrzuty strony po wdrożeniu: zrzuty/ -->

## Dziennik

### 2026-09-27 11:53

- Utworzono zadanie. Praca w worktree `.claude/worktrees/strona` (gałąź `strona` od `origin/main`), bo główny katalog
  zajmuje inna sesja.
- **11:53** Start pracy: projekt strony i workflow „Strona”.

## Wynik

<!-- Wypełniane przy zamknięciu: co powstało, gdzie, co zostało na później. -->
