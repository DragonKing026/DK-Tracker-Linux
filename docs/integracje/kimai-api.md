---
tytul: Kimai REST API
tagi: [integracja, kimai, api, http]
status_integracji: planowana
wersja: Kimai 2.x (dokumentacja 2.67.0; wtyczka deklaruje zgodność z nowoczesnym tokenem Bearer)
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
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
|---|---|---|---|
| GET | `/api/users/me` | test połączenia, alias, `language` | F-01 |
| GET | `/api/timesheets/active` | trwający wpis (lista 0 lub 1 el.) | F-02, F-03 |
| GET | `/api/projects?visible=1&ignoreDates=1` | projekty (z projektami poza oknem dat) | F-06 |
| GET | `/api/customers?visible=1` | flagi billable klientów | F-06, F-09 |
| GET | `/api/activities?visible=1&globals=true[&project={id}]` | czynności projektu + globalne | F-06 |
| GET | `/api/timesheets?size=20&orderBy=begin&order=DESC&full=true` | ostatnie wpisy z rozwiniętymi obiektami | F-08 |
| GET | `/api/timesheets?begin=…&end=…&size=100&page=N` | wpisy tygodnia do sum | F-12 |
| POST | `/api/timesheets` | start: `begin`, `project`, `activity`, `description`, `[billable]` | F-04 |
| PATCH | `/api/timesheets/{id}/stop` | stop „teraz” | F-05 |
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
- Kimai odrzuca początek w przyszłości → start wysyła „teraz − 1 s”.

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
|---|---|---|
| brak odpowiedzi | sieć / DNS / TLS | „brak połączenia z Kimai” |
| 401 / 403 | zły, unieważniony lub wygasły token | „sprawdź token” + link do ustawień |
| 400 | walidacja formularza; treść w `errors` zagnieżdżonych w `children` | pokaż zebrane komunikaty Kimai |
| 400 „This form should not contain extra fields.” po wysłaniu `billable` | brak uprawnienia `edit_billable_own_timesheet` | ponów bez `billable`, zablokuj przełącznik |
| 404 | brak zasobu / koniec stronicowania | zależnie od kontekstu |
| 5xx | błąd serwera | „błąd serwera Kimai (kod)” |

### Uprawnienie `edit_billable_own_timesheet`

Pole `billable` w formularzu API istnieje tylko dla kont z tym uprawnieniem (domyślnie
teamlead i wyżej). Administrator włącza je dla `ROLE_USER` w: **Administracja → Role →
kolumna ROLE_USER → sekcja „Timesheet (own)”**. Szczegóły:
[[docs/architektura/funkcje#F-09 Billable|F-09]].

## Link do panelu

Kimai nie ma trasy bez locale — `/timesheet/` to 404, działa `/{locale}/timesheet/`.
Locale bierzemy z `user.language` (np. z `/api/users/me` albo z wpisów).

## Dokumentacja

- [REST API — start, uwierzytelnienie, formaty](https://www.kimai.org/documentation/rest-api.html)
- [Stronicowanie API](https://www.kimai.org/documentation/api-pagination.html)
- [Tokeny API użytkownika](https://www.kimai.org/documentation/user-api.html)
- [Przykład wywołań w JavaScript](https://www.kimai.org/documentation/api-example-javascript.html)
- [Uprawnienia i role](https://www.kimai.org/documentation/permissions.html)
- Swagger instancji: `https://<kimai-firmy>/api/doc`; demo: [demo.kimai.org/api/doc](https://demo.kimai.org/api/doc)
- Kod źródłowy Kimai: [github.com/kimai/kimai](https://github.com/kimai/kimai)

## Gdzie w kodzie

> [!todo] Uzupełnić po implementacji klienta API.

## Powiązane

- [[docs/integracje/kimai-ws-tracker|WS Tracker — referencyjna implementacja klienta]]
- [[docs/architektura/funkcje|Katalog funkcji]]
- [[docs/integracje/secret-service|Przechowywanie tokenu]]
