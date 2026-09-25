---
noteId: "fb16419f8af44ecebe16e10fbafcdb21"
tytul: Kimai testowy w Dockerze
tags: [testy, kimai, docker]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
---

# Kimai testowy w Dockerze

Lokalny Kimai do testów kontraktowych i integracyjnych. Testy mogą zapisywać, zmieniać
i usuwać wpisy **bez dotykania Kimai firmy**. Opis integracji:
[docs/integracje/kimai-docker.md](../../docs/integracje/kimai-docker.md).

## Użycie

```bash
tests/kimai/kimai-testowe.sh up      # start + konta + tokeny + dane (~25 s, idempotentne)
eval "$(tests/kimai/kimai-testowe.sh env)"   # zmienne KIMAI_TEST_* w bieżącej powłoce
tests/kimai/kimai-testowe.sh down    # zatrzymanie i usunięcie wszystkiego (także wolumenów)
```

`up` wypisuje gotowe `export`-y, więc można też: `eval "$(tests/kimai/kimai-testowe.sh up)"`.

| Zmienna | Domyślnie | Znaczenie |
|---|---|---|
| `KIMAI_VERSION` | `2.67.0` | tag obrazu `kimai/kimai2` (np. wersja z Kimai firmy) |
| `KIMAI_TEST_PORT` | `8001` | port na `127.0.0.1` |

## Co jest w środku

| Konto | Rola | Token (`KIMAI_TEST_*_TOKEN`) | Po co |
|---|---|---|---|
| `admin` | ROLE_SUPER_ADMIN | `ADMIN` | zakładanie danych testowych |
| `jan` | ROLE_USER | `USER` | typowy pracownik — **bez** prawa do billable (400 „extra fields”) |
| `kierownik` | ROLE_TEAMLEAD | `LEAD` | billable dozwolone |

Dane: klienci „Hotel Morski” (billable) i „Sprawy wewnętrzne” (niebillable); projekty
„Moduł rezerwacji”, „Integracja z KSeF”, „Administracja”; czynności „Programowanie”,
„Spotkanie”, „Szkolenie wewnętrzne” (niebillable).

Hasła kont: `admin12345`, `jan12345`, `kier12345` (panel: <http://127.0.0.1:8001>).
To dane wyłącznie lokalnego kontenera testowego.

## Ważne

- **Strefa czasowa kont to UTC** (domyślna w kontenerze). Czas wysyłany do API liczymy
  w strefie z `/api/users/me → timezone`. Inaczej wpisy lądują w przyszłości
  ([raport ze spike'u](../../TODO/W-TRAKCIE/0002-specyfikacja-projektu/testy/raport-kimai-docker-2026-09-25.md)).
- Tokeny są wstawiane SQL-em do `kimai2_access_token`, bo Kimai nie ma na to komendy.
  Jeśli po aktualizacji Kimai to przestanie działać, `up` kończy się błędem
  „Token for … is rejected”.
- Kolory projektów muszą pochodzić z palety Kimai (`theme.color_choices`, np. `#008000`),
  inaczej API odpowiada 400 „The selected choice is invalid”.
- Testy wymagające tego środowiska oznaczamy `@pytest.mark.kimai`.
