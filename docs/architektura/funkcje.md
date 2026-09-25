---
noteId: "4e19ba9a67884984964e334472d5e850"
tytul: Katalog funkcji
tags: [architektura, funkcje, wymagania]
utworzono: 2026-09-25 17:17
zaktualizowano: 2026-09-26 00:22
---

# Katalog funkcji

Każda funkcja ma identyfikator `F-NN`, na który powołują się zadania w `TODO/` i testy.
Opis zachowania pochodzi z analizy kodu wtyczki
[WS Tracker 1.5.1](../integracje/kimai-ws-tracker.md) — kolumna „Źródło” wskazuje plik.
Endpointy opisane są w [Kimai REST API](../integracje/kimai-api.md).

## Mapa stanów aplikacji

```mermaid
stateDiagram-v2
    [*] --> Nieskonfigurowana: brak URL lub tokenu
    Nieskonfigurowana --> Bezczynna: zapisano ustawienia
    [*] --> Bezczynna: GET /api/timesheets/active = []
    [*] --> Trwa: GET /api/timesheets/active = [wpis]
    Bezczynna --> Trwa: Start / Wznów
    Trwa --> Bezczynna: Stop / Stop z godziną końca
    Trwa --> Trwa: edycja opisu, początku, billable / Wznów inny wpis
    Bezczynna --> Blad: błąd sieci / 401 / 5xx
    Trwa --> Blad: błąd sieci / 401 / 5xx
    Blad --> Bezczynna: odświeżenie OK
    Blad --> Trwa: odświeżenie OK
```

---

## F-01 Konfiguracja połączenia

| | |
| --- | --- |
| **Co** | Adres Kimai, token API, język (auto/pl/en), minimalna długość opisu (domyślnie 15, 0 = wyłączone). |
| **Test połączenia** | `GET /api/users/me` → komunikat „Połączono jako *alias/username*” albo powód błędu. |
| **Zapis** | URL obcięty z końcowych `/`. Zapis ustawień **resetuje blokadę billable** (F-09), bo inny serwer/token może mieć uprawnienie. |
| **Źródło** | `options/options.js`, `lib/api.js#getSettings` |
| **Różnica w aplikacji** | Token → magazyn sekretów ([Secret Service](../integracje/secret-service.md)), nie plik ustawień. Brak odpowiednika „host permissions” Chrome — Flatpak ma dostęp do sieci przez `--share=network`. |

## F-02 Ikona w tacce ze stanem

| | |
| --- | --- |
| **Co** | Odpowiednik „badge” wtyczki. Pokazuje, czy timer działa i jak długo. |
| **Format czasu** | `<60 min` → `47m`; `≥60 min` → `1:22` (wtyczka zmieniła z `1h22`, bo Chrome ucinał do 5 znaków). |
| **Kolory wtyczki** | szary `#6b7280` — nic nie trwa / brak konfiguracji; zielony `#16a34a` — trwa; czerwony `#dc2626` + `!` — błąd. |
| **Odświeżanie** | Co 1 minutę (`chrome.alarms`) + natychmiast po start/stop. |
| **Źródło** | `background.js` |
| **Różnica w aplikacji** | Tacka SNI nie ma „badge z tekstem”, więc **czas rysujemy w samej ikonie** (wariant C, decyzja użytkownika 2026-09-25): nic nie trwa → szary zegar; trwa → `47m` / `1:22` białym pogrubionym tekstem na zielonym zaokrąglonym kwadracie; błąd → `!` na czerwonym. Pełna informacja (czas, projekt, opis) w **tooltipie**. Makieta: [0028](../../TODO/ZROBIONE/0028-plan3-projekt-ui/zrzuty/ikony-warianty.png). Etykieta obok ikony na GNOME (`XAyatanaLabel`) — do sprawdzenia w [0020](../../TODO/DO-ZROBIENIA/0020-testy-gnome/todo.md). Patrz [StatusNotifierItem](../integracje/statusnotifieritem.md). |
| **Kliknięcia ikony** | lewy → okno (F-03), prawy → menu (F-20), **środkowy → nic** (decyzja użytkownika 2026-09-25: żadnej akcji bez okna/menu, żeby nie zatrzymać timera przypadkiem). |

