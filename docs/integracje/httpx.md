---
noteId: "e2a2269367b546b8867d23207ac437c4"
tytul: httpx
tags: [integracja, http, python]
status_integracji: w-uzyciu
wersja: 0.28.1 (PyPI, 2026-09-25)
utworzono: 2026-09-25 17:39
zaktualizowano: 2026-09-25 19:02
---

# httpx — klient HTTP

> [!info] W skrócie
> Klient HTTP dla Pythona z API synchronicznym i asynchronicznym. U nas używamy go
> w kliencie Kimai API w rdzeniu bez Qt ([ADR-0004](../decyzje/0004-architektura-rdzen-python-ui-qt.md)).

## Do czego używamy

- Jedna instancja `httpx.Client` na konfigurację (URL + token):
  - `base_url` = adres Kimai,
  - `headers` = `Authorization: Bearer …`, `Accept: application/json`,
  - `timeout` jawnie ustawiony, bo domyślny to 5 s ([źródło](https://www.python-httpx.org/advanced/timeouts/)).
- Wywołania **synchroniczne**, uruchamiane w wątkach `QThreadPool` przez warstwę UI.
  Rdzeń nie wie nic o wątkach.

```python
client = httpx.Client(
    base_url=settings.url,
    headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    timeout=10.0,
)
```

## Testy — MockTransport

([źródło](https://www.python-httpx.org/advanced/transports/))

```python
def handler(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/api/timesheets/active":
        return httpx.Response(200, json=[])
    return httpx.Response(404)

client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://kimai.test")
```

Dzięki temu każdy scenariusz z [katalogu funkcji](../architektura/funkcje.md) (400
„extra fields”, 404 za ostatnią stroną, 401) testujemy bez serwera.

## Zależności (do Flatpaka)

`anyio`, `certifi`, `httpcore` (1.x), `idna` (+ ich zależności) — wszystko czysty Python.
Moduły manifestu generujemy narzędziem
[flatpak-pip-generator](https://github.com/flatpak/flatpak-builder-tools/tree/master/pip).

## Pułapki

> [!warning]
> - Domyślny timeout 5 s — przy wolnym Kimai lepiej ustawić jawnie.
> - `certifi` ma własny zestaw CA. Firmowe Kimai z certyfikatem wewnętrznego CA nie
>   przejdzie weryfikacji. Wtedy opcja „użyj systemowego magazynu CA” (`ssl` context
>   z `/etc/ssl` w runtime) — do rozważenia, gdy wystąpi.
> - Nigdy nie logujemy nagłówków żądań (token).

## Gdzie w kodzie

- [src/kimai_tray/core/kimai_client.py](../../src/kimai_tray/core/kimai_client.py) — jedyne miejsce użycia `httpx.Client`.
- [tests/core/test_kimai_client.py](../../tests/core/test_kimai_client.py) — `httpx.MockTransport`.

## Dokumentacja

- [HTTPX](https://www.python-httpx.org/)
- [Klienci: base_url, nagłówki](https://www.python-httpx.org/advanced/clients/)
- [Timeouty](https://www.python-httpx.org/advanced/timeouts/)
- [Transporty i MockTransport](https://www.python-httpx.org/advanced/transports/)

## Powiązane

- [Kimai REST API](kimai-api.md)
- [ADR-0004](../decyzje/0004-architektura-rdzen-python-ui-qt.md)
