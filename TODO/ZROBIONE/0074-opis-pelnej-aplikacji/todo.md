---
noteId: "52bdddd552f248ac8a57f1566d343556"
tytul: "Opis DK Tracker jako pełnego klienta Kimai: README, dokumentacja, strona, zrzuty"
numer: "0074"
status: zrobione
priorytet: p1
tags: [todo, dokumentacja, strona, zrzuty]
zalezy_od: ["0073-plan7-kalendarz"]
utworzono: 2026-09-27 14:02
zaktualizowano: 2026-09-27 14:12
zamknieto: 2026-09-27 14:12
---

# 0074 — Opis DK Tracker jako pełnego klienta Kimai: README, dokumentacja, strona, zrzuty

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Opisy aplikacji (README, dokumentacja, MetaInfo, strona projektu, plik `.desktop`) mówią o DK Tracker jak o
aplikacji w tacce systemowej. Od 0.10 to klient Kimai z oknem głównym (wpisy, podsumowania, kalendarz), a tacka i
okienko przy niej służą do szybkiego startu i stopu. Opisy i zrzuty mają to pokazywać.

## Kontekst

- Użytkownik (2026-09-27, po wydaniu 0.10.5): README i dokumentacja nadal opisują starą wersję; do tego nowe zrzuty
  i poprawiona strona — napisane samodzielnie, nie słowo w słowo.
- [Specyfikacja 0.10](../../../docs/specyfikacja/2026-09-26-okno-glowne-0.10.md), sekcja 1.

## Kryteria akceptacji

- [x] README (oba) i indeks dokumentacji, przegląd projektu, AGENTS.md: okno główne na pierwszym planie
- [x] MetaInfo (opis w Discover, zrzuty), `.desktop`, `pyproject.toml`, `.flatpakrepo`
- [x] Strona projektu: nagłówek, zrzuty okna głównego, funkcje, konfiguracja
- [x] Nowe zrzuty okna głównego z wymyślonymi danymi, skrypt do ich odświeżania
- [x] Testy, markdownlint, linki; strona opublikowana

## Kroki

- [x] Skrypt i zrzuty
- [x] README i dokumentacja
- [x] MetaInfo, `.desktop`, opis pakietu
- [x] Strona projektu

## Materiały

Zrzuty w dokumentacji: [docs/assets/zrzuty/](../../../docs/assets/zrzuty/) — tworzy je
[scripts/zrzuty-okna.py](../../../scripts/zrzuty-okna.py) (wymyślone dane).

## Dziennik

### 2026-09-27

- **14:02** Utworzono i start.
- **14:12** README, dokumentacja, MetaInfo, strona i zrzuty zaktualizowane; strona publikowana po pushu.

## Wynik

Opis DK Tracker jako klienta Kimai z oknem głównym (tacka do szybkiego dostępu): oba README,
[przegląd projektu](../../../docs/architektura/przeglad.md), indeks dokumentacji, architektura, AGENTS.md, MetaInfo
(opis i cztery zrzuty), `.desktop`, opis pakietu, „O programie”, strona projektu (nagłówek z oknem głównym, sekcja
Widoki). Nowe zrzuty: wpisy, okno edycji, podsumowania, kalendarz. Specyfikacja 1.0 i ADR zostały bez zmian — to
zapis decyzji z tamtego czasu. MetaInfo i `.desktop` trafią do Discover z następnym wydaniem.