## F-03 Okno szybkiej obsługi (popup)

| | |
| --- | --- |
| **Co** | Po kliknięciu ikony: nagłówek (nazwa, suma dnia, suma tygodnia, ustawienia), pasek trackera, komunikaty, lista ostatnich wpisów. |
| **Szerokość** | 460 px we wtyczce 1.5.0. |
| **Stan „nieskonfigurowana”** | Tylko tekst + przycisk „Otwórz ustawienia”. |
| **Źródło** | `popup/popup.html`, `popup/popup.css` |
| **Różnica w aplikacji** | **KDE:** okno zakotwiczone przy tacce (`layer-shell`, prawy dolny róg nad panelem). **Gdzie indziej:** okno bezramkowe, zwykle na środku. Lewy klik ikony otwiera okno; **klik ikony przy otwartym oknie go nie zamyka** (Plasma nie wysyła `Activate`) — zamyka przycisk w nagłówku, `Esc` albo klik obok (utrata fokusu). Wpisany opis zostaje po schowaniu. Bez hosta tacki: zwykłe okno z ramką. Decyzja: [ADR-0005](../decyzje/0005-okno-przy-tacce-na-kde.md) (sprawdzone w prototypie 0004). |

## F-04 Start timera

1. Wymagane: projekt (`errNoProject`), czynność (`errNoActivity`), opis zgodny z F-11.
2. `POST /api/timesheets` z `begin` = czas **minus 1 s** w formacie
   `YYYY-MM-DDTHH:mm:ss` bez strefy, `project`, `activity`, `description`, opcjonalnie
   `billable` (F-09).
   **Różnica w aplikacji:** wtyczka bierze czas przeglądarki. Aplikacja liczy go
   w **strefie konta Kimai** (`/api/users/me → timezone`), bo Kimai dokleja tę strefę
   bez przeliczania. Przy różnych strefach wtyczka zapisuje wpis przesunięty w czasie
   (sprawdzone: [raport](../../TODO/ZROBIONE/0002-specyfikacja-projektu/testy/raport-kimai-docker-2026-09-25.md)).
3. Zapamiętanie `lastProject`, `lastActivity` (F-06).
4. Odświeżenie ikony (F-02) i okna.
5. **Enter** w polu opisu = start; **Shift+Enter** = nowa linia.

Źródło: `popup.js#startTracking`, `api.js#start`, `api.js#localStamp`.

## F-05 Stop timera

- Bez godziny końca → `PATCH /api/timesheets/{id}/stop`.
- Z wpisaną godziną „do” → `PATCH /api/timesheets/{id}` z `end` (ten sam dzień co
  początek). Walidacja: koniec > początek (`errEndBeforeBegin`).

Źródło: `popup.js#stopTracking`.

## F-06 Wybór projektu i czynności

- Projekty: `GET /api/projects?visible=1&ignoreDates=1` (bez `ignoreDates` API ukrywa
  projekty z minionym oknem dat).
- Klienci: `GET /api/customers?visible=1` — tylko po to, by wiedzieć, którzy są
  niebillable (błąd tego zapytania jest ignorowany).
- **Grupowanie po kliencie** (`parentTitle`), sortowanie alfabetyczne klientów i projektów
  — lista 75 projektów bez grup była nieużywalna.
- Kropka z kolorem projektu (`project.color`), szara gdy nic nie wybrano.
- Czynności: `GET /api/activities?visible=1&globals=true&project={id}`, sortowane.
- Zmiana projektu przebudowuje czynności i resetuje billable do domyślnego.
- Ostatni wybór pamiętany lokalnie i przywracany, jeśli nadal istnieje na liście.
- W trakcie trwania wpisu projekt i czynność są **zablokowane** (zmiana = inny wpis,
  nie korekta).

- **W aplikacji (prośba użytkownika, poza wtyczką):** lista projektów otwiera się z polem wyszukiwania na górze
  (jak Select2): filtr po nazwie projektu i klienta, bez wielkości liter i polskich znaków, Enter wybiera pierwszy
  wynik, strzałki chodzą tylko po projektach — [ui/project_picker.py](../../src/kimai_tray/ui/project_picker.py).

