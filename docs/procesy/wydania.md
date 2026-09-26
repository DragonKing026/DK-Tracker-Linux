---
noteId: "947ac69bba214ddcada484a736d2c8fd"
tytul: Wydania i instalacja
tags: [proces, wydanie, flatpak]
utworzono: 2026-09-26 11:58
zaktualizowano: 2026-09-26 11:58
---

# Wydania i instalacja

Jak wydać nową wersję WS Tracker Tray i jak ją zainstalować. Decyzja o dystrybucji:
[ADR-0007](../decyzje/0007-dystrybucja-repozytorium-flatpak-na-github-pages.md); workflow:
[wydanie.yml](../../.github/workflows/wydanie.yml) ([GitHub Actions](../integracje/github-actions.md)).

## Jednorazowo: klucz i Pages

1. `flatpak/klucz-gpg.sh` ([skrypt](../../flatpak/klucz-gpg.sh)) — klucz publiczny trafia do
   `flatpak/ws-tracker-tray-repo.gpg` (commit), prywatny do `~/ws-tracker-tray-repo-private.asc`.
2. Sekret i sprzątnięcie klucza prywatnego:

   ```bash
   gh secret set FLATPAK_GPG_PRIVATE_KEY < ~/ws-tracker-tray-repo-private.asc
   shred -u ~/ws-tracker-tray-repo-private.asc
   ```

3. GitHub → **Settings → Pages → Source: GitHub Actions** ([GitHub Pages](../integracje/github-pages.md)).

> [!warning] Klucz prywatny
> Klucz prywatny istnieje tylko w sekrecie GitHuba — nigdy w repozytorium ani w logach. Jego utrata oznacza nowy klucz
> i ponowną instalację z nowego `.flatpakref` u wszystkich.

## Każde wydanie

1. Wersja w [pyproject.toml](../../pyproject.toml) i [`__init__.py`](../../src/ws_tracker_tray/__init__.py).
2. Nowy `<release version="…" date="…">` na **początku** `<releases>` w
   [MetaInfo](../../data/pl.websystems.WsTrackerTray.metainfo.xml) — lista zmian po angielsku (Discover ją pokazuje);
   po polsku opisuje ją commit.
3. `.venv/bin/pytest` — test spójności wersji ([test_pakiet.py](../../tests/test_pakiet.py)) i reszta.
4. Commit, potem tag i wypchnięcie (**tylko za zgodą właściciela repozytorium**):

   ```bash
   git tag v<wersja>
   git push origin main v<wersja>
   gh run watch                      # testy i wydanie
   ```

5. Sprawdzenie: wydanie na GitHubie z plikiem `pl.websystems.WsTrackerTray-v<wersja>.flatpak`, strona
   <https://dragonking026.github.io/Kimai-App--Linux-/>, `flatpak update` u siebie.

Wersje `0.x` wychodzą jako „pre-release”. **1.0.0** — po testach na GNOME
([0020](../../TODO/DO-ZROBIENIA/0020-testy-gnome/todo.md)).

```mermaid
flowchart LR
    V[wersja + MetaInfo] --> T[pytest] --> C[commit] --> G[tag v…] --> P[push za zgodą]
    P --> A[wydanie.yml] --> R[wydanie + Pages] --> U[flatpak update u ludzi]
```

## Instalacja dla ludzi

Zalecana — z repozytorium, aktualizacje przyjdą same (Discover, GNOME Software, `flatpak update`):

```bash
flatpak install --user https://dragonking026.github.io/Kimai-App--Linux-/pl.websystems.WsTrackerTray.flatpakref
```

Plik `.flatpak` z [najnowszego wydania](https://github.com/DragonKing026/Kimai-App--Linux-/releases/latest) — tylko bez
dostępu do strony repozytorium; **nie dostaje aktualizacji**. Przejście z pliku na repozytorium:

```bash
flatpak uninstall --user pl.websystems.WsTrackerTray    # ustawienia w ~/.var/app zostają
flatpak install --user https://dragonking026.github.io/Kimai-App--Linux-/pl.websystems.WsTrackerTray.flatpakref
```

## Wersja deweloperska a Flatpak

[instaluj-dev.sh](../../scripts/instaluj-dev.sh) kładzie w `~/.local/share` plik `.desktop` i ikonę o tym samym
identyfikatorze co Flatpak, więc przesłania paczkę w menu i w powiadomieniach. Przed instalacją paczki:

```bash
scripts/instaluj-dev.sh --usun
```

## Powiązane

- [Flatpak](../integracje/flatpak.md), [budowa lokalna](../../flatpak/buduj.sh)
- [Plan 4](../plany/2026-09-26-plan-4-flatpak.md)
