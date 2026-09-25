---
noteId: "25e094032a874be099086c112845caf1"
tytul: "Raport: Kimai w Dockerze — weryfikacja zachowań API"
tags: [testy, kimai, docker, spike]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
---

# Raport: Kimai w Dockerze — weryfikacja zachowań API (2026-09-25)

Spike do [zadania 0002](../todo.md), sekcja 4 projektu (testy). Pytanie użytkownika:
czy do testów można lokalnie uruchomić Kimai w Dockerze? **Odpowiedź: tak.** Po drodze
zweryfikowano zachowania API, na których opiera się aplikacja.

## Środowisko

| | |
|---|---|
| Obraz | `kimai/kimai2:apache` → **Kimai 2.67.0** (env: prod) + `mysql:8.3` |
| Compose | [prototyp/kimai-docker/docker-compose.yml](../prototyp/kimai-docker/docker-compose.yml) |
| Skrypty | [probe.py](../prototyp/kimai-docker/probe.py), [probe_teamlead.py](../prototyp/kimai-docker/probe_teamlead.py) |
| Host | Fedora 44, Docker 29.8.1, Compose 5.5.1; strefa systemu Europe/Warsaw |
| Czas uruchomienia | ok. 1 min (pobranie obrazów przy pierwszym razie dłużej) |

## Jak utworzyć użytkowników i tokeny bez klikania

1. Admin z `ADMINMAIL`/`ADMINPASS` powstaje przy starcie kontenera.
2. Kolejni użytkownicy: `bin/console kimai:user:create <login> <email> <ROLA> <hasło>`.
3. **Kimai nie ma komendy konsoli do tokenów API**, ale przechowuje token **jawnie**
   w tabeli `kimai2_access_token` i szuka go po dokładnej wartości
   (`AccessTokenHandler` → `AccessTokenRepository::findByToken`). Wystarczy więc:

```sql
INSERT INTO kimai2_access_token (user_id, token, name)
SELECT id, 'test-user-token-0123456789', 'tests' FROM kimai2_users WHERE username = 'jan';
```

To szczegół implementacji Kimai. Może się zmienić w przyszłej wersji, dlatego test
środowiska sprawdza, że token działa (`GET /api/users/me` → 200).

## Wyniki

| # | Sprawdzenie | Wynik | Plik |
|---|---|---|---|
| 1 | ROLE_USER wysyła `billable` | **400** `This form should not contain extra fields.` — cały request odrzucony | [wynik 3](wynik-probe-3.txt) |
| 2 | ROLE_TEAMLEAD wysyła `billable=false`, potem PATCH `true` | 200 / 200 — przełącznik działa | [teamlead](wynik-probe-teamlead.txt) |
| 3 | `/api/users/me` zawiera strefę | **tak: pole `timezone`** (tu `UTC`) oraz `language` | [wynik 3](wynik-probe-3.txt) |
| 4 | Start z czasem systemu (Warszawa), gdy konto Kimai ma UTC | wpis **2 h w przyszłości**; stop → 400 „end date must not be earlier than the start date”; następny start → 400 „active time record which cannot be stopped automatically” | [wynik 1](wynik-probe-1.txt), [wynik 2](wynik-probe-2.txt) |
| 5 | Start w strefie konta Kimai | poprawny | [wynik 3](wynik-probe-3.txt) |
| 6 | Drugi start przy trwającym wpisie (limit 1) | 200 — poprzedni **zatrzymany automatycznie** | [wynik 3](wynik-probe-3.txt) |
| 7 | Zaokrąglanie | begin/end zaokrąglone do pełnych minut przy auto-stopie i stopie | [wynik 3](wynik-probe-3.txt) |
| 8 | Stop już zatrzymanego wpisu | **200** + wpis (nie błąd) | [wynik 3](wynik-probe-3.txt) |
| 9 | Początek w przyszłości (+2 h) | **200 — przyjęty** (ustawienie serwera, domyślnie dozwolone) | [wynik 3](wynik-probe-3.txt) |
| 10 | Strona za końcem stronicowania | **404** `Not Found`; nagłówki `X-Page`, `X-Total-Count`, `X-Total-Pages`, `X-Per-Page` obecne | [wynik 3](wynik-probe-3.txt) |
| 11 | `full=true` na liście wpisów | `project`, `activity`, `user` jako obiekty; `project.color`, `user.language` dostępne | [wynik 3](wynik-probe-3.txt) |
| 12 | Zły token | **401 z pustą treścią** | [wynik 3](wynik-probe-3.txt) |
| 13 | Billable z klienta | projekt klienta z `billable=false` → wpis `billable: false` | [wynik 3](wynik-probe-3.txt) |

> [!success] Wynik trwały
> Środowisko przeniesione do repozytorium jako [tests/kimai/](../../../../tests/kimai/README.md)
> (skrypt `kimai-testowe.sh up/env/down`, wersja przypięta do 2.67.0). Prototyp poniżej
> zostaje jako zapis spike'a.

## Wnioski dla projektu

- **Strefa czasowa (krytyczne).** Wszystkie godziny wysyłane do Kimai liczymy w strefie
  z `/api/users/me → timezone`, nie w strefie systemu. Przy różnicy stref aplikacja
  pokazuje ostrzeżenie. Wtyczka WS Tracker ma tu błąd dla kont ze strefą ≠ strefie przeglądarki.
- **Wznowienie przy trwającym wpisie:** przy limicie 1 Kimai sam zatrzymuje poprzedni wpis.
  Aplikacja i tak zatrzymuje jawnie (jak wtyczka), bo admin może ustawić limit > 1.
- **„Nieaktualny stop”** nie wymaga specjalnej ścieżki błędu — Kimai odpowiada 200.
- **Przyszły początek** nie jest gwarantowanym błędem. „Teraz − 1 s” zostaje jako
  zabezpieczenie, a walidacja przyszłej godziny w edycji początku zostaje po stronie aplikacji.
- **Środowisko testowe:** Kimai w Dockerze + tokeny wstawiane SQL-em → pełne testy
  kontraktowe (zapis i odczyt) bez prawdziwego Kimai firmy.