Źródło: `popup.js#fillPickers`, `#onProjectChange`, `#restoreLastActivity`.

## F-07 Edycja trwającego wpisu

| Pole | Zachowanie |
| --- | --- |
| Opis | Zapis po 1,2 s od końca pisania (cicho) i przy utracie fokusu. Walidacja F-11; przy zapisie „cichym” błąd walidacji nie jest pokazywany. Enter = zatwierdź. |
| Początek (HH:MM) | Ten sam dzień co pierwotny początek. Przyszłość → `errBeginFuture`. `PATCH` z `begin`, zegar restartuje od nowej wartości. |
| Koniec (HH:MM) | Nie zapisuje od razu — używany przy Stop (F-05). |
| Billable | `PATCH` z `billable` natychmiast (F-09). |

Po udanym zapisie — krótki (2 s) zielony komunikat „Zapisano…”.
Źródło: `popup.js#saveDescription`, `#onBeginChange`, `#onBillableClick`.

## F-08 Lista ostatnich wpisów

- `GET /api/timesheets?size=20&orderBy=begin&order=DESC&full=true`.
- **Nie** `/api/timesheets/recent` — ten zwija listę do jednej pozycji na parę
  projekt+czynność, przez co „ginęły” godziny.
- Pomija wpis trwający (`end == null`).
- Grupowanie po dniu lokalnym: „Dziś”, „Wczoraj”, dalej data (`pon., 22 wrz`), suma dnia
  w formacie `h:mm`.
- Wiersz: kropka koloru projektu, opis (maks. 2 linie, znaki nowej linii → spacje,
  pełny opis w podpowiedzi; brak opisu → „bez opisu”), „projekt - czynność”, czas trwania,
  zakres `HH:MM-HH:MM`, przycisk `$` (F-09), przycisk ▶ wznów (F-10).
- Pod listą link „Moje czasy” → `{url}/{locale}/timesheet/`. Kimai nie ma trasy bez
  locale; locale brane z `entry.user.language` i zapamiętywane.

Źródło: `popup.js#renderRecent`, `#recentRow`, `#rememberKimaiLocale`.

## F-09 Billable

- Przełącznik `$` przy projekcie: zielony = na fakturę klienta, szary przekreślony = czas
  wewnętrzny.
- **Domyślna wartość** jak w Kimai: billable, chyba że klient, projekt lub czynność ma
  `billable=false`.
- **Nietknięty przełącznik nie jest wysyłany** — decyzję zostawiamy Kimai.
- Ręczna zmiana obowiązuje dla jednego wpisu; zmiana projektu wraca do domyślnej.
- `$` na każdym wierszu listy przełącza billable zapisanego wpisu (`PATCH`),
  z optymistycznym odświeżeniem UI i cofnięciem przy odmowie.
- **Brak uprawnienia** `edit_billable_own_timesheet` (domyślnie ma je dopiero teamlead):
  Kimai odrzuca **cały** request z 400 „This form should not contain extra fields.”.
  Wtedy: wpis wysyłany ponownie bez `billable`, przełącznik blokowany i przyciemniony
  z wyjaśnieniem (`errBillableDenied`), blokada trwa do ponownego zapisania ustawień.

Źródło: `api.js#isBillableRejected`, `popup.js#lockBillable`, `#billableButton`.

## F-10 Wznawianie wpisu

- ▶ na wierszu kopiuje opis, projekt, czynność i **billable tego wpisu** (nie domyślne
  projektu) do formularza i startuje.
- Jeśli coś trwa — najpierw zatrzymuje bieżący wpis (przełączenie timera).
- Ukryta czynność (np. kubełek importu z Togglа) nie jest ustawiana, bo nie ma jej na liście.

Źródło: `popup.js#resume`.

## F-11 Walidacja jakości opisu

- `minDescription <= 0` → wyłączona.
- Opis z **linkiem** (`http(s)://`), **numerem zgłoszenia** (`#412`) lub **kluczem**
  (`PROJ-88`) i ≥ 3 znakami → zawsze OK.
