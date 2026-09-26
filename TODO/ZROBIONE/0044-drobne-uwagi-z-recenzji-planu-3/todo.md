---
noteId: "b47deee8d3894b82b70e2645272acff3"
tytul: "Drobne uwagi z recenzji Planu 3 (ui)"
numer: "0044"
status: zrobione
priorytet: p3
tags: [todo, ui, recenzja]
zalezy_od: ["0041"]
utworzono: 2026-09-26 09:59
zaktualizowano: 2026-09-26 10:14
zamknieto: 2026-09-26 10:14
---

# 0044 — Drobne uwagi z recenzji Planu 3 (ui)

> [!info] Status
> **zrobione** · priorytet **p3** · [← tablica zadań](../../README.md)

## Cel

Zdecydować z użytkownikiem, które drobne uwagi z końcowej recenzji Planu 3 poprawić. Recenzja: model opus,
commity `5bda209..fd3c4be`, 0 krytycznych, 5 ważnych (poprawione: I1–I5, commity `e8c5e6d` i wcześniejsze), 12 drobnych.

## Kontekst

- [Plan 3](../../../docs/plany/2026-09-25-plan-3-ui.md), kod: [src/kimai_tray/ui/](../../../src/ws_tracker_tray/ui/)

## Kryteria akceptacji

- [x] Każda uwaga: poprawiona (test RED→GREEN), odłożona do Planu 4 albo odrzucona z uzasadnieniem

## Kroki (uwagi odłożone)

- [x] **M1** Drugi zielony komunikat „Zapisano” w ciągu minuty nie pojawia się; komunikat błędu z trackera wraca przy
  każdym odświeżeniu, aż do następnego udanego odświeżenia. — **poprawione — komunikat przypisany do wyniku akcji
  (`test_every_save_flashes_even_with_the_same_message`)**
- [x] **M2** Zamknięcie aplikacji może zgubić zapis opisu wpisany tuż przed wyjściem. — **poprawione — okno chowane
      najpierw, kolejka Kimai kończona do 5 s (`test_quitting_still_saves_a_description_typed_just_before`)**
- [x] **M3** Lista projektów może zostać stara po szybkim zamknięciu i otwarciu okna. — **poprawione — licznik otwarć
      okna (`test_catalog_answer_after_the_window_closed_does_not_block_the_next_load`)**
- [x] **M4** Kliknięcia w powiadomienia innych aplikacji (portal rozgłasza je do wszystkich) mogą zadziałać u nas
  (np. „Ustawienia”) — przyjmować tylko nasze identyfikatory. — **poprawione — tylko identyfikatory `<rodzaj>.<numer>`
  (`test_clicks_on_other_apps_notifications_are_ignored`)**
- [x] **M5** Jedna instancja: błąd `listen()` kończy aplikację bez słowa; dwa równoczesne starty mogą się oba uruchomić.
      — **poprawione — bez gniazda start z ostrzeżeniem (`test_when_the_socket_cannot_be_opened_the_app_still_starts`);
      wyścig dwóch startów pozostaje — skutek: dwa okna**
- [x] **M6** Pliki motywu: błąd zapisu w `~/.cache` blokuje start; ścieżka ze spacją psuje arkusz stylów (brak
      cudzysłowu w `url()`). — **poprawione — błąd zapisu pomija strzałki, `url("…")` w cudzysłowie**
- [x] **M7** Zapamiętany rozmiar okna nie jest ograniczany do ekranu (po zmianie monitora okno może wyjść poza ekran). —
      **poprawione — rozmiar ograniczony do ekranu (`test_remembered_size_never_exceeds_the_screen`)**
- [x] **M8** Status w tle (portal Background) pokazuje ostatni „Timer …” po zatrzymaniu. — **poprawione — raz „Nic nie
      jest mierzone” po zatrzymaniu (`test_background_status_says_idle_once_after_stop`)**
- [x] **M9** Podpowiedź o braku tacki nie pojawia się, dopóki aplikacja nie jest skonfigurowana. — **poprawione —
      podpowiedź od startu (`test_no_tray_hint_is_shown_before_the_app_is_configured`)**
- [x] **M10** Po zablokowanym portfelu przy starcie „Zapisz” w ustawieniach żąda ponownego wpisania tokenu. —
      **poprawione — puste pole tokenu = token z portfela
      (`test_after_a_locked_wallet_saving_takes_the_token_from_the_wallet`)**
- [x] **M11** Wyszukiwarka projektów: wiersz „+ projekt” pasuje do filtra; filtr O(n²) przy tysiącach projektów;
  projekt trwającego wpisu spoza katalogu znika z pola po przeładowaniu katalogu. — **poprawione — bez wiersza „+
  projekt”, projekt trwającego wpisu zostaje; filtr przy 3000 projektach < 1 s, więc bez przebudowy**
- [x] **M12** Nieaktualne docstringi w `popup.py` i `tray.py` (klik ikony teraz przełącza okno). — **poprawione —
      docstringi `popup.py`, `tray.py`**

## Materiały

## Dziennik

### 2026-09-26

- **09:59** Utworzono z końcowej recenzji Planu 3.
- **10:09** Start: wszystkie uwagi techniczne — poprawiam po kolei (TDD).
- **10:14** Zamknięte: 12/12 poprawione.

## Wynik

Wszystkie 12 uwag poprawione (TDD, test RED→GREEN), 395 testów zielonych. Żadna nie wymagała decyzji użytkownika.
