---
noteId: "bf2d2fabf984496cbc731b1f3c66b604"
tytul: GitHub Actions
tags: [integracja, ci, wydanie, github, bezpieczenstwo]
status_integracji: w-uzyciu
wersja: "akcje: checkout@v4 i v7, setup-python@v5, flatpak-builder@v6, ghaction-import-gpg@v6, upload-pages-artifact@v3, deploy-pages@v4, action-gh-release@v2"
utworzono: 2026-09-26 11:57
zaktualizowano: 2026-10-31 13:10
---

# GitHub Actions

> [!info] W skrócie
> CI repozytorium na GitHubie: testy przy każdym pushu na `main` i pull requeście, a po tagu `v<wersja>` —
> podpisana paczka Flatpak, repozytorium Flatpaka na [GitHub Pages](github-pages.md) i wydanie z plikiem `.flatpak`.
> Do tego audyty bezpieczeństwa: CodeQL, gitleaks, zizmor i OpenSSF Scorecard ([niżej](#audyty-bezpieczeństwa)).

## Do czego używamy

| Workflow | Kiedy | Co robi |
| --- | --- | --- |
| [testy.yml](../../.github/workflows/testy.yml) | push na `main`, pull request | instalacja z sumami, `ruff format --check`, `ruff check`, `pytest` (Qt offscreen), 30 s fuzzingu Atheris, linki, frontmatter, markdownlint |
| [wydanie.yml](../../.github/workflows/wydanie.yml) | tag `v*` | testy (`testy.yml` jako `workflow_call`), zgodność tagu z `pyproject.toml`, walidacja MetaInfo, klucz GPG, budowa i podpis, Pages, poświadczenie pochodzenia paczki, na końcu wydanie |
| [strona.yml](../../.github/workflows/strona.yml) | ręcznie; push na `main` zmieniający stronę | kopia opublikowanego repozytorium Flatpaka (weryfikacja kluczem), ponowny podpis, nowa strona na Pages — bez wydania ([GitHub Pages](github-pages.md)) |
| [codeql.yml](../../.github/workflows/codeql.yml) | każdy push, pull request, co tydzień | analiza statyczna kodu Pythona (CodeQL), wyniki w Security → Code scanning |
| [security.yml](../../.github/workflows/security.yml) | każdy push, pull request, co tydzień | gitleaks (sekrety w całej historii) i zizmor (audyt workflowów) |
| [scorecard.yml](../../.github/workflows/scorecard.yml) | push na `main`, zmiana reguł gałęzi, co tydzień | ocena OpenSSF Scorecard, publikowana na scorecard.dev |

## Audyty bezpieczeństwa

Zestaw jak w repozytorium commit-sentry. Nowe workflowy mają `permissions: contents: read` na górze (Scorecard:
`read-all`, jak wymaga akcja),
szersze uprawnienia (`security-events: write`, `id-token: write`) tylko w zadaniu, które ich potrzebuje,
`persist-credentials: false` w checkoucie i `timeout-minutes`.

- **CodeQL** — język `python`, `build-mode: none` (Python nie wymaga budowy). Kod QML i skrypty powłoki poza zakresem.
- **gitleaks 8.30.1** — pobierany z wydania z weryfikacją sumy SHA-256 (suma z `gitleaks_8.30.1_checksums.txt`),
  skanuje całą historię (`fetch-depth: 0`). Fałszywy alarm: `Fingerprint` w `.gitleaksignore`, nie wyłączanie kroku.
- **zizmor 1.30.1** — `pipx run zizmor==1.30.1 --offline --min-severity low .github/workflows`; to samo uruchomisz
  lokalnie. Wyjątek zizmor tylko komentarzem `# zizmor: ignore[<reguła>]` z uzasadnieniem (np. `self-repository`
  w `wydanie.yml`: forma `./` jest sprawdzana testem pakietu).
- **Scorecard** — wynik i odznaka na
  [scorecard.dev](https://scorecard.dev/viewer/?uri=github.com/DragonKing026/DK-Tracker-Linux);
  publikacja wyniku wymaga publicznego repozytorium.
- **Dependabot** ([dependabot.yml](../../.github/dependabot.yml)) — co tydzień po jednym pull requeście: z przypiętymi
  akcjami i z zależnościami CI w `requirements-ci.txt` (`cooldown` 7 dni). Flatpak instaluje zależności offline
  z przypiętych źródeł w `flatpak/python3-deps.yaml`, których Dependabot nie zaktualizuje.
- **Zależności CI z sumami** — [testy.yml](../../.github/workflows/testy.yml) instaluje
  `pip install --require-hashes -r requirements-ci.txt`, potem sam projekt `pip install --no-deps
  --no-build-isolation -e .` (Scorecard, Pinned-Dependencies, uznaje tylko instalację z sumami; zakresy z
  `pyproject.toml` nie wystarczą). Plik jest generowany z [pyproject.toml](../../pyproject.toml) (extras `dev`, `ui`)
  i [requirements-ci.in](../../requirements-ci.in) (`setuptools`, `atheris`) dla Pythona 3.13 na Linuxie x86-64:

  ```bash
  uv pip compile pyproject.toml requirements-ci.in --extra dev --extra ui --generate-hashes \
    --python-version 3.13 --python-platform x86_64-manylinux_2_39 -o requirements-ci.txt
  ```

  Zmiana przedziału w `pyproject.toml` wymaga ponownego wygenerowania pliku.
- **Fuzzing** — [fuzz/fuzz_core.py](../../fuzz/fuzz_core.py) (Atheris/libFuzzer) wywołuje czyste funkcje rdzenia
  (czas, opis wpisu, sortowanie) na losowych bajtach; `testy.yml` uruchamia go na 30 s. Lokalnie:
  `python fuzz/fuzz_core.py -max_total_time=60` (Linux x86-64, `atheris` z `requirements-ci.txt`). Scorecard
  (Fuzzing) dla Pythona rozpoznaje tylko `import atheris`. Obok są testy właściwości Hypothesis
  ([test_properties.py](../../tests/core/test_properties.py)), uruchamiane z resztą `pytest`.
- **Podpisane wydania** — zadanie `poswiadczenie` w `wydanie.yml` tworzy poświadczenie pochodzenia paczki
  (`actions/attest-build-provenance`, Sigstore) i dołącza je do wydania jako
  `<paczka>.flatpak.sigstore.json` — tej nazwy szuka Scorecard (Signed-Releases; `.sigstore.json` daje 8/10,
  10/10 tylko przy `.intoto.jsonl` z `slsa-github-generator`, którego nie da się przypiąć do SHA, a repozytorium
  tego wymaga). Zadanie ma `id-token: write` i `attestations: write`, nie ma klucza GPG. Wynik w Scorecard rośnie
  dopiero po następnym wydaniu (liczy ostatnie pięć).
- **Zgłaszanie podatności** — [SECURITY.md](../../.github/SECURITY.md): prywatne zgłoszenia GitHuba, wspierane tylko
  najnowsze wydanie.

> [!warning]
>
> - Ustawienie repozytorium zezwala tylko na akcje GitHuba i wymienione wyjątki (patrz „Przypięte akcje”).
>   `ossf/scorecard-action` nie jest akcją GitHuba — **trzeba ją dopisać do dozwolonych** w Settings → Actions →
>   General, inaczej `scorecard.yml` nie ruszy. `github/codeql-action` jest akcją GitHuba.
> - Pull requesty Dependabota zmieniają przypięcia akcji także w `wydanie.yml` i `strona.yml` (zadania z kluczem
>   GPG): przeglądaj je jak zmianę kodu, nie scalaj na ślepo.

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

Zadanie `flatpak` działa w kontenerze `ghcr.io/flathub-infra/flatpak-github-actions:kde-6.11@sha256:b0a8a2ac…` z `--privileged` — tym
samym obrazem co lokalna budowa ([buduj.sh](../../flatpak/buduj.sh),
[ADR-0006](../decyzje/0006-budowanie-flatpaka-w-kontenerze.md));
spójność pilnuje test `test_release_builds_in_the_same_container_as_the_local_script`
([test_pakiet.py](../../tests/test_pakiet.py)).

Obraz jest przypięty do digestu indeksu (tag zostaje dla czytelności) w trzech miejscach naraz: `wydanie.yml`,
`strona.yml` i `buduj.sh` (Scorecard, Pinned-Dependencies; test `test_release_builds_in_the_same_container_as_the_local_script`
pilnuje zgodności). **Dependabot go nie podbije** — ekosystem `docker` czyta tylko Dockerfile, compose i manifesty
Kubernetesa, nie `container:` w workflowach ani skrypt powłoki. Aktualizacja ręczna: sprawdzić nowy obraz, potem

```bash
skopeo inspect --raw docker://ghcr.io/flathub-infra/flatpak-github-actions:kde-6.11 | sha256sum
```

(digest indeksu wieloarchitekturowego) i wpisać wynik w trzech miejscach; zbudować lokalnie `flatpak/buduj.sh`.
Digest z 2026-10-31: tag `kde-6.11`, indeks OCI, pobrany z ghcr.io przez `skopeo`.

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
  `contents: write` — zadanie `wydanie`. Zadanie z kluczem GPG nie ma uprawnień zapisu. Tak samo `strona.yml`:
  zapis Pages tylko w zadaniu `pages`.
- `poswiadczenie` w `wydanie.yml`: `contents: read`, `id-token: write`, `attestations: write` (akcja GitHuba, więc
  mieści się w dozwolonych akcjach repozytorium).
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
| actions/checkout (codeql, security, scorecard) | v7.0.1 | `3d3c42e5aac5ba805825da76410c181273ba90b1` |
| github/codeql-action (init, analyze, upload-sarif) | v4.38.3 | `24c54180a607b1449ed407dd24f251e4e9147c8d` |
| ossf/scorecard-action | v2.5.0 | `fa7117db83c52d787ae5a89f350999701505d78e` |
| actions/setup-python | v5.6.0 | `a26af69be951a213d495a4c3e4e4022e16d87065` |
| actions/upload-pages-artifact | v4.0.0 | `7b1f4a764d45c48632c6b24a0339c27f5614fb0b` |
| actions/deploy-pages | v4.0.5 | `d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e` |
| actions/upload-artifact | v4.6.2 | `ea165f8d65b6e75b540449e92b4886f43607fa02` |
| actions/download-artifact | v4.3.0 | `d3f86a106a0bac45b974a628896c90dbdf5c8093` |
| actions/attest-build-provenance | v4.2.2 | `4d101475d8b20a2381f78447822ac1eab6504dd8` |
| crazy-max/ghaction-import-gpg | v6.3.0 | `e89d40939c28e39f97cf32126055eeae86ba74ec` |
| flatpak/flatpak-github-actions/flatpak-builder | v6.8 | `79327416609af08178ad73b352877e51450790b3` |
| softprops/action-gh-release | v2.6.2 | `3bb12739c298aeb8a4eeaf626c5b8d85266b0e65` |

Aktualizacje proponuje Dependabot (co tydzień jeden pull request). Ręcznie: przejrzeć zmiany między wersjami w
repozytorium akcji, potem

```bash
gh api repos/<właściciel>/<akcja>/commits/<nowy-tag> --jq .sha
```

i wpisać SHA z komentarzem `# <nowy-tag>`. Przy akcji złożonej sprawdzić w jej `action.yml`, czy wewnętrzne `uses:` też
są przypięte do SHA.

## Pułapki i ograniczenia

> [!warning]
>
> - Bez sekretu GPG krok importu kończy wydanie błędem — nic niepodpisanego nie trafia na Pages.
> - Klucz z sekretu musi być tym z `flatpak/dk-tracker-repo.gpg` — [publikuj.sh](../../flatpak/publikuj.sh) inaczej
>   przerywa (podpis innym kluczem zepsułby instalacje i aktualizacje u wszystkich).
> - Środowisko `github-pages` musi dopuszczać tagi `v*` ([github-pages](github-pages.md)).
> - Tag niezgodny z wersją w `pyproject.toml` zatrzymuje wydanie przed budową.
> - `repo-dir` i `state-dir` akcji muszą być na tej samej partycji (README akcji).
> - Kontener wymaga `--privileged` (bubblewrap w flatpak-builder).
> - Workflowy sprawdzamy lokalnie [actionlint](https://github.com/rhysd/actionlint) (`docker run rhysd/actionlint`
  albo `actionlint`) i `zizmor --offline --min-severity low .github/workflows`.

## Gdzie w kodzie

- [.github/workflows/testy.yml](../../.github/workflows/testy.yml)
- [.github/workflows/wydanie.yml](../../.github/workflows/wydanie.yml)
- [.github/workflows/codeql.yml](../../.github/workflows/codeql.yml),
  [security.yml](../../.github/workflows/security.yml), [scorecard.yml](../../.github/workflows/scorecard.yml)
- [.github/dependabot.yml](../../.github/dependabot.yml), [.github/SECURITY.md](../../.github/SECURITY.md)
- [requirements-ci.in](../../requirements-ci.in), [fuzz/fuzz_core.py](../../fuzz/fuzz_core.py)
- [flatpak/publikuj.sh](../../flatpak/publikuj.sh)

## Dokumentacja

- [Workflow syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions)
- [flatpak-github-actions](https://github.com/flatpak/flatpak-github-actions)
- [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions)

## Powiązane

- [GitHub Pages](github-pages.md), [Flatpak](flatpak.md)
- [ADR-0007](../decyzje/0007-dystrybucja-repozytorium-flatpak-na-github-pages.md)
- Zadanie [0051](../../TODO/ZROBIONE/0051-plan4-github-actions/todo.md)
- Zadanie [0083](../../TODO/ZROBIONE/0083-ci-z-audytami-bezpieczenstwa/todo.md) — audyty bezpieczeństwa
- Zadanie [0084](../../TODO/W-TRAKCIE/0084-scorecard-pinned-signed-fuzzing/todo.md) — sumy, poświadczenia, fuzzing
