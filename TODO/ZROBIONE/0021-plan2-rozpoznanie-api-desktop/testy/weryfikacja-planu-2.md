---
noteId: "0eedff89777e42f4a5ccb5cb2daa7598"
tytul: "Weryfikacja Planu 2 — kod z planu uruchomiony"
tags: [testy, plan-2, desktop]
utworzono: 2026-09-25 20:51
zaktualizowano: 2026-09-25 20:51
---

# Weryfikacja Planu 2 (2026-09-25 20:51)

Kod i testy z [planu 2](../../../../docs/plany/2026-09-25-plan-2-desktop.md) wyciągnięte automatycznie
do kopii repozytorium (poza repo) i uruchomione na stacji deweloperskiej (Fedora 44, Plasma 6.7.5).

| Sprawdzenie | Wynik |
| --- | --- |
| `ruff format` + `ruff check` | **All checks passed** |
| `pytest` (domyślnie) | **206 passed** (175 z Planu 1 + 31 nowych), 12 deselected |
| `pytest -m desktop` (prawdziwa sesja D-Bus) | **3 passed**: sekret w KWallet (zapis/odczyt/usunięcie), powiadomienie pokazane i wycofane, portal Background bez autostartu |
| `~/.config/autostart` | bez zmian |

Poprawki planu po weryfikacji: jednoznaczny nagłówek kroku z `tests/desktop/fakes.py`,
liczba testów w zadaniu 1 (5), usunięty zbędny test-atrapa w renderowaniu powiadomień.
