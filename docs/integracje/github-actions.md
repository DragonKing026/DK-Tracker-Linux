---
noteId: "bf2d2fabf984496cbc731b1f3c66b604"
tytul: GitHub Actions
tags: [integracja, ci, wydanie, github]
status_integracji: w-uzyciu
wersja: "akcje: checkout@v4, setup-python@v5, flatpak-builder@v6, ghaction-import-gpg@v6, upload-pages-artifact@v3, deploy-pages@v4, action-gh-release@v2"
utworzono: 2026-09-26 11:57
zaktualizowano: 2026-09-26 11:57
---

# GitHub Actions

> [!info] W skrócie
> CI repozytorium na GitHubie: testy przy każdym pushu na `main` i pull requeście, a po tagu `v<wersja>` —
> podpisana paczka Flatpak, repozytorium Flatpaka na [GitHub Pages](github-pages.md) i wydanie z plikiem `.flatpak`.

## Do czego używamy

| Workflow | Kiedy | Co robi |
| --- | --- | --- |
| [testy.yml](../../.github/workflows/testy.yml) | push na `main`, pull request | `ruff format --check`, `ruff check`, `pytest` (Qt offscreen), linki, frontmatter, markdownlint |
| [wydanie.yml](../../.github/workflows/wydanie.yml) | tag `v*` | testy (`testy.yml` jako `workflow_call`), zgodność tagu z `pyproject.toml`, walidacja MetaInfo, klucz GPG, budowa i podpis, Pages, na końcu wydanie |

## Jak to działa

```mermaid
flowchart LR
    TAG[git push tag v0.9.0] --> T[testy.yml]
    T --> V{tag = wersja<br/>w pyproject?}
    V -- nie --> STOP[koniec, bez budowy]
    V -- tak --> GPG[import klucza<br/>FLATPAK_GPG_PRIVATE_KEY]
    GPG --> B[flatpak-builder@v6<br/>repo + paczka]
    B --> P[publikuj.sh<br/>klucz = repo.gpg?<br/>podpis refów, strona]
    P --> DEP[deploy-pages]
    DEP --> REL[action-gh-release<br/>plik .flatpak]
```

Zadanie `flatpak` działa w kontenerze `ghcr.io/flathub-infra/flatpak-github-actions:kde-6.11` z `--privileged` — tym
samym obrazem co lokalna budowa ([buduj.sh](../../flatpak/buduj.sh),
[ADR-0006](../decyzje/0006-budowanie-flatpaka-w-kontenerze.md));
spójność pilnuje test `test_release_builds_in_the_same_container_as_the_local_script`
([test_pakiet.py](../../tests/test_pakiet.py)).

Użyte akcje:

