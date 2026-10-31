---
noteId: "93fbe2f6ba694705af074e8b2fd01bce"
tytul: "CI z audytami bezpieczeństwa"
numer: "0083"
status: zrobione
priorytet: p2
tags: [todo, ci, bezpieczenstwo]
zalezy_od: []
utworzono: 2026-10-31 12:23
zaktualizowano: 2026-10-31 12:45
zamknieto: 2026-10-31 12:45
---

# 0083 — CI z audytami bezpieczeństwa

> [!info] Status
> **zrobione** · priorytet **p2** · [← tablica zadań](../../README.md)

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
- [x] `actionlint` i `zizmor --offline --min-severity low .github/workflows` bez uwag
- [x] pierwsze przebiegi na GitHubie zielone (po pushu)
- [x] Dokumentacja zaktualizowana
- [x] Zmiany zacommitowane małymi krokami

## Kroki

- [x] Nowe workflowy i konfiguracja Dependabota
- [x] SECURITY.md i odznaki
- [x] Opis w docs/integracje/github-actions.md
- [x] Weryfikacja lokalna (actionlint, zizmor, gitleaks, sprawdzenia docs)
- [x] Pierwsze przebiegi na GitHubie (po pushu)

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
- 2026-10-31 12:43 — push na `main` (c894023) za zgodą użytkownika; `ossf/scorecard-action@*` dopisane do dozwolonych
  akcji, ochrona `main` (bez force-push i usuwania, bez wymogu PR), prywatne zgłoszenia, alerty Dependabota, secret
  scanning z push protection. Pierwszy przebieg Testy czerwony: `test_readme` wymaga tej samej treści w obu README —
  odznaki dopisane też do `README.md` (2d9d261). Na 2d9d261 zielone: Testy, CodeQL, Security, Scorecard.
- **12:45** Przebiegi na GitHubie zielone (2d9d261).

## Wynik

Audyty w GitHub Actions: CodeQL (Python), gitleaks + zizmor, OpenSSF Scorecard (wynik 6,4 — 2026-10-31; niskie
głównie Code-Review i Branch-Protection przy pracy jednego autora bez PR), Dependabot dla akcji (grupowany, karencja
7 dni), [SECURITY.md](../../../.github/SECURITY.md), odznaki w obu README. Na później: PR-y Dependabota zmieniają też
przypięcia w `wydanie.yml` i `strona.yml` — przeglądać jak zmianę kodu.
