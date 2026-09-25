---
noteId: "05566ff2ce6741389c097298fd129518"
tytul: WS Tracker (projekt referencyjny)
tags: [integracja, referencja, kimai]
status_integracji: referencja
wersja: 1.5.1
utworzono: 2026-09-25 17:19
zaktualizowano: 2026-09-25 18:06
---

# WS Tracker — wtyczka przeglądarkowa (projekt referencyjny)

> [!info] W skrócie
> Wtyczka Chrome/Edge/Brave/Firefox (Manifest V3) od Web Systems do mierzenia czasu
> w Kimai. **Nie jest zależnością** tej aplikacji — to wzorzec funkcji i zachowania,
> który odtwarzamy natywnie w tacce systemowej.

- Repozytorium: [github.com/websystemspl/kimai-ws-tracker](https://github.com/websystemspl/kimai-ws-tracker)
  (`git@github.com:websystemspl/kimai-ws-tracker.git`)
- Chrome Web Store: [Kimai — pomiar czasu (Web Systems)](https://chromewebstore.google.com/detail/kimai-pomiar-czasu-web-sy/eliiemekophpilppaobljfjkhbkmchjg)
- Licencja: MIT (napisana od zera — nie jest forkiem „Time Tracker Addon for Kimai”,
  którego licencja zabrania modyfikacji).
- Przeanalizowana wersja: **1.5.1**.

## Wygląd (wzorzec UI)

Zrzuty wykonane z kopii wtyczki z podstawioną atrapą API (dane fikcyjne).

| Bezczynny | Trwa |
|---|---|
| ![popup-bezczynny](../assets/referencja/popup-bezczynny.png) | ![popup-trwa](../assets/referencja/popup-trwa.png) |

| Błąd walidacji opisu | Ustawienia |
|---|---|
| ![popup-blad-opisu](../assets/referencja/popup-blad-opisu.png) | ![ustawienia](../assets/referencja/ustawienia.png) |

Elementy okna (od góry): nagłówek „WS Tracker · Kimai” z sumą dnia i tygodnia oraz
zębatką ustawień → pole opisu z zegarem i okrągłym przyciskiem start (zielony ▶) / stop
(czerwony ■) → wybór projektu z kolorową kropką (grupy po klientach) → wybór czynności
i przełącznik `$` → (tylko gdy trwa) pola „Od / Do” → pasek komunikatu → „Ostatnie
wpisy” z nagłówkami dni i sumami → link „Wszystkie moje wpisy w Kimai”.

## Struktura kodu wtyczki

```
manifest.json         MV3: uprawnienia storage + alarms, opcjonalne https://*/*
background.js         service worker: badge z czasem co 1 min (chrome.alarms)
lib/api.js            klient Kimai REST API (Bearer), obsługa błędów, localStamp
lib/i18n.js           własne ładowanie tłumaczeń z wyborem języka
lib/validate.js       walidacja jakości opisu (lista ogólników PL/EN)
popup/                okno (HTML/CSS/JS, ~1450 linii)
options/              ustawienia: URL, token, język, min. długość opisu
_locales/pl, /en      teksty
```

## Co przenosimy, a co zmieniamy

| Element wtyczki | W aplikacji |
|---|---|
| `lib/api.js` | Przenosimy logikę 1:1 (endpointy, obsługa 400 „extra fields”, `localStamp`, stronicowanie `range`). [Kimai API](kimai-api.md) |
| `lib/validate.js` | Przenosimy 1:1 łącznie z listą ogólników — dobry kandydat na testy jednostkowe. |
| `_locales/*/messages.json` | Teksty i klucze jako punkt wyjścia tłumaczeń aplikacji. |
| `background.js` badge | Ikona w tacce + tooltip. [SNI](statusnotifieritem.md) |
| `popup/` | Okno aplikacji (forma zależna od ADR o Waylandzie). |
| `chrome.storage.sync` token | Magazyn sekretów systemu. [Secret Service](secret-service.md) |
| `chrome.storage.local` (lastProject, billableAllowed, kimaiLocale) | Plik stanu w katalogu XDG aplikacji. |
| `optional_host_permissions` | Niepotrzebne — Flatpak: `--share=network`. |

> [!bug] Drobny błąd zauważony przy zrzutach
> W stanie bezczynnym z przywróconym ostatnim projektem kropka koloru projektu bywa szara:
> `enterIdleState()` wywołuje `paintProjectDot()` bez koloru już po tym, jak
> `fillPickers()` go ustawiło. W aplikacji — nie powielać.

> [!bug] Strefa czasowa (potwierdzone na Kimai 2.67 w Dockerze)
> `localStamp()` wysyła czas **przeglądarki**, a Kimai dokleja do niego strefę **konta
> Kimai** bez przeliczania. Gdy strefy się różnią (np. konto w UTC, system Europe/Warsaw),
> wpis zaczyna się 2 h w przyszłości, a stop i kolejny start są odrzucane.
> [Raport](../../TODO/W-TRAKCIE/0002-specyfikacja-projektu/testy/raport-kimai-docker-2026-09-25.md).
> W aplikacji czas liczymy w strefie z `/api/users/me → timezone`.

## Pełny opis zachowań

[Katalog funkcji F-01…F-14](../architektura/funkcje.md) — każda funkcja wtyczki
rozpisana z endpointami i przypadkami brzegowymi.

## Powiązane

- [Kimai REST API](kimai-api.md)
- [Przegląd projektu](../architektura/przeglad.md)
