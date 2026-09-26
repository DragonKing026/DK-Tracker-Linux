---
noteId: "c66dc8153a9d44b0b0571016ef286ace"
tytul: Dystrybucja — repozytorium Flatpaka na GitHub Pages i wydania na GitHubie
tags: [adr, flatpak, wydanie, github]
status: zaakceptowana
zastapiona_przez:
utworzono: 2026-09-26 11:57
zaktualizowano: 2026-09-26 11:57
---

# ADR-0007: Dystrybucja przez repozytorium Flatpaka na GitHub Pages i wydania na GitHubie

## Kontekst

Aplikacja jest paczką Flatpak ([ADR-0002](0002-stos-python-pyside6.md)). Użytkownicy (na początek osoby z firmy) mają ją
zainstalować prosto i dostawać aktualizacje bez ręcznego pobierania plików. Repozytorium kodu jest publiczne, konto
GitHuba darmowe. Flathub wymaga przeglądu i ma własne wymagania jakości; na wersję beta to za dużo.

## Rozważane opcje

| Opcja | Zalety | Wady |
| --- | --- | --- |
| A. Sam plik `.flatpak` budowany lokalnie | najprościej | brak aktualizacji, ręczne rozsyłanie |
| B. Plik `.flatpak` z GitHub Actions w wydaniach | powtarzalna budowa, pliki do pobrania | nadal brak automatycznych aktualizacji |
| C. B + podpisane repozytorium Flatpaka na GitHub Pages | aktualizacje w Discover / GNOME Software / `flatpak update`, instalacja jedną komendą | klucz GPG do utrzymania, sekret w repozytorium |
| D. Flathub | widoczność, aktualizacje | przegląd, wymagania (np. zrzuty w OSTree, zweryfikowana domena), czas |

## Decyzja

**Wariant C: paczka budowana lokalnie ([buduj.sh](../../flatpak/buduj.sh)) i przez GitHub Actions po tagu
`v<wersja>`, podpisane repozytorium Flatpaka na GitHub Pages i plik `.flatpak` w wydaniu na GitHubie.**

Decyzja użytkownika z 2026-09-26 10:23 (zadanie [0045](../../TODO/W-TRAKCIE/0045-plan4-projekt-flatpak/todo.md)).

## Uzasadnienie

- Aktualizacje przychodzą same, tak jak dla aplikacji z Flathuba, bez przeglądu Flathuba.
- Hosting nic nie kosztuje (publiczne repozytorium), limity Pages (1 GB, 100 GB/miesiąc) wystarczą dla paczki ~70 MB.
- Ten sam obraz budowy lokalnie i w CI ([ADR-0006](0006-budowanie-flatpaka-w-kontenerze.md)); próba na sucho
  (podpis wszystkich refów, instalacja z `.flatpakref` bez ostrzeżeń, aktualizacja) przeszła
  ([0050](../../TODO/ZROBIONE/0050-plan4-repo-pages/todo.md)).

## Konsekwencje

- Klucz prywatny GPG żyje tylko w sekrecie `FLATPAK_GPG_PRIVATE_KEY`; w repozytorium jest wyłącznie klucz publiczny.
  Utrata klucza oznacza nowy klucz i ponowną instalację u wszystkich.
- Aplikacja zainstalowana z pliku `.flatpak` nie ma źródła aktualizacji — instrukcja mówi, żeby instalować z
  `.flatpakref`.
- Wydanie = tag zgodny z wersją w `pyproject.toml`; workflow: [wydanie.yml](../../.github/workflows/wydanie.yml).
- Flathub zostaje otwarty na później (wersja 1.0 i testy na GNOME).

## Powiązane

- [GitHub Actions](../integracje/github-actions.md), [GitHub Pages](../integracje/github-pages.md),
  [Flatpak](../integracje/flatpak.md)
- [Plan 4](../plany/2026-09-26-plan-4-flatpak.md)
