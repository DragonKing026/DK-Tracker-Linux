---
noteId: "acc7e900dc6845bba975f1f477ab6319"
tytul: "Poprawki UI po teście na żywo (Plan 3)"
numer: "0042"
status: zrobione
priorytet: p1
tags: [todo, plan-3, ui, poprawki]
zalezy_od: ["0040"]
utworzono: 2026-09-25 23:34
zaktualizowano: 2026-09-26 00:47
zamknieto: 2026-09-26 00:47
---

# 0042 — Poprawki UI po teście na żywo (Plan 3)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Poprawić to, co użytkownik znalazł w teście na żywo ([0041](../0041-plan3-test-na-zywo/todo.md)),
każdą zmianę kodu metodą TDD, a potem wrócić do listy kontrolnej.

## Kontekst

- [Plan 3](../../../docs/plany/2026-09-25-plan-3-ui.md), [wzorzec wtyczki](../../../docs/integracje/kimai-ws-tracker.md)
- Przyczyna punktów 2, 8, 10: proces uruchomiony z terminala VS Code jest w jego grupie systemd
  (`app-com.microsoft.VSCode-….scope`), więc portal przypisuje powiadomienia VS Code, a kompozytor
  nie zna ikony aplikacji. Na hoście portal ma do tego `org.freedesktop.host.portal.Registry.Register`
  (xdg-desktop-portal 1.22.1 na Fedorze 44, wersja interfejsu 1).
- Logo: [dane/kimai-logo-512.png](dane/kimai-logo-512.png) — `public/touch-icon-512x512.png` z obrazu
  `kimai/kimai2:2.67.0`
  (projekt Kimai, licencja AGPL-3.0-or-later), na prośbę użytkownika jako ikona aplikacji.

## Kryteria akceptacji

- [x] Każdy punkt poniżej: poprawiony (test RED→GREEN, jeśli dotyczy kodu) albo wyjaśniony z użytkownikiem
- [x] Pełny `pytest` zielony, `ruff` bez uwag
- [x] Ponowny test na żywo punktów z tej listy

## Kroki (uwagi użytkownika, 2026-09-25 23:34)

- [x] 1. Ucięty tekst podpowiedzi w oknie ustawień („0 wyłącza sprawdzanie. Zalecane 15.”)
- [x] 2. Ikona Kimai na początku nagłówka okna i jako ikona aplikacji (zamiast „W” Waylanda w oknie ustawień i na pasku
      zadań)
- [x] 3. Wyszukiwanie na liście projektów (poza wtyczką — ułatwienie przy wielu projektach)
- [x] 4. Ostrzeżenie o strefie czasowej w Dockerze — konta testowe mają UTC; ustawić im strefę komputera
- [x] 5. Wygładzić strzałki list rozwijanych i przewijania
- [x] 6. Przyciski `$` mało wyróżnione
- [x] 7. Odstęp między tekstem a brzegiem w ikonie tacki; drugie kliknięcie ikony powinno zamykać okno
- [x] 8. Brak powiadomień (start/stop z menu)
- [x] 9. Lista wpisów wyższa i możliwość zmiany rozmiaru okna przez użytkownika
- [x] 10. „Zatrzymaj” w powiadomieniu powinno je zamknąć; powiadomienie przedstawia się jako VS Code
- [x] 11. Ramka okna ustawień miga po schowaniu i przywróceniu z paska zadań

## Materiały

- [dane/kimai-logo-512.png](dane/kimai-logo-512.png) — logo Kimai (AGPL-3.0-or-later)

## Dziennik

### 2026-09-25

- **23:34** Utworzono z uwag użytkownika po teście na żywo.

### 2026-09-26

- **00:47** Zamknięte: wszystkie uwagi potwierdzone na żywo.

## Wynik

Wszystkie uwagi potwierdzone przez użytkownika na żywo (KDE Plasma 6.7.5, Kimai 2.67 w Dockerze):

| Nr | Poprawka | Test |
| --- | --- | --- |
| 1 | Podpowiedzi w ustawieniach w jednej linii, siatka zamiast `QFormLayout` | `test_wrapped_hints_get_the_height_they_need` |
| 2 | Logo Kimai: nagłówek okna, ikona aplikacji (z marginesem), plik `.desktop` + `scripts/instaluj-dev.sh` | `test_app_icon_is_the_kimai_logo`, `test_app_icon_keeps_a_margin_from_the_edge` |
| 3 | Lista projektów z polem wyszukiwania na górze (jak Select2) — [project_picker.py](../../../src/ws_tracker_tray/ui/project_picker.py) | `test_typing_filters_by_project_or_customer_…` i 5 innych |
| 4 | Konto `kierownik` w Dockerze w strefie komputera | testy kontraktowe 9/9 |
| 5 | Gładkie strzałki list, cienkie paski przewijania | `test_combo_arrows_are_drawn_from_our_own_svg` |
| 6 | Wyraźne przyciski `$`, wyśrodkowane w wierszu | `test_billable_states_stand_out`, `test_dot_and_buttons_are_centred_in_the_row` |
| 7 | Odstęp tekstu w ikonie tacki; klik ikony przełącza okno | `test_badge_text_keeps_a_margin_from_the_edge`, `test_tray_click_toggles_the_window` |
| 8, 10 | `Registry.Register` (powiadomienia jako Kimai Tray), nowy identyfikator każdego powiadomienia, kliknięte znika | `test_every_notification_gets_a_fresh_id_…`, `test_a_handled_notification_is_withdrawn` |
| 9 | Uchwyt zmiany rozmiaru, lista na całą wysokość, rozmiar zapamiętany | `test_grip_drag_grows_the_window_up_and_left` |
| 11 | Miganie ramki ustawień — nie występuje w nowej wersji (użytkownik: „już jest ok”) | — |

Decyzja użytkownika: potwierdzenia start/stop tylko dla menu ikony (N-03 jak w specyfikacji), nie dla akcji w oknie.
