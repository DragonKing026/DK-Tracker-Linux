---
noteId: "a841621c389e4157800fa5bda7b61ce8"
tytul: "Dokumenty zgodne z markdownlint"
numer: "0043"
status: zrobione
priorytet: p1
tags: [todo, dokumentacja, markdownlint]
zalezy_od: []
utworzono: 2026-09-25 23:39
zaktualizowano: 2026-09-25 23:45
zamknieto: 2026-09-25 23:45
---

# 0043 — Dokumenty zgodne z markdownlint

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Wszystkie pliki `.md` w repozytorium bez uwag rozszerzenia VS Code
[markdownlint](https://github.com/DavidAnson/vscode-markdownlint) (0.62.1, biblioteka
[markdownlint](https://github.com/DavidAnson/markdownlint)), a narzędzia repozytorium
(tablica zadań, szablony, skille) od razu piszą zgodne pliki.

## Kontekst

- Uwaga użytkownika (2026-09-25 23:39): pliki nie trzymają się reguł markdownlint.
- Stan przed zmianą (`npx markdownlint-cli2`, reguły domyślne): 1543 × MD013, 390 × MD060, 123 × MD032,
  47 × MD022, 16 × MD031, 11 × MD040, 4 × MD050, 4 × MD028, 3 × MD012, 2 × MD033, 1 × MD041.
- Decyzja użytkownika: MD013 z limitem **120** znaków, bez tabel, bloków kodu i nagłówków; reszta reguł domyślna.

## Kryteria akceptacji

- [x] `.markdownlint.jsonc` w repozytorium (czyta go i rozszerzenie VS Code, i `markdownlint-cli2`)
- [x] `npx markdownlint-cli2` → 0 błędów
- [x] Skill do sprawdzania i poprawiania, wpisany w reguły (AGENTS.md) i w skill `commit`
- [x] Tablica zadań, szablon zadania i dziennik zadań generowane zgodnie z regułami

## Kroki

- [x] Konfiguracja `.markdownlint.jsonc`
- [x] Skill `markdownlint`: `sprawdz` i `napraw` (tabele, łamanie linii, poprawki automatyczne)
- [x] Poprawienie wszystkich plików
- [x] Generatory: `zadanie.py` (tablica, dziennik), szablon zadania
- [x] Reguła w AGENTS.md, dokumentowanie.md i skill `commit`

## Materiały

- [testy/markdownlint-po.txt](testy/markdownlint-po.txt) — wynik `mdfix.py sprawdz` po zmianach

## Dziennik

### 2026-09-25

- **23:39** Utworzono na prośbę użytkownika.
- **23:45** Zamknięte: 0 błędów markdownlint.

## Wynik

- [.markdownlint.jsonc](../../../.markdownlint.jsonc) — reguły domyślne, MD013 do 120 znaków (bez tabel, kodu, nagłówków).
- Skill [markdownlint](../../../.claude/skills/markdownlint/SKILL.md): `mdfix.py sprawdz` / `napraw`, 8 testów skryptu;
  narzędzie przypięte do wersji z rozszerzenia VS Code (`markdownlint-cli2` 0.23.2).
- 92 pliki poprawione; treść sprawdzona skryptem — identyczna poza białymi znakami, formatem tabel i jedną poprawką
  (`__main__.py` renderował się jako pogrubione „main”).
- `zadanie.py` pisze tablicę i dziennik zgodnie z regułami; reguła dopisana w AGENTS.md, dokumentowanie.md i skillu `commit`.
