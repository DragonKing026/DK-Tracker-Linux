---
noteId: "b47deee8d3894b82b70e2645272acff3"
tytul: "Drobne uwagi z recenzji Planu 3 (ui)"
numer: "0044"
status: do-zrobienia
priorytet: p3
tags: [todo, ui, recenzja]
zalezy_od: ["0041"]
utworzono: 2026-09-26 09:59
zaktualizowano: 2026-09-26 09:59
---

# 0044 — Drobne uwagi z recenzji Planu 3 (ui)

> [!info] Status
> **do-zrobienia** · priorytet **p3** · [← tablica zadań](../../README.md)

## Cel

Zdecydować z użytkownikiem, które drobne uwagi z końcowej recenzji Planu 3 poprawić. Recenzja: model opus,
commity `5bda209..fd3c4be`, 0 krytycznych, 5 ważnych (poprawione: I1–I5, commity `e8c5e6d` i wcześniejsze), 12 drobnych.

## Kontekst

- [Plan 3](../../../docs/plany/2026-09-25-plan-3-ui.md), kod: [src/kimai_tray/ui/](../../../src/kimai_tray/ui/)

## Kryteria akceptacji

- [ ] Każda uwaga: poprawiona (test RED→GREEN), odłożona do Planu 4 albo odrzucona z uzasadnieniem

## Kroki (uwagi odłożone)

- [ ] **M1** Drugi zielony komunikat „Zapisano” w ciągu minuty nie pojawia się; komunikat błędu z trackera wraca przy
  każdym odświeżeniu, aż do następnego udanego odświeżenia.
- [ ] **M2** Zamknięcie aplikacji może zgubić zapis opisu wpisany tuż przed wyjściem.
- [ ] **M3** Lista projektów może zostać stara po szybkim zamknięciu i otwarciu okna.
- [ ] **M4** Kliknięcia w powiadomienia innych aplikacji (portal rozgłasza je do wszystkich) mogą zadziałać u nas
  (np. „Ustawienia”) — przyjmować tylko nasze identyfikatory.
- [ ] **M5** Jedna instancja: błąd `listen()` kończy aplikację bez słowa; dwa równoczesne starty mogą się oba uruchomić.
- [ ] **M6** Pliki motywu: błąd zapisu w `~/.cache` blokuje start; ścieżka ze spacją psuje arkusz stylów (brak
      cudzysłowu w `url()`).
- [ ] **M7** Zapamiętany rozmiar okna nie jest ograniczany do ekranu (po zmianie monitora okno może wyjść poza ekran).
- [ ] **M8** Status w tle (portal Background) pokazuje ostatni „Timer …” po zatrzymaniu.
- [ ] **M9** Podpowiedź o braku tacki nie pojawia się, dopóki aplikacja nie jest skonfigurowana.
- [ ] **M10** Po zablokowanym portfelu przy starcie „Zapisz” w ustawieniach żąda ponownego wpisania tokenu.
- [ ] **M11** Wyszukiwarka projektów: wiersz „+ projekt” pasuje do filtra; filtr O(n²) przy tysiącach projektów;
  projekt trwającego wpisu spoza katalogu znika z pola po przeładowaniu katalogu.
- [ ] **M12** Nieaktualne docstringi w `popup.py` i `tray.py` (klik ikony teraz przełącza okno).

## Materiały

## Dziennik

### 2026-09-26

- **09:59** Utworzono z końcowej recenzji Planu 3.
