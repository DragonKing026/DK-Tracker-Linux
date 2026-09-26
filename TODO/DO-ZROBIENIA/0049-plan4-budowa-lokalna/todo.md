---
noteId: "fda18fd8e37947e5896f40e0f0b14a98"
tytul: "Plan 4 · Zadanie 4: Budowa lokalna w kontenerze (`flatpak/buduj.sh`)"
numer: "0049"
status: do-zrobienia
priorytet: p1
tags: [todo, plan-4, flatpak]
zalezy_od: ["0048"]
utworzono: 2026-09-26 11:28
zaktualizowano: 2026-09-26 11:28
zamknieto:
---

# 0049 — Plan 4 · Zadanie 4: Budowa lokalna w kontenerze (`flatpak/buduj.sh`)

> [!info] Status
> **do-zrobienia** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wykonać **zadanie 4** z [Planu 4: Flatpak i wydanie](../../../docs/plany/2026-09-26-plan-4-flatpak.md)
(sekcja „Task 4: Budowa lokalna w kontenerze (`flatpak/buduj.sh`)”) dokładnie według kroków planu, metodą TDD.

## Kontekst

- Plan: [2026-09-26-plan-4-flatpak.md](../../../docs/plany/2026-09-26-plan-4-flatpak.md) — kod, testy i komendy każdego
  kroku.
- Specyfikacja: [WS Tracker Tray 1.0](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md); decyzje:
  [0045](../../W-TRAKCIE/0045-plan4-projekt-flatpak/todo.md).
- Pliki:

- Create: `flatpak/buduj.sh`
- Modify: `.gitignore` (`dist/`), `docs/decyzje/0006-budowanie-flatpaka-w-kontenerze.md`, `docs/integracje/flatpak.md`,
  `AGENTS.md` („Komendy”)

## Kryteria akceptacji

- [ ] Każdy test z zadania napisany przed kodem i widziany jako padający
- [ ] Wynik planu: walidacja AppStream i lint bez uwag, paczka w `dist/`.
- [ ] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [ ] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [ ] Step 1: Skrypt
- [ ] Step 2: Uruchom budowę
- [ ] Step 3: Sprawdź skrypt
- [ ] Step 4: Dokumentacja
- [ ] Step 5: Commit

## Materiały

Brak (materiały pojawią się w podfolderach przy wykonaniu).

## Dziennik

### 2026-09-26

- **11:28** Utworzono zadanie z Planu 4.

## Wynik

<!-- Wypełniane przy zamknięciu. -->
