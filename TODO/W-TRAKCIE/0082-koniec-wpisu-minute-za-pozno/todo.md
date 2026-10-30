---
noteId: "90eea3e4898e4913abcbef352fe2441a"
tytul: "Koniec wpisu zapisany o minutę za późno — nakładanie na osi czasu"
numer: "0082"
status: w-trakcie
priorytet: p1
tags: [todo, blad, kimai, kalendarz]
zalezy_od: []
utworzono: 2026-10-30 14:19
zaktualizowano: 2026-10-30 14:59
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

- [x] Zasady zaokrąglania sprawdzone w dokumentacji Kimai (z linkiem) —
      [Kimai API: zaokrąglanie](../../../docs/integracje/kimai-api.md#zaokrąglanie-czasów).
- [x] Błąd odtworzony na lokalnym Kimai (`tests/kimai/kimai-testowe.sh up`), wynik w `testy/`.
- [x] Poprawka i test regresji (jednostkowy i kontraktowy na lokalnym Kimai).
- [x] Dokumentacja zaktualizowana.

## Kroki

- [x] Dokumentacja zaokrąglania (Context7 / kimai.org).
- [x] Odtworzenie: start, stop, start na lokalnym Kimai.
- [x] Wybór poprawki, test, kod, docs.

## Materiały

- [odtworz_zaokraglanie.py](testy/odtworz_zaokraglanie.py) — pięć scenariuszy na lokalnym Kimai (konto `jan`, UTC):
  `/stop` i start zaraz po nim, PATCH `end` z sekundami, PATCH `end` na pełnej minucie, koniec przed początkiem,
  start przy trwającym wpisie.
- [odtworzenie-kimai-2.67.log](testy/odtworzenie-kimai-2.67.log) — wynik: `/stop` o 13:24:37 → koniec 13:25:00,
  następny wpis → początek 13:24:00 (minuta nakładania); `end` 13:24:00 zostaje; koniec przed początkiem → 400;
  automatyczne zatrzymanie przez serwer też zaokrągla w górę.

## Dziennik

### 2026-10-30 14:19

- Utworzono zadanie.
- **14:22** Start pracy: dokumentacja zaokrąglania i odtworzenie na lokalnym Kimai.

### 2026-10-30 14:28

- Dokumentacja Kimai ([configurations](https://www.kimai.org/documentation/configurations.html)) i kod 2.67.0
  (`DurationCalculator`, `DefaultRounding`): tryb `default` — begin w dół, end w górę do minuty, przy każdym zapisie
  zakończonego wpisu (także PATCH z `end` i automatyczny stop). Hipoteza z rozpoznania potwierdzona na żywo.
- Poprawka (9aa2098): stop „teraz” i wznowienie wysyłają PATCH z `end` = „teraz − 1 s” zaokrąglone w dół do minuty;
  ta sama chwila co `begin` startu, więc koniec nigdy nie wypada po początku następnego wpisu — także w pierwszej
  sekundzie minuty. Wpis w obrębie jednej minuty: `/stop` (inaczej 400).
- Testy: jednostkowe w [test_tracker_actions.py](../../../tests/core/test_tracker_actions.py) (stop, wpis
  w jednej minucie, wznowienie dla sekund 0,4–59,9) i kontraktowy
  `test_a_resumed_entry_begins_where_the_stopped_one_ended` — bez poprawki nie przechodzi (koniec 13:27, początek
  13:26). Wszystkie testy: 780 + 20 kontraktowych zielone. Docs: 7f67aa2.
- Czego poprawka nie obejmie: automatycznego zatrzymania przez Kimai (start w innym kliencie) i innej reguły
  zaokrąglania na serwerze (np. co 5 min) — opisane w [Kimai API](../../../docs/integracje/kimai-api.md).
- Poprawka gotowa, czeka na wydanie.

### 2026-10-30 14:59

- Wydane w 0.10.18 (46a116f, tag `v0.10.18`); `flatpak update` je widzi. Czeka na potwierdzenie u użytkownika.

## Wynik
