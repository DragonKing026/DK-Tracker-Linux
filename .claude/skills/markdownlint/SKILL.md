---
name: markdownlint
description: Use before committing any change to a .md file in this repo, and whenever the user mentions markdownlint — checks every Markdown file with the same rules as the VS Code markdownlint extension and fixes tables, line length and the auto-fixable rules.
---

# markdownlint — dokumenty zgodne z regułami rozszerzenia VS Code

Reguły: [.markdownlint.jsonc](../../../.markdownlint.jsonc) (domyślne reguły markdownlint, MD013 z limitem
**120** znaków, bez tabel, bloków kodu i nagłówków). Pliki:
[.markdownlint-cli2.jsonc](../../../.markdownlint-cli2.jsonc).
Wersja narzędzia jest przypięta do tej z rozszerzenia VS Code (`markdownlint-cli2` 0.23.2, markdownlint 0.41.1),
więc terminal i edytor pokazują to samo.

## Komendy

```bash
python3 .claude/skills/markdownlint/mdfix.py sprawdz               # musi być „markdownlint OK.”
python3 .claude/skills/markdownlint/mdfix.py napraw [PLIK.md ...]  # bez plików: całe repo
```

`napraw` robi to, czego nie umie `markdownlint-cli2 --fix`:

- **MD060** — tabele w stylu „compact”: `| a | b |` i `| --- | --- |`;
- **MD013** — łamie prozę do 120 znaków; nie łamie linków ani krótkiego kodu, nie przenosi przecinka
  od słowa, nie zaczyna linii od `-`, `1.`, `#`, `>`, `|` (zmieniłoby znaczenie), nie łamie tytułu calloutu
  (`> [!note] …`), frontmattera ani bloków kodu;
- potem uruchamia `markdownlint-cli2 --fix` (MD012, MD022, MD031, MD032 …).

## Czego `napraw` nie zrobi — poprawiasz ręcznie

- **MD040** — blok kodu bez języka: dopisz język (`text` dla drzew katalogów i przykładów).
- **MD028** — dwa callouty jeden pod drugim: między nie `<!-- osobne callouty -->`.
- **MD033** — `<coś>` w tekście: w kodzie `` `<coś>` ``.
- **MD050** — `__słowo__` poza kodem to pogrubienie; nazwy jak `__main__.py` zawsze w `` ` ` ``
  (automatyczna poprawka zrobiłaby z nich `**main**`).
- **MD041** — pierwszy po frontmatterze musi być nagłówek `#`.

## Przed commitem

1. `mdfix.py napraw <zmienione pliki .md>`
2. `mdfix.py sprawdz` → „markdownlint OK.”
3. `git diff` — łamanie linii zmienia tylko białe znaki; każda inna zmiana treści to błąd.

Testy skryptu: `.venv/bin/pytest .claude/skills/markdownlint -q -p no:cacheprovider
--rootdir=.claude/skills/markdownlint -c /dev/null`.
