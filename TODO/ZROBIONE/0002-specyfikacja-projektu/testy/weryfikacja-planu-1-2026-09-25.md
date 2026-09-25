---
noteId: "96708baf40214a7c994d90737c191e4c"
tytul: "Weryfikacja Planu 1 (rdzeń) — kod z planu uruchomiony"
tags: [testy, plan, core]
utworzono: 2026-09-25 18:49
zaktualizowano: 2026-09-25 18:49
---

# Weryfikacja Planu 1 (rdzeń) — 2026-09-25

Cel: sprawdzić, że kod i testy zapisane w
[planie 1](../../../../docs/plany/2026-09-25-plan-1-rdzen.md) działają, zanim plan trafi do
wykonawcy. Pliki wyciągnięto automatycznie z bloków kodu planu do katalogu tymczasowego
(poza repozytorium). `tracker.py` złożono z części 1 (zadanie 10) i wstawek z zadania 11.

## Wyniki

| Sprawdzenie | Wynik |
| --- | --- |
| `pytest` (domyślny przebieg) | **144 passed**, 8 deselected (kontraktowe) |
| `pytest --cov=kimai_tray.core --cov-fail-under=90` | **98,34%** — próg spełniony |
| `ruff format` + `ruff check` | po poprawce UP047 (`load_json[T]`) — **All checks passed** |
| `pytest -m kimai` na Kimai 2.67.0 w Dockerze | **8 passed** w 36,6 s |

Środowisko: Python 3.14.7 (lokalnie; runtime Flatpaka ma 3.13), httpx 0.28, pytest z pytest-cov 7.1.

## Pokrycie per moduł

| Moduł | Pokrycie |
| --- | --- |
| billable, grouping, i18n, models, notification_policy, timefmt, validation | 100% |
| errors, kimai_client, settings | 98% |
| tracker | 97% |

## Poprawki wprowadzone do planu po weryfikacji

- `settings.load_json` — składnia `def load_json[T](...)` zamiast `TypeVar` (ruff UP047, Python ≥ 3.12).
- Test `update_begin` — godzina porównywana w UTC (`.astimezone(UTC).hour`).
- Liczby oczekiwanych testów w zadaniach 2, 7, 10.
