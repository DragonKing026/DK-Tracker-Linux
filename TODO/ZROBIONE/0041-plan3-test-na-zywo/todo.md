---
noteId: "28dc3871d475462e976268df276ec5dc"
tytul: "Plan 3 · Zadanie 13: Test na żywo na KDE z Kimai w Dockerze"
numer: "0041"
status: zrobione
priorytet: p1
tags: [todo, plan-3, ui]
zalezy_od: ["0040"]
utworzono: 2026-09-25 23:07
zaktualizowano: 2026-09-26 09:51
zamknieto: 2026-09-26 09:51
---

# 0041 — Plan 3 · Zadanie 13: Test na żywo na KDE z Kimai w Dockerze

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 13** z [Planu 3: Interfejs Qt](../../../docs/plany/2026-09-25-plan-3-ui.md)
(sekcja „Task 13: Test na żywo na KDE z Kimai w Dockerze”) dokładnie według kroków planu.

## Kontekst

- Plan: [2026-09-25-plan-3-ui.md](../../../docs/plany/2026-09-25-plan-3-ui.md) — kod, testy i komendy każdego kroku.
- Specyfikacja: [Kimai Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md); decyzje UI:
  [0028](../0028-plan3-projekt-ui/todo.md).
- Pliki:
- Create (w folderze zadania TODO): `testy/lista-kontrolna.md`, `zrzuty/*.png` (tylko wycinki okna aplikacji i ikony —
  **nigdy** cały pulpit)
- Modify: `README.md` (status), `docs/plany/README.md`

## Kryteria akceptacji

- [x] Każdy punkt listy kontrolnej sprawdzony z użytkownikiem
- [x] Wynik planu: lista kontrolna 12 punktów z użytkownikiem.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Kimai testowy i izolowana konfiguracja
- [x] Step 2: Lista kontrolna z użytkownikiem
- [x] Step 3: Zrzuty
- [x] Step 4: Sprzątanie
- [x] Step 5: Status
- [x] Step 6: Commit

## Materiały

- [testy/lista-kontrolna.md](testy/lista-kontrolna.md) — 12 punktów z wynikami
- ![Okno w ciemnym motywie](zrzuty/okno-ciemny-motyw.png)

## Dziennik

### 2026-09-25

- **23:07** Utworzono zadanie z Planu 3.
- **23:11** Start wykonania.

### 2026-09-26

- **09:51** Zamknięte: test na żywo 12/12.

## Wynik

Test na żywo z użytkownikiem na KDE Plasma 6.7.5 i Kimai 2.67 w Dockerze: 12/12 punktów działa
([lista kontrolna](testy/lista-kontrolna.md)). Znalezione po drodze błędy i prośby poprawione w
[0042](../0042-poprawki-po-tescie-na-zywo/todo.md) (11 uwag) i przy punkcie 10 (niskie okno bez konfiguracji);
reguły markdownlint — [0043](../0043-markdownlint/todo.md). Link do Kimai otworzył Firefoxa tylko przez
izolację testu (`XDG_CONFIG_HOME`), normalnie otwiera domyślną przeglądarkę.
