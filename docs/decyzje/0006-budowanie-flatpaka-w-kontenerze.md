---
noteId: "3bd3283622dc40c6a65245ebdffb83b2"
tytul: Budowanie Flatpaka w kontenerze
tags: [adr, flatpak, build, docker]
status: zaakceptowana
zastapiona_przez:
utworzono: 2026-09-25 20:37
zaktualizowano: 2026-09-26 11:49
---

# ADR-0006: Paczkę Flatpak budujemy w kontenerze, nie na hoście

Uzupełnia [ADR-0002](0002-stos-python-pyside6.md) (stos i baza `io.qt.PySide.BaseApp`).

## Kontekst

Na Fedorze 44 jest Flatpak **1.18.2** z regresją: `flatpak build-init --base` kończy się
`lsetxattr(security.selinux): Operation not supported` na systemach z SELinux
([flatpak#6818](https://github.com/flatpak/flatpak/issues/6818); poprawka w 1.18.3,
[PR #6834](https://github.com/flatpak/flatpak/pull/6834)). 1.18.3 nie ma w Fedorze 44
(Bodhi, stan 2026-09-25 20:37). Manifest z `base: io.qt.PySide.BaseApp` nie zbuduje się więc na
stacji deweloperskiej. Regresja dotyczy **tylko budowania** — gotowa paczka instaluje się
i działa na 1.18.2 (sprawdzone).

## Rozważane opcje

| Opcja | Zalety | Wady |
| --- | --- | --- |
| Czekać na 1.18.3 w Fedorze | nic nie robimy | termin nieznany |
| Cofnąć Flatpak hosta do 1.17.7 | budowa lokalna | `sudo`, zmiana systemu użytkownika |
| PySide6 z paczek pip zamiast bazy | działa na hoście | 236 MB zamiast 70 MB, własne Qt; **uniemożliwia `layer-shell-qt`** ([ADR-0005](0005-okno-przy-tacce-na-kde.md)) |
| **Budowa w kontenerze** (Debian trixie, Flatpak 1.16) | działa dziś, bez zmian w systemie; te same runtime'y; niezależna od wersji Flatpaka hosta; ta sama droga nadaje się do CI | Docker z `--privileged` (bubblewrap); pierwsze uruchomienie kopiuje runtime'y (kilka GB w `~/.cache`) |

## Decyzja

**Paczkę Flatpak budujemy w kontenerze** (obecnie `debian:trixie`, Flatpak 1.16.x) z bazą
`io.qt.PySide.BaseApp`. Lokalnie: skrypt budujący (prototyp:
[buduj-w-dockerze.sh](../../TODO/ZROBIONE/0004-prototyp-tacki-i-okna/prototyp/flatpak/buduj-w-dockerze.sh)), który
montuje
runtime'y hosta tylko do odczytu. Docelowo (Plan 4): ten sam obraz albo obraz CI Flathuba.

Zaakceptowane przez użytkownika 2026-09-25 20:37.

## Aktualizacja (2026-09-26 11:49)

Obraz `debian:trixie` z prototypu zastąpił obraz CI Flathuba
`ghcr.io/flathub-infra/flatpak-github-actions:kde-6.11`: Flatpak 1.18.1 (bez regresji flatpak#6818), SDK KDE 6.11,
`appstreamcli` i `flatpak-builder-lint`. Ten sam obraz buduje paczkę lokalnie ([buduj.sh](../../flatpak/buduj.sh)) i w
GitHub Actions; na Fedorze 44 z SELinux zbudował aplikację z bazą PySide
([próba budowy](../../TODO/ZROBIONE/0045-plan4-projekt-flatpak/notatki/proba-budowy.md)). Runtime'y hosta nie są już
montowane — obraz pobiera je sam, a cache leży w `~/.cache/ws-tracker-tray-flatpak`.

## Konsekwencje

- Wynik budowy: plik `.flatpak`, instalowany na hoście `flatpak install --user --bundle`.
- Skrypt jest w repozytorium: [flatpak/buduj.sh](../../flatpak/buduj.sh) (Plan 4).
- Gdy Fedora dostanie Flatpak 1.18.3, budowa na hoście znów będzie możliwa — kontener
  zostaje jako droga powtarzalna (CI).
- Narzędzie agenta (Claude Code) uruchamia budowę poza swoją piaskownicą (Docker, `~/.local/share/flatpak`).

## Powiązane

- [Flatpak](../integracje/flatpak.md), [ADR-0002](0002-stos-python-pyside6.md),
  [ADR-0005](0005-okno-przy-tacce-na-kde.md)
- [Prototyp 0004 — ustalenia](../../TODO/ZROBIONE/0004-prototyp-tacki-i-okna/notatki/ustalenia.md)
