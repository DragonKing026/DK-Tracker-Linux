---
noteId: "a03fbe53f8384175b06b39eaf5ee63cc"
tytul: "Dependabot gubi zależności z pyproject.toml w requirements-ci.txt"
numer: "0087"
status: zrobione
priorytet: p1
tags: [todo, ci, zaleznosci]
zalezy_od: []
utworzono: 2026-11-20 10:10
zaktualizowano: 2026-11-20 10:19
zamknieto: 2026-11-20 10:19
---

# 0087 — Dependabot gubi zależności z pyproject.toml w requirements-ci.txt

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Cotygodniowy pull request Dependabota z zależnościami CI ma dawać kompletny `requirements-ci.txt`, na którym
przechodzą testy.

## Kontekst

- [PR #5](https://github.com/DragonKing026/DK-Tracker-Linux/pull/5) (hypothesis, pyside6, setuptools) usuwa
  z [requirements-ci.txt](../../../requirements-ci.txt) wszystko poza `atheris`. Dependabot kompiluje plik tylko
  z [requirements-ci.in](../../../requirements-ci.in) i pomija drugie wejście z nagłówka, `pyproject.toml`
  z extras `dev` i `ui`. Testy w CI padają na `No module named 'setuptools'`.
- Opis generowania: [GitHub Actions](../../../docs/integracje/github-actions.md),
  konfiguracja: [dependabot.yml](../../../.github/dependabot.yml).

## Kryteria akceptacji

- [x] `requirements-ci.txt` generowany z jednego pliku `requirements-ci.in`, który zawiera wszystkie zależności CI
- [x] Test pilnuje, że `requirements-ci.in` obejmuje zależności i extras z `pyproject.toml`
- [x] Zależności podniesione (zastępuje PR #5), PR #5 zamknięty z komentarzem
- [x] Dokumentacja zaktualizowana

## Kroki

- [x] Przenieść zależności `pyproject.toml` (główne, `dev`, `ui`) do `requirements-ci.in`
- [x] Test zgodności `requirements-ci.in` z `pyproject.toml`
- [x] Wygenerować `requirements-ci.txt` nowym poleceniem, uruchomić testy
- [x] Zaktualizować dokumentację
- [x] Zamknąć PR #5

## Materiały

Brak.

## Dziennik

### 2026-11-20 10:10

- Utworzono zadanie.
- **10:11** Start pracy: zależności CI w jednym pliku wejściowym.
- **10:19** requirements-ci.in z kompletem zależności (b904636), test zgodności (6220fb8), docs (5cd146e); testy CI na
  main zielone; PR #5 zamknięty przez Dependabota, dopisany komentarz.

## Wynik

- `requirements-ci.in` zawiera wszystkie zależności CI; `requirements-ci.txt` generowany tylko z niego.
- Test `tests/test_requirements_ci.py` pilnuje zgodności zakresów z `pyproject.toml`.
- Dokumentacja: [GitHub Actions](../../../docs/integracje/github-actions.md).
