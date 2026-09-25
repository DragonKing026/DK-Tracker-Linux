---
noteId: "3bd05b294c5f44a1b6bd803bbe09249e"
tytul: "Drobne uwagi z recenzji Planu 2 (desktop)"
numer: "0027"
status: zrobione
priorytet: p3
tags: [todo, desktop, recenzja]
zalezy_od: ["0026"]
utworzono: 2026-09-25 21:06
zaktualizowano: 2026-09-25 21:48
zamknieto: 2026-09-25 21:48
---

# 0027 — Drobne uwagi z recenzji Planu 2 (desktop)

> [!info] Status
> **zrobione** · priorytet **p3** · [← tablica zadań](../../README.md)

## Cel

Zdecydować z użytkownikiem, które drobne uwagi z końcowej recenzji Planu 2 poprawić (teraz, w Planie 3
albo wcale). Recenzja: model opus, commity `6ed7042..577cd54`, 0 krytycznych, 1 ważna, 9 drobnych.
Ważną (I1: surowe wyjątki z usługi sekretów, wygasła sesja) poprawiono w commicie `0cbd5e9`.

## Kontekst

- [Plan 2](../../../docs/plany/2026-09-25-plan-2-desktop.md),
  [specyfikacja](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md)
- Kod: [src/kimai_tray/desktop/](../../../src/kimai_tray/desktop/),
  [notification_policy.py](../../../src/kimai_tray/core/notification_policy.py)
- Rozpoznanie API: [rozpoznanie.md](../0021-plan2-rozpoznanie-api-desktop/notatki/rozpoznanie.md)

## Kryteria akceptacji

- [ ] Każda uwaga: poprawiona (test RED→GREEN), przeniesiona do Planu 3 albo świadomie odrzucona z uzasadnieniem w
      dzienniku

## Kroki (uwagi odłożone)

- [x] **M1** `entry_id_from` używa `str.isdigit()` — przepuszcza np. „²”, potem `int()` rzuca `ValueError`.
      Identyfikatory nadajemy sami, więc ryzyko znikome. Poprawka: `re.fullmatch(r"[0-9]+", …)`. — **poprawione**
      (`a8839ca`): `re.fullmatch(r"[0-9]+")`, test `test_entry_id_from_ignores_non_ascii_digits`.
- [x] **M2** `SecretServiceStore.get`: surowy `KeyError`, gdy `GetSecrets` pominie wpis (wyścig z usunięciem), i
      `UnicodeDecodeError` przy sekrecie nie-UTF-8. Poprawka: `.get()` → `None`; błąd dekodowania → `None` albo
      `SecretsUnavailable`. — **poprawione** (`52d9234`): brak wpisu lub sekret nie-UTF-8 → `None` (nowy zapis tokenu go
      zastąpi); testy `test_item_gone_between_search_and_read_is_no_token`, `test_secret_that_is_not_text_is_no_token`.
- [x] **M3** `portal_request` po przekroczeniu czasu nie wywołuje `Request.Close` (okno portalu może zostać) i nie
      porównuje zwróconego uchwytu z oczekiwanym. — **poprawione** (`ee57836`): po limicie czasu `Request.Close` na
      zwróconym uchwycie (błędy zamknięcia pomijane); test `test_portal_request_timeout_closes_the_request`. Porównania
      uchwytu nie dodaję: portale od wersji 0.9 zwracają ścieżkę z naszego `handle_token`, a na Plasmie 6.7 to
      sprawdziliśmy.
- [x] **M4** Po przekroczeniu czasu okna odblokowania portfela nie wołamy `Prompt.Dismiss` — okno zostaje na ekranie. —
      **poprawione** (`52d9234`): po limicie czasu `Prompt.Dismiss`; test `test_unanswered_unlock_prompt_is_dismissed`.
- [x] **M5** `_JeepneyExpectation.close()` nie jest idempotentne — drugie wywołanie rzuca `KeyError` (ważne przy
      zamykaniu w Planie 3). — **poprawione** (`ee57836`): flaga `_closed`; test `test_expectation_close_is_idempotent`
      (fałszywe połączenie jeepney).
- [x] **M6** Odpowiedź na `AddMatch` nie jest sprawdzana — przy błędzie `wait` czeka do końca limitu czasu. —
      **poprawione** (`ee57836`): odpowiedź `AddMatch` sprawdzana (`DBusCallError`); test
      `test_expect_reports_a_refused_subscription`.
- [x] ~~**M7** Reguły dopasowania bez `sender` — dowolny proces sesji może podrobić `ActionInvoked`~~ — **odrzucone z
      notatką** (decyzja użytkownika): proces w sesji, który mógłby podrobić kliknięcie, i tak może odczytać token z
      odblokowanego portfela (Secret Service wydaje sekrety każdemu procesowi sesji) i zmieniać wpisy w Kimai
      bezpośrednio; najgorszy skutek podróbki to zatrzymany timer widoczny w tacce. Gdyby jednak: przy starcie
      `GetNameOwner(org.freedesktop.portal.Desktop)`, reguła z `sender=<unikalna nazwa>`, a na `NameOwnerChanged`
      portalu — ponowna subskrypcja (inaczej po restarcie portalu kliknięcia przestaną działać).
- [x] **Brak domyślnego portfela** (decyzja z recenzji, zatwierdzona przez użytkownika: opcja 1) — `SecretsUnavailable`,
      aplikacja nie zakłada portfela sama (okno z hasłem dla nowego portfela zaskakiwałoby użytkownika). W Planie 3
      komunikat podpowie, jak założyć portfel (Menedżer portfeli KDE / „Hasła i klucze” w GNOME).
- [x] **M8** `listen()` działa na tej samej szynie co `show()` — Plan 3 musi dać nasłuchowi osobne połączenie (jedno na
      wątek) i sprawdzić, czy `ActionInvoked` do niego dociera. — **wyjaśnione** (`f073dca`): w źródle portalu
      `ActionInvoked` jest rozgłaszany bez adresata, więc osobne połączenie nasłuchu zadziała; opis w
      [portale XDG](../../../docs/integracje/xdg-portale.md), potwierdzenie na żywo w Planie 3.
- [x] **M9** Brakujące testy: `get` przy dwóch pasujących wpisach, przekroczenie czasu okna odblokowania, ścieżka `set`
      przy braku usługi. — **uzupełnione** (`52d9234`): `test_get_reads_only_the_first_of_several_matches`,
      `test_unanswered_unlock_prompt_is_dismissed`, `test_missing_service_when_saving_is_unavailable`; `SessionBus` ma
      teraz testy z fałszywym połączeniem.

## Materiały

## Dziennik

### 2026-09-25

- **21:06** Utworzono z końcowej recenzji Planu 2.
- **21:10** Start: techniczne uwagi poprawiam sam, decyzje produktowe do omówienia z użytkownikiem.
- **21:44** M7 odrzucona z notatką (decyzja użytkownika).
- **21:48** Zamknięte: wszystkie uwagi rozstrzygnięte.

## Wynik

M1–M6, M8, M9 poprawione lub uzupełnione testami (RED→GREEN), M7 odrzucona z notatką, brak domyślnego portfela →
komunikat (opcja 1). Testy: 223 zielone + 3 `desktop`.
