---
noteId: "6378874d09904eb8a9941af1a59ce41c"
tytul: "Specyfikacja projektu (design) i plan implementacji"
numer: "0002"
status: w-trakcie
priorytet: p0
tags: [todo, planowanie, spec]
zalezy_od: []
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
zamknieto:
---

# 0002 — Specyfikacja projektu i plan implementacji

> [!info] Status
> **w-trakcie** · priorytet **p0** · [← tablica zadań](../../README.md)

## Cel

Razem z użytkownikiem doprecyzować, co dokładnie budujemy w wersji 1.0, i zapisać
zatwierdzoną specyfikację, a potem szczegółowy plan implementacji w małych krokach.

## Kontekst

- Punkt wyjścia: [Przegląd](../../../docs/architektura/przeglad.md), [Katalog funkcji](../../../docs/architektura/funkcje.md),
  [szkic architektury](../../../docs/architektura/architektura-aplikacji.md).
- Proces: pytania → 2–3 podejścia → projekt w sekcjach → spec → akceptacja → plan.

## Kryteria akceptacji

- [x] Ustalony zakres 1.0: F-20, F-21, F-22 wchodzą; F-23, F-24 później
- [x] Zatwierdzony stos ([0003](../../ZROBIONE/0003-wybor-stosu/todo.md) → [ADR-0002](../../../docs/decyzje/0002-stos-python-pyside6.md): Python + PySide6)
- [x] Zatwierdzona forma okna na Waylandzie ([ADR-0003](../../../docs/decyzje/0003-okno-szybkiej-obslugi-na-wayland.md))
- [ ] Spec zapisana w `docs/specyfikacja/` ([2026-09-25-kimai-tray-1.0.md](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md)) i zaakceptowana przez użytkownika
- [ ] Sekcja „Komendy” w [AGENTS.md](../../../AGENTS.md) zaplanowana (uzupełniana przy szkielecie projektu)
- [ ] Plan implementacji zapisany i zaakceptowany; kolejne zadania TODO z planu utworzone

## Kroki

- [ ] Pytania o cel i zakres (jedno na raz)
- [ ] Propozycje podejść z rekomendacją
- [ ] Projekt w sekcjach: architektura, komponenty, przepływ danych, błędy, testy
- [ ] Spec + samoprzegląd
- [ ] Plan implementacji

## Materiały

- [prototyp/kimai-docker/](prototyp/kimai-docker/) — Kimai w Dockerze + skrypty sprawdzające API (spike, do wyrzucenia)
- [testy/raport-kimai-docker-2026-09-25.md](testy/raport-kimai-docker-2026-09-25.md) — raport z weryfikacji API
- [testy/](testy/) — surowe wyniki uruchomień (`wynik-probe-*.txt`)

## Dziennik

### 2026-09-25
- Utworzono zadanie.
- Rozpoczęto brainstorming. Pytanie 1 (stos) → Python + PySide6 ([ADR-0002](../../../docs/decyzje/0002-stos-python-pyside6.md)).
- Pytanie 2 (okno) → wariant A + menu kontekstowe, B do prototypu ([ADR-0003](../../../docs/decyzje/0003-okno-szybkiej-obslugi-na-wayland.md), [0004](../../DO-ZROBIENIA/0004-prototyp-tacki-i-okna/todo.md)).
- Pytanie 3 (zakres) → autostart i powiadomienia w 1.0; bezczynność i skrót później.
- Pytanie 4 (powiadomienia) → długi timer, utrata połączenia, potwierdzenie z menu ([F-21](../../../docs/architektura/funkcje.md)).
- Podejście → 1: rdzeń w czystym Pythonie, httpx, jeepney, Qt Widgets ([ADR-0004](../../../docs/decyzje/0004-architektura-rdzen-python-ui-qt.md)).
- Użytkownik przypomniał: aplikacja w pełnej wersji PL i EN → doprecyzowano [F-13](../../../docs/architektura/funkcje.md).
- Sekcja 1 projektu (moduły i katalogi) zaakceptowana.
- Sekcja 2 (przepływ danych: Snapshot, AppState, odświeżanie 60 s / pełne, kolejka akcji, polityka powiadomień w rdzeniu, jedna instancja) zaakceptowana.
- Sekcja 3 (obsługa błędów i przypadki brzegowe) zaakceptowana.
- Struktura TODO zmieniona: foldery DO-ZROBIENIA / W-TRAKCIE / ZROBIONE; status `w-toku` → `w-trakcie`.
- Spike: Kimai 2.67.0 w Dockerze do testów — działa; tokeny wstawiane SQL-em. Wykryto pułapkę strefy czasowej. Raport: [testy/raport-kimai-docker-2026-09-25.md](testy/raport-kimai-docker-2026-09-25.md).
- Sekcja 4 (testy) zaakceptowana, z Kimai w Dockerze do testów kontraktowych. Środowisko dodane do repo: [tests/kimai/](../../../tests/kimai/README.md).
- Spisano specyfikację: [2026-09-25-kimai-tray-1.0.md](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md) — czeka na akceptację.
- Nowe zasady od użytkownika: materiały zadań w podfolderach, linki markdown wszędzie ([sprawdz-linki](../../../.claude/skills/sprawdz-linki/SKILL.md)).

## Wynik
