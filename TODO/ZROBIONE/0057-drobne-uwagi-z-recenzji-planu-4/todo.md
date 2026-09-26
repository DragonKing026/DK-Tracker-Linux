---
noteId: "71460991a53d4e68af031c3926a7fc33"
tytul: "Drobne uwagi z recenzji Planu 4"
numer: "0057"
status: zrobione
priorytet: p3
tags: [todo, plan-4, recenzja]
zalezy_od: []
utworzono: 2026-09-26 12:25
zaktualizowano: 2026-09-26 12:40
zamknieto: 2026-09-26 12:40
---

# 0057 — Drobne uwagi z recenzji Planu 4

> [!info] Status
> **zrobione** · priorytet **p3** · [← tablica zadań](../../README.md)

## Cel

Rozstrzygnąć z użytkownikiem drobne uwagi z końcowej recenzji
[Planu 4](../../../docs/plany/2026-09-26-plan-4-flatpak.md) (sekcja „Poprawki po recenzji końcowej”). Ważne uwagi są
już poprawione; te nie blokują wydania 0.9.0.

## Kontekst

Recenzja: 2026-09-26, zakres `813461f..dc672f8`. Identyfikator aplikacji — osobno w
[0056](../0056-identyfikator-i-wydawca/todo.md).

## Kryteria akceptacji

- [x] Każda uwaga: zrobiona albo odrzucona z notatką

## Kroki

- [x] M1: [publikuj.sh](../../../flatpak/publikuj.sh) — pętla po refach przejdzie zero razy, gdy `ostree refs` zawiedzie
  (dziś ratuje to `--gpg-sign` akcji); zebrać refy do tablicy i przerwać, gdy pusta — **zrobione: refy w tablicy, pusta
  → błąd (`test_publish_stops_when_the_repository_has_no_app`)**
- [x] M2: `ruff` bez przypiętej wersji — nowe wydanie ruffa może zaczerwienić CI bez zmian w kodzie — **zrobione:
      `ruff>=0.16,<0.17`**
- [x] M3: pokrycie rdzenia ≥ 90% (specyfikacja 12.6) nie jest sprawdzane w
      [testy.yml](../../../.github/workflows/testy.yml) — **zrobione: `--cov=ws_tracker_tray.core --cov-fail-under=90` w
      CI (`test_ci_enforces_core_coverage`)**
- [x] M4: akcje zewnętrzne przypięte tylko wersją główną, nie SHA (klucz GPG trafia do `ghaction-import-gpg`) —
      **decyzja: wariant A — akcje firm trzecich przypięte do SHA, `actions/*` na tagach
      (`test_third_party_actions_are_pinned_to_a_commit`,
      [github-actions](../../../docs/integracje/github-actions.md))**
- [x] M5: `test_version_is_the_same_everywhere` ma wpisane `0.9.0` — każde wydanie zmienia test;
  [wydania.md](../../../docs/procesy/wydania.md) tego nie mówi — **zrobione: testy bez stałej wersji — wersja z
  `pyproject.toml` = `__init__.py` = najnowsze wydanie w MetaInfo**
- [x] M6: na komputerze dewelopera zostały `~/.cache/kimai-tray`, `~/.local/state/kimai-tray`, stare ustawienia i wpis
  portfela `application=pl.websystems.KimaiTray` (po zmianie nazwy,
  [0055](../0055-zmiana-nazwy-ws-tracker-tray/todo.md)) — **decyzja: usunąć; usunięte katalogi, wpis portfela (token
  Kimai z Dockera), stary Kimai testowy w Dockerze i 11 GB resztek prób w cache budowy**
- [x] M7: `RuntimeRepo=` w `.flatpakrepo` ([pages.py](../../../flatpak/pages.py)) nie jest udokumentowanym kluczem
  (nieszkodliwy) — **zrobione: usunięty — w dokumentacji Flatpaka `RuntimeRepo` jest tylko kluczem `.flatpakref`**

## Materiały

- [testy/pytest-2026-09-26.txt](testy/pytest-2026-09-26.txt) — końcowy przebieg:
  `422 passed, 1 skipped, 12 deselected in 2.71s`

## Dziennik

### 2026-09-26

- **12:25** Utworzono z końcowej recenzji Planu 4.
- **12:29** Start: przegląd uwag.
- **12:31** M1, M2, M3, M5, M7 zrobione (421 testów, próba publikacji w kontenerze OK); M4 i M6 do decyzji.
- **12:40** Zamknięte: 422 passed, 1 skipped, 12 deselected in 2.71s, commity na main.

## Wynik

Wszystkie 7 uwag rozstrzygnięte: M1, M2, M3, M5, M7 poprawione samodzielnie; M4 (wariant A) i M6 (usunąć) — decyzje
użytkownika. Testy: [test_skrypty_flatpak.py](../../../tests/test_skrypty_flatpak.py),
[test_pakiet.py](../../../tests/test_pakiet.py), [test_strona_repo.py](../../../tests/test_strona_repo.py).
