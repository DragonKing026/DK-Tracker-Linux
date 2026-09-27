---
noteId: "94d697ed28c14208b4ce42a5dff2126d"
tytul: "O programie i wersja w ustawieniach (0.10.4)"
numer: "0072"
status: zrobione
priorytet: p2
tags: [todo, ui, ustawienia, wydanie]
zalezy_od: ["0070-plan6-podsumowania"]
utworzono: 2026-09-27 12:50
zaktualizowano: 2026-09-27 13:07
zamknieto: 2026-09-27 13:07
---

# 0072 — O programie i wersja w ustawieniach (0.10.4)

> [!info] Status
> **zrobione** · priorytet **p2** · [← tablica zadań](../../README.md)

## Cel

Na stronie ustawień okna głównego sekcja „O programie”: nazwa, wersja, krótki opis, licencja, strona projektu.

## Kontekst

- Użytkownik po teście 0.10.3 (2026-09-27): „w ustawieniach dodaj about i wersję”; bez pytania o zgodę przed
  wydaniem. Wydanie 0.10.4, kalendarz przesuwa się na 0.10.5
  ([specyfikacja 0.10](../../../docs/specyfikacja/2026-09-26-okno-glowne-0.10.md)).

## Kryteria akceptacji

- [x] Sekcja „O programie” na stronie ustawień: znak, nazwa, wersja z pakietu, opis, licencja, link do projektu
- [x] PL/EN, oba motywy; test dymny i test formularza
- [x] Dokumentacja zaktualizowana; wydanie 0.10.4

## Kroki

- [x] Wersja i teksty w `SettingsForm`
- [x] Sekcja w `SettingsView.qml`
- [x] Dokumentacja, wersja 0.10.4, wydanie

## Materiały

Brak.

## Dziennik

### 2026-09-27

- **12:50** Utworzono i start.
- **13:07** Wydane 0.10.4 (tag v0.10.4); CI i Pages zielone.

## Wynik

Wydane [0.10.4](https://github.com/DragonKing026/DK-Tracker-Linux/releases/tag/v0.10.4): karta „O programie” na
dole strony ustawień (znak, nazwa, wersja, opis, licencja, strona projektu); podpowiedź normy mówi o dniu roboczym.
