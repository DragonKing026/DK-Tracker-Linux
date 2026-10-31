---
noteId: "47d8d230be2e4a47bfa8036553fc0282"
tytul: "Scorecard: przypięte zależności, podpisane wydania, fuzzing"
numer: "0084"
status: w-trakcie
priorytet: p3
tags: [todo, ci, bezpieczenstwo]
zalezy_od: []
utworzono: 2026-10-31 12:50
zaktualizowano: 2026-10-31 12:49
zamknieto:
---

# 0084 — Scorecard: przypięte zależności, podpisane wydania, fuzzing

> [!info] Status
> **w-trakcie** · priorytet **p3** · [← tablica zadań](../../README.md)

## Cel

Podnieść wynik OpenSSF Scorecard w trzech kontrolach: Pinned-Dependencies (instalacja pip z sumami),
Signed-Releases (podpis i pochodzenie artefaktów wydania) i Fuzzing (testy właściwości i harness fuzzujący).

## Kontekst

- Kontynuacja [0083](../../ZROBIONE/0083-ci-z-audytami-bezpieczenstwa/todo.md); opis workflowów:
  [GitHub Actions](../../../docs/integracje/github-actions.md).
- Zadanie 335 w repozytorium Narzędzi (źródło zlecenia).

## Kryteria akceptacji

- [ ] `testy.yml` instaluje zależności przez `pip install --require-hashes`, Dependabot aktualizuje plik z sumami
- [ ] `wydanie.yml` dołącza do wydania podpis i pochodzenie artefaktu (nazwy rozpoznawane przez Scorecard)
- [ ] testy Hypothesis i harness Atheris w repozytorium, uruchamiane w `testy.yml`
- [ ] `actionlint` i `zizmor --offline .github/workflows` bez uwag
- [ ] Dokumentacja zaktualizowana
- [ ] Zmiany zacommitowane małymi krokami

## Kroki

- [ ] Plik wymagań z sumami i zmiana `testy.yml`
- [ ] Podpis i pochodzenie w `wydanie.yml`
- [ ] Testy właściwości i fuzzing
- [ ] Dokumentacja

## Materiały

Brak.

## Dziennik

### 2026-10-31 12:50

- Utworzono zadanie.
- **12:49** Start pracy w worktree zadanie/335-scorecard.
- **12:49** Start pracy w worktree zadanie/335-scorecard.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
