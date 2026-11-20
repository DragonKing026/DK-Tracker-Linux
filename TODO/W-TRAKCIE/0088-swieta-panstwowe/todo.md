---
noteId: "21bc84e3ba1545138a710c7afe833fbf"
tytul: "Święta państwowe w Kalendarzu i Podsumowaniach"
numer: "0088"
status: w-trakcie
priorytet: p2
tags: [todo, swieta, kalendarz, podsumowania, ustawienia]
zalezy_od: []
utworzono: 2026-11-20 12:21
zaktualizowano: 2026-11-20 12:40
zamknieto:
---

# 0088 — Święta państwowe w Kalendarzu i Podsumowaniach

> [!info] Status
> **w-trakcie** · priorytet **p2** · [← tablica zadań](../../README.md)

## Cel

Aplikacja zna święta państwowe wybranego kraju: zaznacza je w Kalendarzu i nie liczy ich jako dni roboczych
w Podsumowaniach (średnia dzienna i norma).

## Kontekst

- Prośba użytkownika (2026-11-20 12:21). Rozważana integracja z firmowym seats.k4.pl (urlopy, dni wolne) odpadła —
  jego API jest tylko dla admina; zamiast niej same święta państwowe z publicznego API.
- Źródło: [Nager.Date](../../../docs/integracje/nager-date.md) — darmowe, bez klucza, ok. 120 krajów.
- Wyjątek od złotej zasady 11 („tylko adres Kimai”) — [AGENTS.md](../../../AGENTS.md); decyzja w ADR.
- Podsumowania liczą średnią jako czas ÷ dni robocze —
  [specyfikacja 0.10](../../../docs/specyfikacja/2026-09-26-okno-glowne-0.10.md).

## Ustalenia

- Ustawienia: pole **Święta — kraj**, domyślnie **brak** (wtedy żadnego połączenia z Nager.Date).
- Wybór kraju pobiera święta od razu; obok przycisk ↻ z podpowiedzią **Synchronizuj** — pobiera ponownie.
  Każde pobranie **nadpisuje** poprzednie dane (bez historii). Wybór „brak” usuwa zapisane święta.
- Pobierane lata: poprzedni, bieżący i następny (decyzja agenta).
- Tylko święta ogólnokrajowe (`global: true`); regionalne (np. landy) pomijane (decyzja agenta).
- Błąd pobrania: zapisane dane zostają, komunikat przy polu (decyzja agenta).
- Kalendarz: nagłówek dnia ze świętem pokazuje jego nazwę, kolumna dnia wyróżniona.
- Podsumowania: święto w dzień roboczy nie jest dniem roboczym (średnia, norma słupka); praca w święto podnosi
  średnią, jak praca w sobotę.

## Kryteria akceptacji

- [x] Kraj w Ustawieniach (domyślnie brak), pobranie przy wyborze i przyciskiem ↻ „Synchronizuj”, nadpisanie danych
- [x] Święta zaznaczone w Kalendarzu (nazwa w nagłówku dnia)
- [x] Podsumowania nie liczą świąt jako dni roboczych
- [x] Testy rdzenia (parsowanie, filtr `global`, dni robocze) bez sieci; pokrycie rdzenia ≥ 90%
- [x] ADR, plik integracji, zmiana zasady 11 w AGENTS.md, dokumentacja widoków
- [x] Zmiany zacommitowane małymi krokami

## Kroki

- [x] ADR + [AGENTS.md](../../../AGENTS.md) (zasada 11) + plik integracji Nager.Date
- [x] Rdzeń: `core/holidays.py` (klient, zapis, zapytania), lista krajów
- [x] Podsumowania: dni robocze bez świąt
- [x] Ustawienia: kraj + ↻ Synchronizuj
- [x] Kalendarz: oznaczenie świąt
- [x] Dokumentacja architektury i widoków

## Materiały

Zrzuty offscreen w obu motywach (dane zmyślone, święta wpisane z ręki, Polska, tydzień z 2026-11-11), generowane
skryptem [prototyp/zrzuty-swieta.py](prototyp/zrzuty-swieta.py):

| Widok | Ciemny | Jasny |
| --- | --- | --- |
| Ustawienia — po synchronizacji | [zrzut](zrzuty/ustawienia-swieta-ok-ciemny.png) | [zrzut](zrzuty/ustawienia-swieta-ok-jasny.png) |
| Ustawienia — błąd pobrania | [zrzut](zrzuty/ustawienia-swieta-blad-ciemny.png) | [zrzut](zrzuty/ustawienia-swieta-blad-jasny.png) |
| Kalendarz tygodnia ze świętem | [zrzut](zrzuty/kalendarz-swieta-ciemny.png) | [zrzut](zrzuty/kalendarz-swieta-jasny.png) |
| Podsumowania tygodnia ze świętem | [zrzut](zrzuty/podsumowania-swieta-ciemny.png) | [zrzut](zrzuty/podsumowania-swieta-jasny.png) |
| Kalendarzyk wyboru daty (Zakres) | [zrzut](zrzuty/kalendarzyk-swieta-ciemny.png) | [zrzut](zrzuty/kalendarzyk-swieta-jasny.png) |

## Dziennik

### 2026-11-20 12:21

- Utworzono zadanie.
- **12:23** Start pracy: rdzeń, Podsumowania, Ustawienia, Kalendarz.
- **12:40** Zrobione (do sprawdzenia przez koordynatora): rdzeń (`core/holidays.py`, lista krajów), Podsumowania
  (dni robocze i norma bez świąt), Ustawienia (pole kraju, ↻, status), Kalendarz (nazwa w nagłówku, tło kolumny),
  słupki Podsumowań i kalendarzyk daty, dokumentacja
  ([F-38](../../../docs/architektura/funkcje.md#f-38-święta-państwowe)),
  zrzuty w obu motywach. Decyzje: dane innego kraju niż wybrany nie są używane; ↻ działa tylko dla zapisanego kraju
  (nowy kraj pobiera „Zapisz”); osobny worker „holidays”; nazwy krajów po angielsku (Qt nie zna polskich).

## Wynik

<!-- Wypełniane przy zamknięciu: co powstało, gdzie, co zostało na później. -->
