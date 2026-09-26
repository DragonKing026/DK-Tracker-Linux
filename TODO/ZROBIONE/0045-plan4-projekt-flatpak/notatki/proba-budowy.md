---
noteId: "b6c2aa090e5f4873b126b572b8972e7d"
tytul: "Próba budowy Flatpaka przed Planem 4"
tags: [todo, plan-4, flatpak, notatki]
utworzono: 2026-09-26 11:01
zaktualizowano: 2026-09-26 11:01
---

# Próba budowy Flatpaka przed Planem 4

Zadanie: [0045](../todo.md). Pliki próby: [manifest](../prototyp/pl.websystems.KimaiTray.yml),
[zależności Pythona](../prototyp/python3-deps.yaml), [MetaInfo](../prototyp/pl.websystems.KimaiTray.metainfo.xml).

## Środowisko budowy

- Obraz `ghcr.io/flathub-infra/flatpak-github-actions:kde-6.11` (ten sam co w GitHub Actions): Freedesktop SDK 25.08,
  **Flatpak 1.18.1**, flatpak-builder 1.4.9, `org.kde.Platform`/`Sdk` 6.11, `appstreamcli`, `flatpak-builder-lint`.
- Zbudował z bazą `io.qt.PySide.BaseApp` na Fedorze 44 z SELinux (`docker run --privileged`) — regresja flatpak#6818
  (1.18.2) go nie dotyczy. Zastępuje obraz Debiana z prototypu
  ([ADR-0006](../../../../docs/decyzje/0006-budowanie-flatpaka-w-kontenerze.md)).
- Baza PySide: Python 3.13.15, PySide6 6.11.2; **brak** `httpx` i `jeepney` — moduły z `flatpak-pip-generator`
  (`--runtime org.kde.Sdk//6.11`): httpx 0.28.1, anyio, certifi, h11, httpcore, idna, typing_extensions, jeepney 0.9.0 —
  same koła `py3-none-any`.
- `pip3 install --no-build-isolation` naszego pakietu działa w SDK (setuptools jest).

## Wynik

- Paczka `.flatpak`: **71 MB**, `appstreamcli compose` bez błędów, `appstreamcli validate`: OK, `desktop-file-validate`:
  OK.
- `flatpak-builder-lint`: tylko `appid-url-not-reachable` (certyfikat websystems.pl wygasł) i brak zrzutu ekranu pod
  adresem GitHuba (nic jeszcze nie wypchnięte) — wymagania Flathuba, nie naszego repozytorium na Pages.

## Test na żywo z użytkownikiem (2026-09-26 11:01)

Najpierw usunięta wersja deweloperska (`scripts/instaluj-dev.sh --usun` — jej `.desktop` w `~/.local/share/applications`
przesłaniałby wpis Flatpaka o tym samym identyfikatorze), potem `flatpak install --user --bundle`.

| Punkt | Wynik |
| --- | --- |
| Menu programów z logo, ikona w tacce | tak |
| Token w KWallet (Secret Service z piaskownicy) | działa; ksecretd nie pyta o zgodę dla aplikacji |
| Okno przy tacce (layer-shell w piaskownicy) | tak (`window: layer` w logu) |
| Powiadomienia „Kimai Tray” (start/stop z menu) | tak |
| Autostart (portal Background) | działa bez pytania — Plasma utworzyła `~/.config/autostart/pl.websystems.KimaiTray.desktop` z `kimai-tray --hidden` |
