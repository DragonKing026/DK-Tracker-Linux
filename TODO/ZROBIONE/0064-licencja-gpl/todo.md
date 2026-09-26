---
noteId: "ec8231ac333b45afa8c70fdd42bfb204"
tytul: "Licencja GPL-3.0-or-later zamiast AGPL"
numer: "0064"
status: zrobione
priorytet: p1
tags: [todo, licencja]
zalezy_od: []
utworzono: 2026-09-26 14:13
zaktualizowano: 2026-09-26 14:14
zamknieto: 2026-09-26 14:14
---

# 0064 — Licencja GPL-3.0-or-later zamiast AGPL

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Od następnej wersji licencja **GPL-3.0-or-later** zamiast AGPL-3.0-or-later.

## Kontekst

- Uwaga użytkownika: to aplikacja na pulpit, nie serwer — dodatkowy punkt AGPL (udostępnianie przez sieć) jej nie
  dotyczy; do wyboru GPL albo MIT. Decyzja (2026-09-26): **GPL** na teraz; po przekazaniu projektu firmie właściciel
  może zmienić (firmowa wtyczka jest na MIT). Wydania 0.9.0 i 0.9.1 zostają na AGPL.

## Kryteria akceptacji

- [x] `LICENSE` = tekst GPLv3 z gnu.org; `pyproject.toml`, MetaInfo, README, dokumentacja
- [x] Test licencji zmieniony przed kodem

## Kroki

- [x] Testy (TDD), implementacja, dokumentacja

## Materiały

- [testy/pytest-2026-09-26.txt](testy/pytest-2026-09-26.txt) — końcowy przebieg:
  `460 passed, 1 skipped, 14 deselected in 3.47s`

## Dziennik

### 2026-09-26

- **14:13** Utworzono i start.
- **14:14** Zamknięte: 460 passed, 1 skipped, 14 deselected in 3.47s, commity na main.

## Wynik

[LICENSE](../../../LICENSE) — GPLv3 z gnu.org; `pyproject.toml`, MetaInfo, README, dokumentacja. Wydania 0.9.0 i
0.9.1 zostają na AGPL; nowa licencja od następnego wydania.
