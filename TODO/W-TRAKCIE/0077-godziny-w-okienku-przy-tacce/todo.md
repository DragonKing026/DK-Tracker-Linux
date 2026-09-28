---
noteId: "20c73124c6c9436592eda1400646be60"
tytul: "Okienko przy tacce: godziny OD/DO z listy, w jednym wierszu; kursor rączki"
numer: "0077"
status: w-trakcie
priorytet: p2
tags: [todo, okno-przy-tacce, wyglad]
zalezy_od: []
utworzono: 2026-09-28 12:43
zaktualizowano: 2026-09-28 13:10
zamknieto:
---

# 0077 — Okienko przy tacce: godziny OD/DO z listy, w jednym wierszu; kursor rączki

> [!info] Status
> **w-trakcie** · priorytet **p2** · [← tablica zadań](../../README.md)

## Cel

Pola godziny rozpoczęcia i zakończenia trwającego wpisu w okienku przy tacce zajmują mniej miejsca i działają jak w
oknie głównym: godzinę się wybiera, nie wpisuje. Wszystko, co da się kliknąć, pokazuje kursor rączki.

## Kontekst

- Uwaga użytkownika (zrzut niżej): ramka OD/DO ma trzy wiersze (etykiety, pola, „puste = teraz”), a pola to zwykłe
  pola tekstowe z maską `--:--`. Najechanie na przyciski, listy i wiersze nie zmienia kursora.
- Wzór: `TimeField.qml` okna głównego — przycisk z ikoną zegara, po kliknięciu lista godzin i minut (co 5 min, plus
  minuta z Kimai spoza kroku) —
  [wygląd okna głównego](../../../docs/architektura/wyglad-okna-glownego.md).
- Okienko przy tacce jest w Qt Widgets ([form.py](../../../src/dk_tracker/ui/form.py)), więc potrzebny jest jego
  odpowiednik w widżetach.

## Kryteria akceptacji

- [x] OD i DO w jednym wierszu razem z podpowiedzią „puste = teraz”
- [x] Godzinę wybiera się z listy godzin i minut (jak w oknie głównym); DO da się wyczyścić (= teraz)
- [x] Zmiana OD zapisuje godzinę rozpoczęcia, DO jest brane przy stopie — jak dotąd
- [x] Kursor rączki nad przyciskami, listami, polami wyboru godziny i wierszami wpisów
- [x] Testy i dokumentacja zaktualizowane
- [ ] Zmiany zacommitowane małymi krokami

## Kroki

- [x] Widżet wyboru godziny (`TimePicker`) z testami
- [x] Wiersz OD/DO w formularzu
- [x] Kursor rączki
- [x] Dokumentacja

## Materiały

![Przed: pola OD/DO w trzech wierszach, wpisywane](zrzuty/przed-pola-od-do.png)

Po zmianie (render offscreen, ciemny i jasny motyw):

![Po: OD i DO w jednym wierszu, ciemny](zrzuty/po-okno-dark.png)
![Po: OD i DO w jednym wierszu, jasny](zrzuty/po-okno-light.png)
![Po: lista godzin i minut, ciemna](zrzuty/po-lista-dark.png)
![Po: lista godzin i minut, jasna](zrzuty/po-lista-light.png)

## Dziennik

### 2026-09-28 12:43

- Utworzono zadanie.
- **12:43** Start pracy.

### 2026-09-28 13:10

- `TimePicker` ([time_picker.py](../../../src/dk_tracker/ui/time_picker.py)): przycisk z zegarem, lista godzin
  i minut, zmiana zgłaszana raz po zamknięciu listy, „Teraz” czyści koniec. OD/DO w jednym wierszu.
- Kursor rączki: przyciski formularza i nagłówka, listy, wiersze wpisów, lista projektów.
- Testy: 757 zielonych. Czeka na sprawdzenie przez użytkownika na KDE (lista w warstwie layer-shell).

## Wynik

<!-- Wypełniane przy zamknięciu: co powstało, gdzie, co zostało na później. -->
