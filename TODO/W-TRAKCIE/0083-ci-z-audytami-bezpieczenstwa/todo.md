---
noteId: "93fbe2f6ba694705af074e8b2fd01bce"
tytul: "CI z audytami bezpieczeństwa"
numer: "0083"
status: w-trakcie
priorytet: p2
tags: [todo, ci, bezpieczenstwo]
zalezy_od: []
utworzono: 2026-10-31 12:23
zaktualizowano: 2026-10-31 12:26
zamknieto:
---

# 0083 — CI z audytami bezpieczeństwa

> [!info] Status
> **w-trakcie** · priorytet **p2** · [← tablica zadań](../../README.md)

## Cel

Dodać do publicznego repozytorium zestaw automatycznych audytów bezpieczeństwa (CodeQL, gitleaks, zizmor, OpenSSF
Scorecard, Dependabot, polityka zgłaszania podatności), żeby błędy i wycieki były widoczne przy każdej zmianie.

## Kontekst

- Wzorzec: ten sam zestaw działa w repozytorium commit-sentry (CodeQL, gitleaks, zizmor, Scorecard, Dependabot).
- Istniejące workflowy ([GitHub Actions](../../../docs/integracje/github-actions.md)) zostają bez zmian logiki:
  `strona.yml` i `wydanie.yml` publikują Pages i podpisane wydania.
- Powiązane dokumenty: [Dokumentacja](../../../docs/README.md)

## Kryteria akceptacji

- [x] `codeql.yml`, `security.yml` (gitleaks + zizmor), `scorecard.yml` i `dependabot.yml` w `.github/`
- [x] `.github/SECURITY.md` i odznaki na górze `.github/README.md`
- [ ] `actionlint` i `zizmor --offline --min-severity low .github/workflows` bez uwag
- [ ] pierwsze przebiegi na GitHubie zielone (po pushu)
- [x] Dokumentacja zaktualizowana
- [ ] Zmiany zacommitowane małymi krokami

## Kroki

- [x] Nowe workflowy i konfiguracja Dependabota
- [x] SECURITY.md i odznaki
- [x] Opis w docs/integracje/github-actions.md
- [x] Weryfikacja lokalna (actionlint, zizmor, gitleaks, sprawdzenia docs)
- [ ] Pierwsze przebiegi na GitHubie (po pushu)

## Materiały

Wszystkie materiały zadania leżą w jego folderze (podfoldery tworzone, gdy są potrzebne):

- `zrzuty/` — zrzuty ekranu
- `diagramy/` — diagramy eksportowane i ich źródła
- `testy/` — scenariusze testów ręcznych, raporty, logi
- `prototyp/` — kod roboczy / spike
- `notatki/` — notatki badawcze, porównania
- `dane/` — przykładowe dane, odpowiedzi API

<!-- Linki w szablonie są liczone z miejsca zadania: TODO/<STATUS>/NNNN-slug/todo.md -->
<!-- Osadzenie: ![opis](zrzuty/plik.png) · link: [raport](testy/raport.md) · diagram mermaid inline -->

## Dziennik

### 2026-10-31 12:23

- Utworzono zadanie.
- **12:23** Start pracy: worktree ci/audyty.

- 2026-10-31 12:26 — zrobione lokalnie w worktree `ci/audyty` (gałąź nie scalona, bez pushu): workflowy `codeql.yml`,
  `security.yml`,
  `scorecard.yml`, `dependabot.yml` (tylko akcje; `pip` pominięty — zależności Flatpaka są przypięte offline),
  `SECURITY.md`, odznaki, opis w [GitHub Actions](../../../docs/integracje/github-actions.md). W istniejących
  workflowach
  tylko `persist-credentials: false` i wyjątek zizmor `self-repository`. Czeka: push, pierwsze przebiegi na GitHubie,
  dopisanie `ossf/scorecard-action` do dozwolonych akcji w ustawieniach repozytorium.

## Wynik

<!-- Wypełniane przy zamknięciu: co powstało, gdzie, co zostało na później. -->
