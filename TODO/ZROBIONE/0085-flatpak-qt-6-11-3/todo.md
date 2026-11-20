---
noteId: "25749b01df9d49e9aa9e3766e4dedac1"
tytul: "Flatpak nie startuje po aktualizacji runtime'u do Qt 6.11.3"
numer: "0085"
status: zrobione
priorytet: p0
tags: [todo, flatpak, wydanie, blad]
zalezy_od: []
utworzono: 2026-11-02 16:45
zaktualizowano: 2026-11-02 17:13
zamknieto: 2026-11-02 17:13
---

# 0085 — Flatpak nie startuje po aktualizacji runtime'u do Qt 6.11.3

> [!info] Status
> **zrobione** · priorytet **p0** · [← tablica zadań](../../README.md)

## Cel

Przywrócić działanie aplikacji z Flatpaka: wydać paczkę zbudowaną na PySide6 zgodnym z Qt w aktualnym runtime.

## Kontekst

Wydana 0.10.18 nie startuje:

```text
ImportError: /app/lib/python3.13/site-packages/PySide6/QtCore.abi3.so: undefined symbol:
_ZN14QObjectPrivateC2E16QtPrivate_6_11_2, version Qt_6_PRIVATE_API
```

Moduły PySide6 używają prywatnego API Qt, którego symbole są związane z konkretną wersją łatkową Qt
(`QtPrivate_6_11_2`). PySide6 trafia do paczki w czasie budowania (z `io.qt.PySide.BaseApp`), a runtime aktualizuje się
u użytkownika osobno, w obrębie tej samej gałęzi `6.11`:

| Kiedy | Co |
| --- | --- |
| 2026-10-30 13:54 | build 0.10.18 — BaseApp z PySide6 6.11.2 |
| 2026-10-31 00:50 | `org.kde.Platform//6.11` z Qt 6.11.3 — paczka przestaje działać |
| 2026-11-02 01:24 | `io.qt.PySide.BaseApp//6.11` z PySide6 6.11.3 |

Powiązane: [Flatpak](../../../docs/integracje/flatpak.md), [Qt i PySide6](../../../docs/integracje/qt-pyside6.md),
[wydania](../../../docs/procesy/wydania.md).

## Kryteria akceptacji

- [x] Paczka zbudowana z obecnych zależności startuje na runtime z Qt 6.11.3
- [x] Wydana nowa wersja, `flatpak update` u użytkownika naprawia aplikację
- [x] Ryzyko powtórki opisane w dokumentacji integracji
- [x] Zmiany zacommitowane małymi krokami

## Kroki

- [x] Sprawdzić lokalnym buildem, że nowa BaseApp usuwa błąd
- [x] Wersja 0.10.19, MetaInfo, testy
- [x] Opis ryzyka w [Flatpak](../../../docs/integracje/flatpak.md)
- [x] Wydanie i sprawdzenie u użytkownika

## Materiały

Brak.

## Dziennik

### 2026-11-02 16:45

- Utworzono zadanie. Przyczyna ustalona z `flatpak info`, historii Flathuba i zawartości paczki.
- **16:45** Start pracy.
- **17:13** Wydano 0.10.19 (workflow zielony). Po flatpak update: 0.10.19, PySide 6.11.3, Qt 6.11.3, aplikacja działa po
  15 s.

## Wynik

Wydana [0.10.19](https://github.com/DragonKing026/DK-Tracker-Linux/releases/tag/v0.10.19) z PySide6 6.11.3, zbudowana na
nowej BaseApp, bez zmian
w kodzie aplikacji. Po `flatpak update` paczka z repozytorium startuje na Qt 6.11.3. Commity: `abb4220`, `e7e0d0f`.
Pułapka opisana w [dokumentacji Flatpaka](../../../docs/integracje/flatpak.md). Zapobieganie powtórce:
[0086](../../W-TRAKCIE/0086-flatpak-straznik-qt/todo.md),
[issue #3](https://github.com/DragonKing026/DK-Tracker-Linux/issues/3).
