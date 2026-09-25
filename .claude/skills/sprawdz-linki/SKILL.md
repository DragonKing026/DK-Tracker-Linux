---
name: sprawdz-linki
description: Use after creating, moving or renaming any .md file (or a TODO task folder) in this repo, before every commit touching docs/ or TODO/, and whenever a link might be broken — checks all relative Markdown links, repairs them after moves, moves files with automatic link rewriting, and converts [[wikilinks]] to Markdown links.
---

# sprawdz-linki — linki w dokumentacji

Linki w repo to **względne linki markdown** `[tekst](../sciezka/plik.md)`. Działają
w VS Code, Obsidianie i na GitHubie. Wikilinki `[[...]]` są zakazane: VS Code i GitHub
ich nie obsługują.

Skrypt: `.claude/skills/sprawdz-linki/linki.py` (uruchamiany z katalogu głównego repo).

## Komendy

```bash
# 1. Sprawdź wszystkie linki (kod wyjścia 1 = są problemy)
python3 .claude/skills/sprawdz-linki/linki.py sprawdz

# 2. Przenieś plik lub folder I popraw wszystkie linki (do niego i w nim)
python3 .claude/skills/sprawdz-linki/linki.py przenies TODO/W-TRAKCIE/0004-prototyp TODO/ZROBIONE/0004-prototyp

# 3. Napraw zepsute linki po przeniesieniu zrobionym ręcznie
#    (szuka pliku o tej samej nazwie; gdy kandydatów jest kilka — zgłasza do ręcznej poprawy)
python3 .claude/skills/sprawdz-linki/linki.py napraw

# 4. Zamień wikilinki [[...]] na linki markdown
python3 .claude/skills/sprawdz-linki/linki.py wikilinki
```

## Kiedy

- **Przenosisz lub zmieniasz nazwę pliku `.md` / folderu zadania** → zawsze `przenies`
  zamiast `git mv` (skill `zmien-status-zadania` robi tak przy każdej zmianie statusu).
- **Przed commitem** zmian w `docs/` lub `TODO/` → `sprawdz`. Wynik musi być
  „Wszystkie linki OK.”
- Po ręcznym przeniesieniu (albo gdy ktoś przeniósł plik w Obsidianie/VS Code) →
  `napraw`, potem `sprawdz`.

## Zasady linkowania (co musi być linkiem)

Każde odwołanie do czegoś, co istnieje w repo, jest linkiem ze **ścieżką względną od
bieżącego pliku**, nie zwykłym tekstem (przykłady poniżej z perspektywy pliku w `docs/`
lub `TODO/`):
- zadanie: `[0003](../TODO/ZROBIONE/0003-wybor-stosu/todo.md)`, a nie „zadanie 0003”,
- ADR: `[ADR-0002](../docs/decyzje/0002-stos-python-pyside6.md)`, a nie samo „ADR-0002”,
- kolumna „Zależy od” na tablicy i pole `zalezy_od` → w treści zadania link do zadania,
- dokument, integracja, plik kodu, zrzut, raport testów.

Nie linkujemy tylko w blokach kodu i w przykładach (w `inline code`) — skrypt je pomija,
tak samo jak komentarze HTML `<!-- -->`.

## Czego skrypt nie sprawdza

- Linków zewnętrznych (http/https) — te sprawdzaj `curl -s -o /dev/null -w '%{http_code}' URL`.
- Kotwic nagłówków (`#sekcja`) — sprawdzany jest tylko plik docelowy.
