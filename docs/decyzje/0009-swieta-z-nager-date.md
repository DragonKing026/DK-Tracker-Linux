---
noteId: "f281be0e728d4204b8c08ef056d76e4e"
tytul: Święta państwowe z Nager.Date — drugi dozwolony adres
tags: [adr, swieta, siec, prywatnosc]
status: zaakceptowana
zastapiona_przez:
utworzono: 2026-11-20 12:33
zaktualizowano: 2026-11-20 12:33
---

# ADR-0009: Święta państwowe z Nager.Date — drugi dozwolony adres

Zmienia złotą zasadę 11 w [AGENTS.md](../../AGENTS.md) („aplikacja łączy się wyłącznie z adresem Kimai”).

## Kontekst

- Kalendarz i Podsumowania nie znają świąt: święto w tygodniu liczy się jako dzień roboczy i obniża średnią dzienną.
- Użytkownik chce wybrać kraj w Ustawieniach (domyślnie brak), pobrać święta przy wyborze i przyciskiem
  „Synchronizuj”, bez trzymania starszych danych (rozmowa 2026-11-20 12:21; tam też zgoda na tę decyzję).
- Firmowy seats.k4.pl odpadł: jego API wydaje token tylko adminowi i nie zwraca świąt.

## Rozważane opcje

| Opcja | Zalety | Wady |
| --- | --- | --- |
| Liczyć święta lokalnie (reguły w kodzie, Wielkanoc z algorytmu) | zero sieci | reguły dla każdego kraju do utrzymania; zmiany ustawowe (np. nowe święto) wymagają wydania |
| Biblioteka `holidays` (PyPI) | bez sieci, wiele krajów | nowa zależność w paczce; aktualność świąt zależy od wydania aplikacji |
| **API Nager.Date na żądanie użytkownika** | ok. 120 krajów, MIT, bez klucza; nowe dane bez wydania aplikacji | drugi adres poza Kimai; zależność od zewnętrznej usługi przy synchronizacji |

## Decyzja

**Święta pobieramy z Nager.Date wyłącznie na żądanie użytkownika (wybór kraju, przycisk ↻) i trzymamy lokalnie;
domyślnie kraj „brak” — wtedy aplikacja nadal łączy się tylko z Kimai.**

## Uzasadnienie

- Prośba użytkownika wprost dotyczy pobierania z sieci i synchronizacji.
- Zapytanie nie niesie żadnych danych użytkownika poza kodem kraju i rokiem; to nie telemetria.
- Brak połączeń w tle: dane się nie zmieniają bez kliknięcia.

## Konsekwencje

- Zasada 11 brzmi: łączymy się tylko z adresem Kimai i — gdy użytkownik wybierze kraj świąt — z Nager.Date.
- Plik integracji [nager-date](../integracje/nager-date.md); `--share=network` w Flatpaku już jest.
- Gdy usługa zniknie, zapisane święta działają dalej; zamiennikiem byłaby biblioteka `holidays`.

## Powiązane

- [Zadanie 0088 — święta państwowe](../../TODO/W-TRAKCIE/0088-swieta-panstwowe/todo.md)
- [Nager.Date](../integracje/nager-date.md)
