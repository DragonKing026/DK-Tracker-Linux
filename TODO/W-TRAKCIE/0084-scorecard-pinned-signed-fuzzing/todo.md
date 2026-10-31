---
noteId: "47d8d230be2e4a47bfa8036553fc0282"
tytul: "Scorecard: przypięte zależności, podpisane wydania, fuzzing"
numer: "0084"
status: w-trakcie
priorytet: p3
tags: [todo, ci, bezpieczenstwo]
zalezy_od: []
utworzono: 2026-10-31 12:50
zaktualizowano: 2026-10-31 13:15
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

- [x] `testy.yml` instaluje zależności przez `pip install --require-hashes`, Dependabot aktualizuje plik z sumami
- [x] `wydanie.yml` dołącza do wydania podpis i pochodzenie artefaktu (nazwy rozpoznawane przez Scorecard)
- [x] testy Hypothesis i harness Atheris w repozytorium, uruchamiane w `testy.yml` (Scorecard wykrywa tylko
      `import atheris`)
- [x] `actionlint` i `zizmor --offline .github/workflows` bez uwag
- [x] Dokumentacja zaktualizowana
- [x] Zmiany zacommitowane małymi krokami

## Kroki

- [x] Plik wymagań z sumami i zmiana `testy.yml`
- [x] Podpis i pochodzenie w `wydanie.yml`
- [x] Testy właściwości i fuzzing
- [x] Dokumentacja

## Materiały

Brak.

## Dziennik

### 2026-10-31 13:04

- Po recenzji: obraz kontenera Flatpak przypięty do digestu `sha256:b0a8a2ac…` (indeks OCI tagu `kde-6.11`, `skopeo`) w `wydanie.yml`, `strona.yml`, `buduj.sh`; `pages` czeka na `poswiadczenie`; `ignore` w Dependabocie dla górnych granic z `pyproject.toml`; scalono `origin/main`.

### 2026-10-31 13:15

- Zależności CI z sumami (`requirements-ci.txt`, uv), Dependabot pip, `testy.yml` z `--require-hashes`.
- `wydanie.yml`: zadanie `poswiadczenie` (attest-build-provenance v4.2.2), bundle jako `*.flatpak.sigstore.json`.
- Testy Hypothesis (`tests/core/test_properties.py`) i harness Atheris (`fuzz/fuzz_core.py`, 30 s w CI).
- Do sprawdzenia po scaleniu i wypchnięciu: przebieg `testy.yml` na GitHubie; Signed-Releases po następnym wydaniu.

### 2026-10-31 12:50

- Utworzono zadanie.
- **12:49** Start pracy w worktree zadanie/335-scorecard.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
