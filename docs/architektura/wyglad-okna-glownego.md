---
noteId: "58e626bf9a2344179f812d9a43cf1830"
tytul: Wygląd okna głównego — kolory, kontrolki, układ
tags: [architektura, ui, qml, wyglad, motyw]
utworzono: 2026-09-26 18:57
zaktualizowano: 2026-09-27 12:40
---

# Wygląd okna głównego — kolory, kontrolki, układ

Jeden projekt wyglądu dla całego okna głównego ([F-35](funkcje.md#f-35-okno-główne-0100)): najpierw kolory, potem
kontrolki ze wszystkimi stanami, na końcu układ widoków. Nowy widok (Podsumowania, Kalendarz) składa się z tych samych
kontrolek. Powstał po teście na żywo 0.10.0, gdy poprawki pojedynczych uwag („zlewa się”, „bije po oczach”) psuły
jedna drugą ([0069](../../TODO/ZROBIONE/0069-plan5-okno-glowne/todo.md)).

## Zasady

- **Warstwy widać od razu**: tło treści → pasek boczny i pasek timera → okno edycji; pola do wpisywania są ciemniejsze
  (w jasnym motywie — białe) od tła, przyciski i listy jaśniejsze; każda kontrolka ma ramkę.
- **Jeden akcent** (niebieski) tylko na fokus, główną akcję i zaznaczenie — jako tekst i ramka, nie pełne tło.
  **Zielony** tylko start i „płatne”, **czerwony** tylko stop i usuwanie.
- **Tekst zawsze czytelny**: wyłączona kontrolka ma tekst `muted` i tło `panel`, nie przezroczystość całości.
- Kolor jest w adresie każdego rysowanego obrazka (`image://glyph/<nazwa>/<rrggbb>`, `image://icons/mark/<rrggbb>`):
  QML trzyma obrazki według adresu, więc po zmianie motywu stary kolor by został.
- Motyw jasny albo ciemny: jak w systemie (domyślnie) albo wybrany w ustawieniach (`Settings.theme`: `auto`,
  `light`, `dark`) — ten sam dla okna głównego i okienka przy tacce.

## Kolory (`theme.py`: `MAIN_DARK`, `MAIN_LIGHT`)

| Token | Ciemny | Jasny | Gdzie |
| --- | --- | --- | --- |
| `bg` | `#1a1d23` | `#ffffff` | tło treści (lista, ustawienia) |
| `surface` | `#20242b` | `#f4f5f7` | pasek boczny, pasek timera, nagłówki dni, najechany wiersz |
| `panel` | `#272b34` | `#ffffff` | okno edycji, rozwijane listy, kalendarz, pasek „Cofnij” |
| `input` | `#14171c` | `#ffffff` | pola tekstowe |
| `control` | `#2d323c` | `#eef0f3` | przyciski, listy, wybór dnia i godziny |
| `control_hover` | `#373d48` | `#e3e6eb` | … pod kursorem |
| `control_down` | `#414855` | `#d6dae0` | … wciśnięte |
| `border` | `#4a515e` | `#c3c8d0` | ramki kontrolek |
| `border_hover` | `#5f6776` | `#a4abb6` | ramka pod kursorem |
| `divider` | `#2c3038` | `#e6e8ec` | linie między wierszami, podział stopki |
| `fg` | `#e6e8ec` | `#1d2026` | tekst |
| `muted` | `#9ba2ae` | `#626974` | etykiety pomocnicze, ikony |
| `placeholder` | `#737a87` | `#8b919b` | podpowiedź w pustym polu, tekst wyłączony |
| `accent` | `#6f9bf2` | `#2563eb` | fokus, główna akcja, zaznaczenie |
| `start` | `#2ea043` | `#1a7f37` | start, „płatne” |
| `danger` | `#e5534b` | `#cf222e` | stop, usuń, zamknij pod kursorem, błędy |
| `danger_bg` | `#3a2124` | `#fdecec` | pasek błędu |

## Kontrolki (`ui/main_window/qml/`)

Wysokość 34 px, promień 4 px (okna i listy — 8 px), odstępy 8 / 12 / 16 px, tekst 14 px, etykiety formularza 13 px
półgrube. Kursor rączki na wszystkim, co się klika.

| Kontrolka | Plik | Wygląd i stany |
| --- | --- | --- |
| Pole tekstowe | `Field.qml` | `input`, ramka `border`; kursor → `border_hover`; fokus → `accent`; wyłączone → tło `panel`, tekst `placeholder` |
| Opis (wiele linii) | `DescriptionArea.qml` | jak pole; Enter potwierdza, Shift+Enter — nowa linia; rośnie do `maxLines` |
| Przycisk | `Btn.qml` | `control` + ramka; odmiany: `primary` (tekst i ramka `accent`), `danger` (tekst, ikona i ramka `danger`, pod kursorem czerwone tło 15 %), `flat` (bez tła i ramki); opcjonalna ikona przed tekstem |
| Przycisk-ikona | `IconButton.qml` | bez tła; pod kursorem `control_hover`; `danger`: pod kursorem czerwone tło, biała ikona (jak zamykanie okna) |
| Wybór (lista, projekt, dzień, godzina) | `SelectButton.qml` → `Combo`, `ProjectPicker`, `DateField`, `TimeField` | wygląd przycisku, tekst do lewej, ikona z lewej (kalendarz, zegar), strzałka w dół z prawej (listy) |
| Lista godzin, kalendarz | `TimeField.qml`, `DateField.qml` | wybrana pozycja: tło `control`, ramka i pogrubiony tekst `accent` (bez pełnego niebieskiego tła); dziś — ramka `border` |
| Tagi | `TagPicker.qml` | pole jak `Field` z kafelkami wybranych tagów (kolor tagu, × pod kursorem czerwony), „+ tag” otwiera `Panel` z wyszukiwaniem i listą tagów Kimai; nazwę spoza listy można dodać |
| Pole wyboru | `Check.qml` | kwadrat 18 px, zaznaczony — `accent` z białym ✓ |
| Liczba | `Spin.qml` | [−] pole [+] w jednej ramce |
| Pasek przewijania | `Scroller.qml` | uchwyt 6 px, zaokrąglony, w kolorze `border` (pod kursorem `border_hover`); widoczny zawsze, gdy jest co przewijać — w każdej liście i stronie |
| Okno / lista rozwijana | `Panel.qml` | `panel`, ramka `border`, promień 8 |
| Karta | `Card.qml` | `surface`, ramka `divider`, promień 8 — kafelek z liczbą, wykres, podział (podsumowania) |
| Przełącznik | `Segmented.qml` | przyciski w jednej ramce jak przycisk (`control`, `border`); wybrany: tekst półgruby i ramka `accent`; między dwoma niewybranymi cienka kreska `border` |
| Wykres słupkowy | `BarChart.qml` | linie godzin `divider`, podpisy 11 px `muted`; słupki w kolorach projektów, szew 1 px między warstwami, zaokrąglona góra (3 px); norma — linia przerywana `fg` 55 % (słupki dni) albo kreska nad słupkiem (miesiące); kolumna pod kursorem na tle `control`; dziś — podpis `accent` pogrubiony; dymek w `Panel` |
| Pierścień | `DonutChart.qml` | grubość 24 px, odstęp 1,2° między wycinkami, tor `divider`; w środku suma (20 px pogrubiona) i podpis `muted` |
| Wiersz formularza | `FormRow.qml` | etykieta z lewej (130 px, w ustawieniach 230 px; długa zawija się), kontrolka z prawej — w oknie edycji i w ustawieniach |

## Widoki

- **Pasek boczny** (`surface`): znak i nazwa, pozycje 36 px; aktywna — tło `control` i pasek `accent` z lewej.
- **Pasek timera** (`surface`, linia `divider` pod spodem): tryb ⏱/✎, opis, projekt, rodzaj pracy, `$`,
  (trwa: od, zegar), okrągły start (zielony) / stop (czerwony) / dodaj (akcent). Tryb ręczny: druga linia — dzień,
  od – do.
- **Lista**: wyszukiwanie; tydzień (15 px, pogrubiony), dzień (`surface`, 12 px, `muted`), wiersze 44 px z linią
  `divider`, pod kursorem `surface`.
- **Okno edycji** (`Panel`, 600 px): tytuł, kłódka (wyeksportowany — pasek informacji), zamknij; formularz
  `FormRow`: Dzień, Godziny (od – do, czas trwania obok), Projekt, Rodzaj pracy, Płatne (`$` + słowo), Opis, Tagi,
  pola dodatkowe; stopka po linii `divider`: **Usuń** (`danger`, kosz) z lewej, **Anuluj**, **Zapisz**
  (`primary`) z prawej. Kliknięcie obok i Esc zamykają.
- **Ustawienia**: ten sam `FormRow`, szerokość do 680 px.
- **Podsumowania** (0.10.3, F-36), marginesy 16 px, odstępy 12 px: pasek okresu (`Segmented` Tydzień / Miesiąc / Rok
  / Zakres, ◀ nazwa okresu ▶ — przy zakresie dwa `DateField` — i „Dziś”, wyłączone w bieżącym okresie; zawija się
  w wąskim oknie); rząd kafelków `Card` równej szerokości i wysokości (podpis 12 px `muted`, liczba 22 px
  pogrubiona, pasek 4 px: płatne — `start`, średnia wobec normy — `accent`, dopisek 12 px `muted`); karta wykresu
  (240 px); karta podziału (pierścień 176 px, tabela: kropka, nazwa · klient, czas półgruby, udział, w tym płatne).
  Odświeżenie tego samego okresu: karty na 60 %; nowy okres: „–” w kafelkach i „Wczytywanie…” w kartach.

## Sprawdzanie

Zrzuty wszystkich widoków w obu motywach (bez ekranu, `QQuickWindow.grabWindow()`) przed pokazaniem: lista, trwający
wpis, tryb ręczny, okno edycji, okno edycji wyeksportowanego wpisu, kalendarz i lista godzin otwarte, ustawienia,
błąd i „Cofnij”; podsumowania: tydzień, miesiąc, rok, zakres, dymek, podział wg klienta, pusty okres, wczytywanie; do
tego szerokość minimalna 800 px.

## Powiązane

- [Funkcje — F-35](funkcje.md#f-35-okno-główne-0100)
- [Qt / PySide6 — pułapki QML](../integracje/qt-pyside6.md)
- [Specyfikacja 0.10](../specyfikacja/2026-09-26-okno-glowne-0.10.md)
