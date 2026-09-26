---
noteId: "fda18fd8e37947e5896f40e0f0b14a98"
tytul: "Plan 4 · Zadanie 4: Budowa lokalna w kontenerze (`flatpak/buduj.sh`)"
numer: "0049"
status: zrobione
priorytet: p1
tags: [todo, plan-4, flatpak]
zalezy_od: ["0048"]
utworzono: 2026-09-26 11:28
zaktualizowano: 2026-09-26 11:54
zamknieto: 2026-09-26 11:54
---

# 0049 — Plan 4 · Zadanie 4: Budowa lokalna w kontenerze (`flatpak/buduj.sh`)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

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

- [x] Każdy test z zadania napisany przed kodem i widziany jako padający
- [x] Wynik planu: walidacja AppStream i lint bez uwag, paczka w `dist/`.
- [x] Pełny `.venv/bin/pytest` zielony, `ruff format` + `ruff check` bez uwag
- [x] Commit(y) zgodne z planem; odchylenia zapisane jako „Ruling” w dzienniku

## Kroki

- [x] Step 1: Skrypt
- [x] Step 2: Uruchom budowę
- [x] Step 3: Sprawdź skrypt
- [x] Step 4: Dokumentacja
- [x] Step 5: Commit

## Materiały

- Wynik: [testy/budowa-2026-09-26.log](testy/budowa-2026-09-26.log) — walidacja AppStream, `lint manifest: OK`,
  `lint repo: OK`, paczka 71 MB

## Dziennik

### 2026-09-26

- **11:28** Utworzono zadanie z Planu 4.
- **11:48** Start wykonania.
- **11:54** Zamknięte: [testy/budowa-2026-09-26.log](testy/budowa-2026-09-26.log) — walidacja AppStream,
  `lint manifest: OK`, `lint repo: OK`, paczka 71 MB, commity na main.

## Wynik

[buduj.sh](../../../flatpak/buduj.sh) buduje paczkę `dist/pl.websystems.WsTrackerTray-0.9.0.flatpak` w obrazie
`flathub-infra` kde-6.11. Odchylenie: linter zgłosił nowy wyjątek tylko dla Flathuba
(`appstream-external-screenshot-url`) — dopisany do dopuszczonych. Dokumentacja:
[ADR-0006](../../../docs/decyzje/0006-budowanie-flatpaka-w-kontenerze.md),
[Flatpak](../../../docs/integracje/flatpak.md), [AGENTS.md](../../../AGENTS.md).
