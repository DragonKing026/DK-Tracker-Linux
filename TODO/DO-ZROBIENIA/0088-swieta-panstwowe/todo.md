---
noteId: "21bc84e3ba1545138a710c7afe833fbf"
tytul: "Święta państwowe w Kalendarzu i Podsumowaniach"
numer: "0088"
status: do-zrobienia
priorytet: p2
tags: [todo, swieta, kalendarz, podsumowania, ustawienia]
zalezy_od: []
utworzono: 2026-11-20 12:21
zaktualizowano: 2026-11-20 12:21
zamknieto:
---

# 0088 — Święta państwowe w Kalendarzu i Podsumowaniach

> [!info] Status
> **do-zrobienia** · priorytet **p2** · [← tablica zadań](../../README.md)

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

- [ ] Kraj w Ustawieniach (domyślnie brak), pobranie przy wyborze i przyciskiem ↻ „Synchronizuj”, nadpisanie danych
- [ ] Święta zaznaczone w Kalendarzu (nazwa w nagłówku dnia)
- [ ] Podsumowania nie liczą świąt jako dni roboczych
- [ ] Testy rdzenia (parsowanie, filtr `global`, dni robocze) bez sieci; pokrycie rdzenia ≥ 90%
- [ ] ADR, plik integracji, zmiana zasady 11 w AGENTS.md, dokumentacja widoków
- [ ] Zmiany zacommitowane małymi krokami

## Kroki

- [ ] ADR + [AGENTS.md](../../../AGENTS.md) (zasada 11) + plik integracji Nager.Date
- [ ] Rdzeń: `core/holidays.py` (klient, zapis, zapytania), lista krajów
- [ ] Podsumowania: dni robocze bez świąt
- [ ] Ustawienia: kraj + ↻ Synchronizuj
- [ ] Kalendarz: oznaczenie świąt
- [ ] Dokumentacja architektury i widoków

## Materiały

Brak.

## Dziennik

### 2026-11-20 12:21

- Utworzono zadanie.

## Wynik

<!-- Wypełniane przy zamknięciu: co powstało, gdzie, co zostało na później. -->
