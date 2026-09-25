---
noteId: "0ecfc22f03a54724b3d336cfb9cbb87b"
tytul: Architektura — rdzeń w czystym Pythonie, Qt tylko w interfejsie
tags: [adr, architektura, http, sekrety, ui]
status: zaakceptowana
zastapiona_przez:
utworzono: 2026-09-25 17:39
zaktualizowano: 2026-09-25 17:47
---

# ADR-0004: Rdzeń w czystym Pythonie (httpx, jeepney), UI w Qt Widgets

## Kontekst

Po wyborze PySide6 ([ADR-0002](0002-stos-python-pyside6.md)) zostały trzy
decyzje: jak rozdzielić logikę od UI, czym robić HTTP i jak przechowywać token.
Logika wtyczki (walidacja, billable, formatowanie, klient API) ma zostać przeniesiona
1:1 i być dobrze przetestowana.

## Rozważane opcje

| Opcja | Zalety | Wady |
| --- | --- | --- |
| **1. Rdzeń bez Qt: `httpx` + `jeepney`, UI Qt Widgets** | rdzeń testowany zwykłym pytest, bez pętli zdarzeń; atrapa Kimai przez `httpx.MockTransport`; tylko czysto-pythonowe zależności (bez kompilacji w Flatpaku) | kilka paczek pip w manifeście; I/O w wątkach roboczych |
| 2. Wszystko w Qt: `QNetworkAccessManager`, `QtDBus`, QML | zero zależności pip | logika spleciona z pętlą Qt, trudniejsze testy, QML + Python trudniejszy w debugowaniu |

Odrzucone w ramach opcji 1: `secretstorage`. Wymaga `cryptography`, a jej budowa
w Flatpaku potrzebuje toolchainu Rusta.

## Decyzja

**Rdzeń aplikacji (domena, klient Kimai API, ustawienia, sekrety) jest czystym Pythonem
bez importów Qt. HTTP: `httpx`. Sekrety: własny mały moduł na `jeepney` do Secret Service
(sesja `plain`, kolekcja `default`). UI: Qt Widgets ze stylem odwzorowującym wtyczkę.
Wywołania sieciowe w `QThreadPool`, wyniki wracają sygnałami.**

Zaakceptowane przez użytkownika 2026-09-25.

## Uzasadnienie

- Logika wtyczki to czyste funkcje, które w Pythonie testujemy tak samo łatwo jak w JS.
- `httpx` ma wbudowany `MockTransport`, więc testy klienta API nie potrzebują serwera.
- `jeepney` to czysty Python bez zależności (0.9.0). Na stacji deweloperskiej
  sprawdzono 2026-09-25: `OpenSession('plain')` działa z ksecretd, alias `default`
  wskazuje `/org/freedesktop/secrets/collection/kdewallet`.
- Sesja `plain` jest dopuszczona przez specyfikację („strongly recommended” do
  obsługi). Sekret idzie po lokalnej szynie sesji użytkownika bez szyfrowania transportu.
  To akceptowalne, bo szyna jest dostępna tylko dla procesów tego użytkownika.

## Konsekwencje

- Flatpak: `--talk-name=org.freedesktop.secrets`; paczki pip (`httpx` + zależności,
  `jeepney`) generowane przez `flatpak-pip-generator`.
- Token jest widoczny w KWallet / GNOME Keyring jako „`Kimai Tray — <url>`” i użytkownik
  może go usunąć.
- Moduł sekretów jest za interfejsem, więc można go później zamienić na portal Secret.
- Zablokowany portfel (`IsLocked`) wymaga `Unlock` → systemowe okno hasła. Obsługa
  asynchroniczna, bez blokowania UI.
- Zasada architektury: katalog rdzenia nie może importować `PySide6`. Pilnuje tego test.

## Powiązane

- [httpx](../integracje/httpx.md)
- [jeepney](../integracje/jeepney.md)
- [Secret Service](../integracje/secret-service.md)
- [Qt / PySide6](../integracje/qt-pyside6.md)
