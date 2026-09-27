---
noteId: "42180eacf59745ab803a4dcb034f23b0"
tytul: GitHub Pages
tags: [integracja, wydanie, flatpak, github]
status_integracji: w-uzyciu
wersja: "źródło: GitHub Actions"
utworzono: 2026-09-26 11:57
zaktualizowano: 2026-09-27 12:40
---

# GitHub Pages

> [!info] W skrócie
> Darmowy hosting statyczny GitHuba. Trzyma nasze podpisane repozytorium Flatpaka, z którego Discover, GNOME Software
> i `flatpak update` pobierają aktualizacje.

## Do czego używamy

Adres: **<https://dragonking026.github.io/DK-Tracker-Linux>** (repozytorium kodu jest publiczne, konto darmowe).
Stronę publikuje workflow [wydanie.yml](../../.github/workflows/wydanie.yml) po tagu wersji, a samą stronę projektu —
bez wydania — workflow [strona.yml](../../.github/workflows/strona.yml) ([GitHub Actions](github-actions.md)).

| Ścieżka na stronie | Zawartość |
| --- | --- |
| `repo/` | repozytorium OSTree (aplikacja, `.Locale`, `.Debug`, appstream), podpisane GPG, z deltami statycznymi |
| `dk-tracker.flatpakrepo` | dodaje źródło aktualizacji (`flatpak remote-add`) |
| `io.github.dragonking026.DK-Tracker-Linux.flatpakref` | instaluje aplikację jedną komendą; źródło dodaje się samo |
| `index.html`, `strona.css`, `strona.js` | strona projektu (PL/EN, jasny i ciemny motyw), szablon: `flatpak/strona/` |
| `dk-tracker.svg`, `okno-ciemny-motyw.png` | ikona i zrzut okna na stronie (z `data/icons/` i `docs/assets/zrzuty/`) |

Format plików `.flatpakrepo` i `.flatpakref`:
[flatpak command reference](https://docs.flatpak.org/en/latest/flatpak-command-reference.html); hosting repozytorium:
[Hosting a repository](https://docs.flatpak.org/en/latest/hosting-a-repository.html). Pliki pisze
[pages.py](../../flatpak/pages.py), całość składa [publikuj.sh](../../flatpak/publikuj.sh).

## Strona projektu

Szablon [flatpak/strona/](../../flatpak/strona/index.html): statyczny HTML, CSS i JS bez niczego z innych serwerów
(czcionki systemowe, zero skryptów zewnętrznych — [brak telemetrii](../../AGENTS.md)). Obie wersje językowe są
w jednym pliku; język wybiera przeglądarka (`navigator.language`), przełącznik PL/EN i motywu zapamiętuje wybór
w `localStorage`. [pages.py](../../flatpak/pages.py) wstawia adres, wersję i datę najnowszego `<release>` z pliku
MetaInfo i kopiuje zasoby. Zmianę strony oglądamy lokalnie:

```bash
python3 flatpak/pages.py /tmp/strona https://dragonking026.github.io/DK-Tracker-Linux flatpak/dk-tracker-repo.gpg
python3 -m http.server -d /tmp/strona 8765   # http://127.0.0.1:8765
```

**Publikacja bez wydania** — [strona.yml](../../.github/workflows/strona.yml), ręcznie (Actions → Strona → Run
workflow) i sama po pushu na `main` zmieniającym stronę. Pages to jedno wdrożenie (strona **i** `repo/`), więc
workflow:

1. kopiuje opublikowane repozytorium: `ostree pull --mirror` z weryfikacją podpisów kluczem
   `flatpak/dk-tracker-repo.gpg` — repozytorium podpisane innym kluczem zatrzymuje publikację;
2. podpisuje je ponownie tym samym kluczem i składa stronę ([publikuj.sh](../../flatpak/publikuj.sh)) — commity
   aplikacji się nie zmieniają, więc `flatpak update` u ludzi nie widzi „nowej wersji”;
3. bierze MetaInfo z najnowszego tagu `v*`, żeby strona nie pokazała wersji jeszcze niewydanej.

Próba na prawdziwym repozytorium (2026-09-27 12:40, klucz testowy): kopia 333 MB w ok. 3 min, po ponownym podpisie
`flatpak remote-info` pokazuje ten sam commit aplikacji co przed kopią.

## Jak to działa

```mermaid
flowchart LR
    U[użytkownik] -- flatpak install .flatpakref --> P[GitHub Pages]
    P --> R[(repo/ OSTree)]
    R -- podpis GPG sprawdzany kluczem z .flatpakref --> F[flatpak u użytkownika]
    F -- runtime KDE, baza PySide --> FH[Flathub]
```

Klucz publiczny `flatpak/dk-tracker-repo.gpg` (tworzy go [klucz-gpg.sh](../../flatpak/klucz-gpg.sh) przy pierwszym
wydaniu) jest wpisany w oba pliki jako `GPGKey`, więc `flatpak` sprawdza każdy commit i podsumowanie repozytorium.
Runtime KDE i baza PySide
przychodzą z Flathuba (`RuntimeRepo`).

## Konfiguracja / uprawnienia

- Ustawienia repozytorium → **Pages → Source: GitHub Actions**
  ([Configuring a publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)).
- Workflow: `pages: write`, `id-token: write` (tylko zadanie `pages`), środowisko `github-pages`.
- Środowisko `github-pages` musi dopuszczać tagi `v*` — domyślnie publikuje tylko gałąź domyślna, a wydanie idzie z
  tagu (komendy: [wydania](../procesy/wydania.md),
  [deployment branch policies](https://docs.github.com/en/rest/deployments/branch-policies)).

## Pułapki i ograniczenia

> [!warning]
>
> - Limity
>   ([GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)):
>   strona do **1 GB**, miękki limit transferu **100 GB/miesiąc**, publikacja do 10 minut. Paczka ma ok. 70 MB, więc
>   starczy na wiele wersji; `--prune` w `publikuj.sh` usuwa stare obiekty.
> - Każde wydanie publikuje stronę od nowa z repozytorium z tej budowy — wcześniejsze wersje nie zostają w `repo/`.
> - `wydanie.yml` i `strona.yml` dzielą grupę `concurrency: pages` — nie publikują naraz. GitHub trzyma w kolejce
>   tylko **jedno** oczekujące uruchomienie grupy: nie uruchamiaj strony w trakcie wydania, bo oczekujące wydanie
>   mogłoby zostać anulowane
>   ([concurrency](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/control-the-concurrency-of-workflows-and-jobs)).
> - Aplikacja zainstalowana z pliku `.flatpak` nie ma tego źródła i nie dostaje aktualizacji — trzeba ją odinstalować i
>   zainstalować z `.flatpakref`.

## Gdzie w kodzie

- [flatpak/pages.py](../../flatpak/pages.py), [flatpak/strona/](../../flatpak/strona/index.html),
  [flatpak/publikuj.sh](../../flatpak/publikuj.sh), [flatpak/klucz-gpg.sh](../../flatpak/klucz-gpg.sh)
- [.github/workflows/strona.yml](../../.github/workflows/strona.yml)
- Testy: [test_strona_repo.py](../../tests/test_strona_repo.py), [test_pakiet.py](../../tests/test_pakiet.py)

## Dokumentacja

- [GitHub Pages — publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)
- [Flatpak — hosting a repository](https://docs.flatpak.org/en/latest/hosting-a-repository.html)

## Powiązane

- [GitHub Actions](github-actions.md), [Flatpak](flatpak.md)
- [ADR-0007](../decyzje/0007-dystrybucja-repozytorium-flatpak-na-github-pages.md)