- Po normalizacji (małe litery, bez diakrytyków, bez interpunkcji na brzegach) opis z listy
  ogólników (`poprawki`, `spotkanie`, `fixes`, `call`, `bug fixing`… — ok. 90 fraz PL/EN)
  → błąd `generic`.
- Krótszy niż minimum → błąd `short`.

Źródło: `lib/validate.js` (pełna lista ogólników tam).

## F-12 Sumy dzienna i tygodniowa

- Jedno zapytanie: `GET /api/timesheets?begin=<pon 00:00>&end=<dziś 23:59:59>&size=100&page=N`,
  maks. 3 strony; 404 za ostatnią stroną = koniec.
- Liczone **tylko zamknięte** wpisy (`end != null`), trwający dodawany na żywo co sekundę.
- Tydzień od poniedziałku (wtyczka). **W aplikacji:** od dnia z preferencji konta Kimai
  `first_weekday` (domyślnie poniedziałek), tak jak w widokach tygodniowych Kimai.
- Błąd → sumy ukryte (nie blokuje reszty okna).

Źródło: `popup.js#renderTotals`, `api.js#range`.

**Różnice w aplikacji** (poprawki z recenzji, zadanie 0019):

- Stronicowanie: **500 wpisów na stronę** (maksimum Kimai), **do 10 stron**; liczba stron z
  nagłówka `X-Total-Pages` (sprawdzone na Kimai 2.65/2.67), 404 za ostatnią stroną tylko jako
  zabezpieczenie. Wtyczka: 100 × 3 strony, więc przy > 300 wpisach w tygodniu zaniżała sumę.
- Trwający wpis jest doliczany **do dnia, w którym się zaczął** — do „Dziś” tylko, gdy zaczął
  się dziś, do „Tydzień” tylko, gdy zaczął się w tym tygodniu. Tak liczy Kimai, więc po
  zatrzymaniu godziny nie przeskakują między dniami (wtyczka dodawała cały czas do dziś).
- Gdy zmieni się zestaw trwających wpisów (np. stop we wtyczce lub w panelu Kimai), lekkie
  odświeżenie co minutę dociąga też sumy.

## F-13 Język interfejsu

- `auto` (język systemu), `pl`, `en`. Braki w tłumaczeniu uzupełniane angielskim.
- Wybór jawny w ustawieniach, bo zespół chce wybierać niezależnie od systemu.

Źródło: `lib/i18n.js`, `_locales/*/messages.json`.

**W aplikacji (wymóg 1.0, potwierdzony przez użytkownika 2026-09-25): pełna wersja
polska i angielska.**

| Element | Jak tłumaczymy |
| --- | --- |
| Okno, menu tacki, tooltip, ustawienia, komunikaty błędów, powiadomienia N-01…N-03 | własne teksty w `core/i18n` — pliki PL i EN, klucze przeniesione z `_locales` wtyczki i uzupełnione o nowe (menu, powiadomienia, autostart) |
| Standardowe elementy Qt (przyciski „OK/Anuluj”, menu kontekstowe pól tekstowych) | `QTranslator` z `qtbase_<lang>.qm` z katalogu tłumaczeń Qt. Runtime `org.kde.Platform` 6.11 zawiera `translations/qtbase_pl.qm` (sprawdzone 2026-09-25) |
| Nazwy dni i daty na liście wpisów | locale wybranego języka (`QLocale`) |
| Plik `.desktop` (nazwa, komentarz) | klucze `Name[pl]`, `Comment[pl]` |
| MetaInfo (AppStream: opis, podsumowanie) | `xml:lang="pl"` |

Zasady:

- **Każdy tekst widoczny dla użytkownika idzie przez `t(klucz)`.** Żadnych napisów
  wpisanych na sztywno w kodzie UI.
- Test pilnuje, że zestawy kluczy PL i EN są identyczne, a wszystkie klucze użyte
  w kodzie istnieją.
- Zmiana języka w ustawieniach działa od razu, bez restartu (przebudowa tekstów okna,
  menu i tooltipa).

## F-14 Obsługa błędów