- [actions/checkout](https://github.com/actions/checkout) i
  [actions/setup-python](https://github.com/actions/setup-python)
  — kod i Python 3.13 do testów.
- [flatpak/flatpak-github-actions](https://github.com/flatpak/flatpak-github-actions) (`flatpak-builder@v6`) — budowa z
  manifestu (`manifest-path`), paczka (`bundle`), podpis (`gpg-sign`); repozytorium OSTree ląduje w katalogu `repo`,
  gałąź domyślna `master`.
- [crazy-max/ghaction-import-gpg](https://github.com/crazy-max/ghaction-import-gpg) — klucz z sekretu, wynik
  `fingerprint`.
- [actions/upload-pages-artifact](https://github.com/actions/upload-pages-artifact) i
  [actions/deploy-pages](https://github.com/actions/deploy-pages) — publikacja katalogu `site`.
- [softprops/action-gh-release](https://github.com/softprops/action-gh-release) — wydanie z paczką; tagi `v0.*` jako
  pre-release.

## Konfiguracja / uprawnienia

- Sekret repozytorium **`FLATPAK_GPG_PRIVATE_KEY`** — klucz prywatny z [klucz-gpg.sh](../../flatpak/klucz-gpg.sh)
  ([Using secrets](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions)).
- `wydanie.yml`: domyślnie tylko `contents: read`; `pages: write` i `id-token: write` ma wyłącznie zadanie `pages`,
  `contents: write` — zadanie `wydanie`. Zadanie z kluczem GPG nie ma uprawnień zapisu.
- Ustawienia repozytorium → Pages → źródło **GitHub Actions** ([github-pages](github-pages.md)).

## Przypięte akcje

**Wszystkie** akcje są przypięte do commita (SHA). Repozytorium tego wymaga (Settings → Actions → General: tylko
akcje GitHuba i trzy wymienione niżej, wymóg pełnego SHA), a zadanie z akcjami firm trzecich dostaje klucz prywatny GPG
—
przesunięty tag nie zmieni uruchamianego kodu. Wymóg obejmuje też akcje wywoływane **wewnątrz** akcji złożonych
(composite), dlatego `upload-pages-artifact` jest w wersji v4.0.0, która sama przypina `upload-artifact` do SHA (v3
wołała go po tagu). Pilnuje tego `test_every_action_is_pinned_to_a_commit`
([test_pakiet.py](../../tests/test_pakiet.py)).

| Akcja | Wersja | Commit |
| --- | --- | --- |
| actions/checkout | v4.4.0 | `11d5960a326750d5838078e36cf38b85af677262` |
| actions/setup-python | v5.6.0 | `a26af69be951a213d495a4c3e4e4022e16d87065` |
| actions/upload-pages-artifact | v4.0.0 | `7b1f4a764d45c48632c6b24a0339c27f5614fb0b` |
| actions/deploy-pages | v4.0.5 | `d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e` |
| actions/upload-artifact | v4.6.2 | `ea165f8d65b6e75b540449e92b4886f43607fa02` |
| actions/download-artifact | v4.3.0 | `d3f86a106a0bac45b974a628896c90dbdf5c8093` |
| crazy-max/ghaction-import-gpg | v6.3.0 | `e89d40939c28e39f97cf32126055eeae86ba74ec` |
| flatpak/flatpak-github-actions/flatpak-builder | v6.8 | `79327416609af08178ad73b352877e51450790b3` |
| softprops/action-gh-release | v2.6.2 | `3bb12739c298aeb8a4eeaf626c5b8d85266b0e65` |

Aktualizacja ręczna: przejrzeć zmiany między wersjami w repozytorium akcji, potem

```bash
gh api repos/<właściciel>/<akcja>/commits/<nowy-tag> --jq .sha
```

i wpisać SHA z komentarzem `# <nowy-tag>`. Przy akcji złożonej sprawdzić w jej `action.yml`, czy wewnętrzne `uses:` też
są przypięte do SHA.

## Pułapki i ograniczenia

> [!warning]
>
> - Bez sekretu GPG krok importu kończy wydanie błędem — nic niepodpisanego nie trafia na Pages.
> - Klucz z sekretu musi być tym z `flatpak/ws-tracker-repo.gpg` — [publikuj.sh](../../flatpak/publikuj.sh) inaczej
>   przerywa (podpis innym kluczem zepsułby instalacje i aktualizacje u wszystkich).
> - Środowisko `github-pages` musi dopuszczać tagi `v*` ([github-pages](github-pages.md)).
> - Tag niezgodny z wersją w `pyproject.toml` zatrzymuje wydanie przed budową.
> - `repo-dir` i `state-dir` akcji muszą być na tej samej partycji (README akcji).
> - Kontener wymaga `--privileged` (bubblewrap w flatpak-builder).
> - Workflowy sprawdzamy lokalnie [actionlint](https://github.com/rhysd/actionlint) (`docker run rhysd/actionlint`).

## Gdzie w kodzie

- [.github/workflows/testy.yml](../../.github/workflows/testy.yml)
- [.github/workflows/wydanie.yml](../../.github/workflows/wydanie.yml)
- [flatpak/publikuj.sh](../../flatpak/publikuj.sh)

## Dokumentacja

- [Workflow syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions)
- [flatpak-github-actions](https://github.com/flatpak/flatpak-github-actions)
- [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions)

## Powiązane

- [GitHub Pages](github-pages.md), [Flatpak](flatpak.md)
- [ADR-0007](../decyzje/0007-dystrybucja-repozytorium-flatpak-na-github-pages.md)
- Zadanie [0051](../../TODO/ZROBIONE/0051-plan4-github-actions/todo.md)
