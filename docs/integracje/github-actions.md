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

## Pułapki i ograniczenia

> [!warning]
>
> - Bez sekretu GPG krok importu kończy wydanie błędem — nic niepodpisanego nie trafia na Pages.
> - Klucz z sekretu musi być tym z `flatpak/ws-tracker-tray-repo.gpg` — [publikuj.sh](../../flatpak/publikuj.sh) inaczej
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
