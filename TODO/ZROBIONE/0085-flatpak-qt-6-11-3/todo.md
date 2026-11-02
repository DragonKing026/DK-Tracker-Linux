---
noteId: "25749b01df9d49e9aa9e3766e4dedac1"
tytul: "Flatpak nie startuje po aktualizacji runtime'u do Qt 6.11.3"
numer: "0085"
status: w-trakcie
priorytet: p0
tags: [todo, flatpak, wydanie, blad]
zalezy_od: []
utworzono: 2026-11-02 16:45
zaktualizowano: 2026-11-02 16:45
zamknieto:
---

# 0085 — Flatpak nie startuje po aktualizacji runtime'u do Qt 6.11.3

> [!info] Status
> **w-trakcie** · priorytet **p0** · [← tablica zadań](../../README.md)

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

- [ ] Paczka zbudowana z obecnych zależności startuje na runtime z Qt 6.11.3
- [ ] Wydana nowa wersja, `flatpak update` u użytkownika naprawia aplikację
- [ ] Ryzyko powtórki opisane w dokumentacji integracji
- [ ] Zmiany zacommitowane małymi krokami

## Kroki

- [ ] Sprawdzić lokalnym buildem, że nowa BaseApp usuwa błąd
- [ ] Wersja 0.10.19, MetaInfo, testy
- [ ] Opis ryzyka w [Flatpak](../../../docs/integracje/flatpak.md)
- [ ] Wydanie i sprawdzenie u użytkownika

## Materiały

Brak.

## Dziennik

### 2026-11-02 16:45

- Utworzono zadanie. Przyczyna ustalona z `flatpak info`, historii Flathuba i zawartości paczki.
- **16:45** Start pracy.

## Wynik

<!-- Wypełniane przy zamknięciu: co powstało, gdzie, co zostało na później. -->
