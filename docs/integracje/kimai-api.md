---
noteId: "d4ca0ed1ee384a2392516906d96bbf7b"
tytul: Kimai REST API
tags: [integracja, kimai, api, http]
status_integracji: w-uzyciu
wersja: Kimai 2.x — firma 2.65.0; testowane na 2.65.0 i 2.67.0
utworzono: 2026-09-25 17:19
zaktualizowano: 2026-09-25 19:54
---

# Kimai REST API

> [!info] W skrócie
> JSON-owe REST API self-hostowanego Kimai. Jedyne źródło danych aplikacji: wpisy czasu,
> projekty, klienci, czynności, użytkownik.

## Uwierzytelnienie

- Nagłówek przy **każdym** wywołaniu: `Authorization: Bearer <token>`
  ([źródło](https://www.kimai.org/documentation/rest-api.html)).
- Token tworzy każdy użytkownik sam: **Profil → API**. Użytkownik może mieć wiele tokenów;
  token ma nazwę, **opcjonalną datę wygaśnięcia** i znacznik ostatniego użycia.
- Token jest **pokazywany tylko raz** — zaraz po utworzeniu.
- Token ≠ hasło logowania; można go w każdej chwili unieważnić.
- Wymagane **HTTPS**.
- Stara para nagłówków `X-AUTH-USER` / `X-AUTH-TOKEN` jest przestarzała (wtyczka podaje,
  że Kimai 2.65 ją oznacza jako deprecated i limituje) — **nie wspieramy jej**.

> [!warning] Wygasły token
> Ponieważ token może mieć datę wygaśnięcia, 401 w trakcie działania nie musi oznaczać
> błędu konfiguracji. Aplikacja powinna jasno komunikować „token nieważny lub wygasł”
> i prowadzić do ustawień.

## Endpointy używane przez aplikację

Pełna, interaktywna dokumentacja jest na każdej instancji pod **`/api/doc`**
(np. `https://<kimai-firmy>/api/doc`) — to wiążące źródło dla naszej wersji serwera.

| Metoda | Ścieżka | Po co | Funkcja |
| --- | --- | --- | --- |
| GET | `/api/users/me` | test połączenia, alias, `language` | F-01 |
| GET | `/api/timesheets/active` | trwający wpis (lista 0 lub 1 el.) | F-02, F-03 |
| GET | `/api/projects?visible=1&ignoreDates=1` | projekty (z projektami poza oknem dat) | F-06 |
| GET | `/api/customers?visible=1` | flagi billable klientów | F-06, F-09 |
| GET | `/api/activities?visible=1&globals=true[&project={id}]` | czynności projektu + globalne | F-06 |
| GET | `/api/timesheets?size=20&orderBy=begin&order=DESC&full=true` | ostatnie wpisy z rozwiniętymi obiektami | F-08 |
| GET | `/api/timesheets?begin=…&end=…&size=100&page=N` | wpisy tygodnia do sum | F-12 |
| POST | `/api/timesheets` | start: `begin`, `project`, `activity`, `description`, `[billable]` | F-04 |
| PATCH | `/api/timesheets/{id}/stop` | stop „teraz”; na już zatrzymanym wpisie zwraca 200 (sprawdzone) | F-05 |
| PATCH | `/api/timesheets/{id}` | częściowa edycja: `description`, `begin`, `end`, `billable` | F-05, F-07, F-09 |

> [!tip] Dlaczego nie `/api/timesheets/recent`
> Ten endpoint zwija listę do jednej pozycji na parę projekt+czynność. Dzień spędzony nad
> jednym projektem wygląda jak jeden wiersz. Używamy zwykłej kolekcji z `full=true`.

## Format dat

- API **zwraca** ISO 8601 ze strefą.
- API **oczekuje** w POST/PATCH formatu HTML5 „local date and time”:
  **`YYYY-MM-DDTHH:mm:ss`** bez strefy — tylko ten format jest gwarantowany na przyszłość
  ([źródło](https://www.kimai.org/documentation/rest-api.html)).
- Czas interpretowany jest w strefie użytkownika Kimai → wysyłamy lokalny czas ścienny.
- Start wysyła „teraz − 1 s” (tak robi wtyczka). Odrzucanie przyszłego początku zależy
  jednak od ustawienia serwera: na domyślnym Kimai 2.67 początek +2 h został **przyjęty**
  ([raport](../../TODO/ZROBIONE/0002-specyfikacja-projektu/testy/raport-kimai-docker-2026-09-25.md)).

## Stronicowanie

([źródło](https://www.kimai.org/documentation/api-pagination.html))

- Parametry `page` i `size` (domyślnie 50, **maks. 500**).
- Nagłówki odpowiedzi: `X-Page`, `X-Total-Count`, `X-Total-Pages`, `X-Per-Page`.
- Za ostatnią stroną Kimai zwraca **404** zamiast pustej listy (obserwacja z wtyczki) —
  przy iteracji traktujemy 404 na stronie > 1 jako koniec.

> [!tip] Usprawnienie względem wtyczki
> Wtyczka pobiera sumy tygodnia do 3 stron po 100. Możemy użyć `X-Total-Pages`
> albo `size` do 500, żeby nie zgadywać liczby stron.

## Błędy

| Kod | Znaczenie | Reakcja |
| --- | --- | --- |
| brak odpowiedzi | sieć / DNS / TLS | „brak połączenia z Kimai” |
| 401 | zły, unieważniony lub wygasły token (**pusta treść** — sprawdzone) | „token odrzucony lub wygasł” + link do ustawień |
| 403 `Forbidden` | token działa, ale akcja jest zabroniona: edycja **wpisu wyeksportowanego**, cudzego wpisu, brak uprawnienia (sprawdzone na 2.65.0) | „Kimai nie pozwala na tę zmianę” (`errForbidden`); wpisy z `exported: true` UI blokuje z góry |
| 400 | walidacja formularza; treść w `errors` zagnieżdżonych w `children` | pokaż zebrane komunikaty Kimai |
| 400 „This form should not contain extra fields.” po wysłaniu `billable` | brak uprawnienia `edit_billable_own_timesheet` | ponów bez `billable`, zablokuj przełącznik |
| 3xx z `Location` | Kimai jest pod innym adresem (np. `http://` → `https://`, nowa domena) | „Kimai przekierowuje na …” (`errRedirect`) z adresem bazowym; **nie podążamy** za przekierowaniem, żeby nie wysyłać tokenu ponownie |
| 404 | brak zasobu / koniec stronicowania (`{"code":404,"message":"Not Found"}` — sprawdzone) | zależnie od kontekstu |
| 400 „You have an active time record which cannot be stopped automatically.” | start przy trwającym wpisie, którego nie da się zamknąć (np. jego początek jest w przyszłości przez złą strefę) | komunikat + odświeżenie; sprawdź strefę czasową |
| 400 „The end date must not be earlier than the start date.” | stop/edycja z końcem przed początkiem | komunikat Kimai; typowy objaw złej strefy |
| 5xx | błąd serwera | „błąd serwera Kimai (kod)” |

### Uprawnienie `edit_billable_own_timesheet`

Pole `billable` w formularzu API istnieje tylko dla kont z tym uprawnieniem (domyślnie
teamlead i wyżej). Administrator włącza je dla `ROLE_USER` w: **Administracja → Role →
kolumna ROLE_USER → sekcja „Timesheet (own)”**. Szczegóły:
[F-09](../architektura/funkcje.md).

## Wersja Kimai firmy

**Kimai firmy: 2.65.0** (podane przez użytkownika 2026-09-25 19:26). Zweryfikowano na obrazie
`kimai/kimai2:2.65.0` w Dockerze: testy kontraktowe rdzenia 8/8, `/api/users/me` zwraca pole
`timezone` (oraz `language`, `locale`, listę `preferences` bez strefy — m.in.
`first_weekday: monday`). Testy na tej wersji: `KIMAI_VERSION=2.65.0 tests/kimai/kimai-testowe.sh up`.

> [!note] Strefa czasowa w starszych wersjach
> Gdy odpowiedź nie ma pola `timezone`, rdzeń szuka `preferences[name=timezone]`; gdy i tam
> brak — używa strefy komputera i pokazuje ostrzeżenie `warnTimezoneMissing` (nigdy nie
> zakłada UTC).

<!-- osobne callouty -->

> [!note] Początek tygodnia
> Preferencja `first_weekday` (np. `monday` / `sunday`) ustala początek tygodnia konta.
> Rdzeń liczy sumy tygodnia od tego dnia (`User.first_weekday`, domyślnie poniedziałek).

## Ustawienia serwera, które zmieniają zachowanie API

Z [dokumentacji konfiguracji](https://www.kimai.org/documentation/configurations.html)
(Ustawienia → Timesheet). Administrator może je zmienić, więc aplikacja nie może
zakładać wartości domyślnych:

| Ustawienie | Domyślnie | Skutek dla aplikacji |
| --- | --- | --- |
| Dozwolona liczba jednocześnie trwających wpisów | `1` — start nowego **automatycznie zatrzymuje** trwający (sprawdzone: 200, poprzedni wpis dostaje `end`) | przy `> 1` start może zostać odrzucony po osiągnięciu limitu, a `/active` może zwrócić kilka wpisów |
| Maksymalny czas trwania wpisu | wyłączone (0) | przy włączonym limicie **stop lub edycja mogą zostać odrzucone** (400) |
| Nakładające się wpisy | dozwolone | przy wyłączeniu edycja początku/końca może zostać odrzucona (400) |
| Wpisy w przyszłości | — | przyszła godzina początku jest odrzucana |

## Strefa czasowa

Z [preferencji użytkownika](https://www.kimai.org/documentation/user-preferences.html)
i [REST API](https://www.kimai.org/documentation/rest-api.html):

- Każdy użytkownik Kimai ma **własną strefę czasową** (domyślnie strefę serwera, która
  „często jest błędna”).
- API zwraca daty w ISO 8601 z przesunięciem strefy użytkownika.
- W POST/PATCH Kimai traktuje podaną godzinę jako lokalną i **dokleja strefę
  użytkownika bez przeliczania**.
- `GET /api/users/me` zwraca strefę w polu **`timezone`** (np. `"UTC"`) i język w polu
  `language` — sprawdzone na Kimai 2.67.0.
- **Sprawdzone na żywo**
  ([raport](../../TODO/ZROBIONE/0002-specyfikacja-projektu/testy/raport-kimai-docker-2026-09-25.md)): konto Kimai w UTC,
  system w Europe/Warsaw.
  Wysłanie „teraz” w czasie systemu dało wpis **2 h w przyszłości**. Stop został
  odrzucony („end date must not be earlier than the start date”), następny start też
  („active time record which cannot be stopped automatically”).
- Zasada w aplikacji: **wszystkie godziny wysyłane do Kimai liczymy w strefie
  `/api/users/me → timezone`**. Przy różnicy stref pokazujemy ostrzeżenie.
- Kimai **zaokrągla** czasy do pełnych minut przy stopie i auto-stopie (ustawienie
  serwera) — nie porównujemy czasów co do sekundy.

## Link do panelu

Kimai nie ma trasy bez locale — `/timesheet/` to 404, działa `/{locale}/timesheet/`.
Locale bierzemy z `user.language` (np. z `/api/users/me` albo z wpisów).

## Dokumentacja

- [REST API — start, uwierzytelnienie, formaty](https://www.kimai.org/documentation/rest-api.html)
- [Stronicowanie API](https://www.kimai.org/documentation/api-pagination.html)
- [Tokeny API użytkownika](https://www.kimai.org/documentation/user-api.html)
- [Przykład wywołań w JavaScript](https://www.kimai.org/documentation/api-example-javascript.html)
- [Uprawnienia i role](https://www.kimai.org/documentation/permissions.html)
- [Konfiguracja (Timesheet)](https://www.kimai.org/documentation/configurations.html)
- [Preferencje użytkownika — strefa czasowa](https://www.kimai.org/documentation/user-preferences.html)
- Swagger instancji: `https://<kimai-firmy>/api/doc`; demo: [demo.kimai.org/api/doc](https://demo.kimai.org/api/doc)
- Kod źródłowy Kimai: [github.com/kimai/kimai](https://github.com/kimai/kimai)

## Gdzie w kodzie

- [src/kimai_tray/core/kimai_client.py](../../src/kimai_tray/core/kimai_client.py) — `KimaiClient`
  (wszystkie endpointy z tabeli powyżej, stronicowanie `range`).
- [src/kimai_tray/core/errors.py](../../src/kimai_tray/core/errors.py) — `ApiError`, zbieranie błędów formularza.
- Testy: [tests/core/test_kimai_client.py](../../tests/core/test_kimai_client.py) (MockTransport).

## Powiązane

- [WS Tracker — referencyjna implementacja klienta](kimai-ws-tracker.md)
- [Katalog funkcji](../architektura/funkcje.md)
- [Przechowywanie tokenu](secret-service.md)
