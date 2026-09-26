---
noteId: "71460991a53d4e68af031c3926a7fc33"
tytul: "Drobne uwagi z recenzji Planu 4"
numer: "0057"
status: do-zrobienia
priorytet: p3
tags: [todo, plan-4, recenzja]
zalezy_od: []
utworzono: 2026-09-26 12:25
zaktualizowano: 2026-09-26 12:25
zamknieto:
---

# 0057 — Drobne uwagi z recenzji Planu 4

> [!info] Status
> **do-zrobienia** · priorytet **p3** · [← tablica zadań](../../README.md)

## Cel

Rozstrzygnąć z użytkownikiem drobne uwagi z końcowej recenzji
[Planu 4](../../../docs/plany/2026-09-26-plan-4-flatpak.md) (sekcja „Poprawki po recenzji końcowej”). Ważne uwagi są
już poprawione; te nie blokują wydania 0.9.0.

## Kontekst

Recenzja: 2026-09-26, zakres `813461f..dc672f8`. Identyfikator aplikacji — osobno w
[0056](../../W-TRAKCIE/0056-identyfikator-i-wydawca/todo.md).

## Kryteria akceptacji

- [ ] Każda uwaga: zrobiona albo odrzucona z notatką

## Kroki

- [ ] M1: [publikuj.sh](../../../flatpak/publikuj.sh) — pętla po refach przejdzie zero razy, gdy `ostree refs` zawiedzie
  (dziś ratuje to `--gpg-sign` akcji); zebrać refy do tablicy i przerwać, gdy pusta
- [ ] M2: `ruff` bez przypiętej wersji — nowe wydanie ruffa może zaczerwienić CI bez zmian w kodzie
- [ ] M3: pokrycie rdzenia ≥ 90% (specyfikacja 12.6) nie jest sprawdzane w
      [testy.yml](../../../.github/workflows/testy.yml)
- [ ] M4: akcje zewnętrzne przypięte tylko wersją główną, nie SHA (klucz GPG trafia do `ghaction-import-gpg`)
- [ ] M5: `test_version_is_the_same_everywhere` ma wpisane `0.9.0` — każde wydanie zmienia test;
  [wydania.md](../../../docs/procesy/wydania.md) tego nie mówi
- [ ] M6: na komputerze dewelopera zostały `~/.cache/kimai-tray`, `~/.local/state/kimai-tray`, stare ustawienia i wpis
  portfela `application=pl.websystems.KimaiTray` (po zmianie nazwy,
  [0055](../../ZROBIONE/0055-zmiana-nazwy-ws-tracker-tray/todo.md))
- [ ] M7: `RuntimeRepo=` w `.flatpakrepo` ([pages.py](../../../flatpak/pages.py)) nie jest udokumentowanym kluczem
  (nieszkodliwy)

## Materiały

Brak.

## Dziennik

### 2026-09-26

- **12:25** Utworzono z końcowej recenzji Planu 4.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
