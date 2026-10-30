---
noteId: "90eea3e4898e4913abcbef352fe2441a"
tytul: "Koniec wpisu zapisany o minutę za późno — nakładanie na osi czasu"
numer: "0082"
status: w-trakcie
priorytet: p1
tags: [todo, blad, kimai, kalendarz]
zalezy_od: []
utworzono: 2026-10-30 14:19
zaktualizowano: 2026-10-30 14:22
zamknieto:
---

# 0082 — Koniec wpisu zapisany o minutę za późno — nakładanie na osi czasu

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wpis zatrzymany w aplikacji kończy się najpóźniej tam, gdzie zaczyna się wpis rozpoczęty zaraz po nim. W kalendarzu
wpisy stoją jeden za drugim i nie nachodzą na siebie.

## Kontekst

- Zgłoszenie użytkownika (2026-10-30): zakończony wpis ma koniec o minutę za późno i w kalendarzu nachodzi na następny.
- Rozpoznanie (sam odczyt kodu): `Tracker.stop()` bez godziny wywołuje `PATCH /api/timesheets/{id}/stop`
  ([kimai_client.py](../../../src/dk_tracker/core/kimai_client.py)), więc koniec ustala serwer. Start wysyła
  „teraz − 1 s” ([timefmt.py](../../../src/dk_tracker/core/timefmt.py)). Hipoteza: domyślne zaokrąglanie Kimai
  (początek w dół, koniec w górę do minuty) daje nakładanie o minutę. Dotyczy też `resume()`.
- [Kimai API — format dat i zaokrąglanie](../../../docs/integracje/kimai-api.md).

## Kryteria akceptacji

- [ ] Zasady zaokrąglania sprawdzone w dokumentacji Kimai (z linkiem).
- [ ] Błąd odtworzony na lokalnym Kimai (`tests/kimai/kimai-testowe.sh up`), wynik w `testy/`.
- [ ] Poprawka i test regresji (jednostkowy i kontraktowy na lokalnym Kimai).
- [ ] Dokumentacja zaktualizowana.

## Kroki

- [ ] Dokumentacja zaokrąglania (Context7 / kimai.org).
- [ ] Odtworzenie: start, stop, start na lokalnym Kimai.
- [ ] Wybór poprawki, test, kod, docs.

## Materiały

## Dziennik

### 2026-10-30 14:19

- Utworzono zadanie.
- **14:22** Start pracy: dokumentacja zaokrąglania i odtworzenie na lokalnym Kimai.

## Wynik