| Sytuacja | Komunikat |
| --- | --- |
| Brak połączenia (status 0) | `errConnection` |
| 401 | `errAuth` — token odrzucony lub wygasł |
| 403 | `errForbidden` — wpis zablokowany (np. wyeksportowany) lub brak uprawnień. **Różnica względem wtyczki:** wtyczka traktowała 403 jak zły token |
| 200 bez JSON-a Kimai | `errUnexpected` — np. strona logowania Wi-Fi |
| 3xx (przekierowanie) | `errRedirect` z nowym adresem Kimai (np. `https://…` zamiast `http://…`) |
| 400 z treścią | `errRejected` + **treść błędu z Kimai** (zebrane `errors` z zagnieżdżonych `children` formularza) |
| inne | `errServer` + kod |

Treść nie-JSON przycinana do 200 znaków (bez stack trace'ów w oknie).
Źródło: `api.js#readError`, `#collectFormErrors`, `popup.js#describeError`.

---

## Funkcje nowe względem wtyczki (kandydaci)

| Id | Funkcja | Uzasadnienie | Status |
| --- | --- | --- | --- |
| F-20 | Menu kontekstowe ikony (prawy klik): stop, wznów ostatni, otwórz okno, otwórz Kimai, ustawienia, zakończ | menu rysuje host tacki, więc zawsze jest przy ikonie | **w 1.0** ([ADR-0005](../decyzje/0005-okno-przy-tacce-na-kde.md)); menu rysuje Plasma z dbusmenu — sprawdzone |
| F-21 | Powiadomienia systemowe (portal Notification) | przypomnienie o długim timerze, problemy z połączeniem | **w 1.0** (szczegóły w specyfikacji) |
| F-22 | Autostart z sesją (portal Background, opcja w ustawieniach) | aplikacja tackowa powinna startować sama | **w 1.0** |
| F-23 | Wykrywanie bezczynności | propozycja odjęcia czasu nieaktywności; trudne w Flatpaku na Waylandzie (brak portalu czasu bezczynności) | później |
| F-24 | Globalny skrót klawiszowy (portal GlobalShortcuts) | start/stop bez myszy | później |

## F-21 Powiadomienia — szczegóły (1.0)

Przez portal Notification (w Qt/PySide przez D-Bus). Ustalone z użytkownikiem 2026-09-25.

| Id | Kiedy | Treść | Akcje | Ustawienie |
| --- | --- | --- | --- | --- |
| N-01 Długi timer | trwający wpis przekroczył próg | „Timer działa od 8:00 h — *Projekt*” + opis | **Zatrzymaj**, **Działa dalej** (wycisza do następnego progu: +1 h) | próg w godzinach, domyślnie 8, 0 = wyłączone |
| N-02 Utrata połączenia | 3 kolejne nieudane odświeżenia (~3 min) albo 401/403 | „Brak połączenia z Kimai” / „Token nieważny lub wygasł” | **Ustawienia** (przy 401) | wł./wył., domyślnie wł. |
| N-02b Powrót połączenia | pierwsze udane odświeżenie po N-02 | „Połączenie z Kimai przywrócone” | — | razem z N-02 |
| N-03 Potwierdzenie z menu | start/stop/wznów wykonane **z menu kontekstowego** | „Start: *opis* — *Projekt*” / „Stop: *1:22* — *Projekt*” | — | wł./wył., domyślnie wł. |

Zasady:

- Jedno powiadomienie na zdarzenie. N-02 nie powtarza się co minutę, dopóki trwa ta sama
  awaria. N-01 zastępuje poprzednie **dla tego samego wpisu** (`id` = `long-timer-<nr wpisu>`);
  przycisk „Zatrzymaj” działa na wpis wskazany w powiadomieniu (`entry_id`).
- Akcje z okna aplikacji (nie z menu) nie wysyłają N-03, bo wynik widać w oknie.
- Brak portalu lub odmowa → funkcja cicho wyłączona, informacja w ustawieniach.

Odrzucone na 1.0: „brak timera w godzinach pracy” (wymaga ustawień godzin pracy).

## Powiązane

- [Przegląd projektu](przeglad.md)
- [Kimai REST API](../integracje/kimai-api.md)
- [WS Tracker](../integracje/kimai-ws-tracker.md)
