---
noteId: "acc7e900dc6845bba975f1f477ab6319"
tytul: "Poprawki UI po teście na żywo (Plan 3)"
numer: "0042"
status: w-trakcie
priorytet: p1
tags: [todo, plan-3, ui, poprawki]
zalezy_od: ["0040"]
utworzono: 2026-09-25 23:34
zaktualizowano: 2026-09-25 23:34
---

# 0042 — Poprawki UI po teście na żywo (Plan 3)

> [!info] Status
> **w-trakcie** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Poprawić to, co użytkownik znalazł w teście na żywo ([0041](../0041-plan3-test-na-zywo/todo.md)),
każdą zmianę kodu metodą TDD, a potem wrócić do listy kontrolnej.

## Kontekst

- [Plan 3](../../../docs/plany/2026-09-25-plan-3-ui.md), [wzorzec wtyczki](../../../docs/integracje/kimai-ws-tracker.md)
- Przyczyna punktów 2, 8, 10: proces uruchomiony z terminala VS Code jest w jego grupie systemd
  (`app-com.microsoft.VSCode-….scope`), więc portal przypisuje powiadomienia VS Code, a kompozytor
  nie zna ikony aplikacji. Na hoście portal ma do tego `org.freedesktop.host.portal.Registry.Register`
  (xdg-desktop-portal 1.22.1 na Fedorze 44, wersja interfejsu 1).
- Logo: [dane/kimai-logo-512.png](dane/kimai-logo-512.png) — `public/touch-icon-512x512.png` z obrazu `kimai/kimai2:2.67.0`
  (projekt Kimai, licencja AGPL-3.0-or-later), na prośbę użytkownika jako ikona aplikacji.

## Kryteria akceptacji

- [ ] Każdy punkt poniżej: poprawiony (test RED→GREEN, jeśli dotyczy kodu) albo wyjaśniony z użytkownikiem
- [ ] Pełny `pytest` zielony, `ruff` bez uwag
- [ ] Ponowny test na żywo punktów z tej listy

## Kroki (uwagi użytkownika, 2026-09-25 23:34)

- [ ] 1. Ucięty tekst podpowiedzi w oknie ustawień („0 wyłącza sprawdzanie. Zalecane 15.”)
- [ ] 2. Ikona Kimai na początku nagłówka okna i jako ikona aplikacji (zamiast „W” Waylanda w oknie ustawień i na pasku zadań)
- [ ] 3. Wyszukiwanie na liście projektów (poza wtyczką — ułatwienie przy wielu projektach)
- [ ] 4. Ostrzeżenie o strefie czasowej w Dockerze — konta testowe mają UTC; ustawić im strefę komputera
- [ ] 5. Wygładzić strzałki list rozwijanych i przewijania
- [ ] 6. Przyciski `$` mało wyróżnione
- [ ] 7. Odstęp między tekstem a brzegiem w ikonie tacki; drugie kliknięcie ikony powinno zamykać okno
- [ ] 8. Brak powiadomień (start/stop z menu)
- [ ] 9. Lista wpisów wyższa i możliwość zmiany rozmiaru okna przez użytkownika
- [ ] 10. „Zatrzymaj” w powiadomieniu powinno je zamknąć; powiadomienie przedstawia się jako VS Code
- [ ] 11. Ramka okna ustawień miga po schowaniu i przywróceniu z paska zadań

## Materiały

- [dane/kimai-logo-512.png](dane/kimai-logo-512.png) — logo Kimai (AGPL-3.0-or-later)

## Dziennik

### 2026-09-25
- **23:34** Utworzono z uwag użytkownika po teście na żywo.
