---
tytul: Zasady dokumentowania
tagi: [proces, dokumentacja, obsidian]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
---

# Zasady dokumentowania

Repozytorium jest jednocześnie **vaultem Obsidiana** — można je otworzyć w Obsidianie
(„Open folder as vault”) i nawigować po wikilinkach, grafie i tagach.
Pliki muszą też czytelnie renderować się na GitHubie.

## Co dokumentujemy i gdzie

| Co | Gdzie | Kiedy |
|---|---|---|
| Jak działa aplikacja, komponenty, przepływy | `docs/architektura/` | przy każdej zmianie struktury lub zachowania |
| Integracje zewnętrzne (API, biblioteki, usługi systemowe) | `docs/integracje/<nazwa>.md` | przed dodaniem zależności |
| Decyzje („wybraliśmy X zamiast Y, bo…”) | `docs/decyzje/NNNN-<slug>.md` (ADR) | gdy decyzja jest trudna do cofnięcia |
| Procesy pracy | `docs/procesy/` | gdy zmienia się sposób pracy |
| Zadania, postęp, notatki robocze | `TODO/<NNNN-slug>/todo.md` | cały czas |
| Zrzuty ekranu, obrazy | `docs/assets/` albo `TODO/<zadanie>/assets/` | przy każdej zmianie UI |

## Szablon nagłówka (frontmatter)

```yaml
---
tytul: Krótki tytuł
tagi: [obszar, temat]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
---
```

Zmieniając plik — aktualizuj `zaktualizowano`.

## Elementy formatowania

- **Wikilinki**: `[[docs/integracje/kimai-api|Kimai API]]` — ścieżka od korzenia repo.
- **Callouty**:
  ```markdown
  > [!warning] Uwaga
  > Token API pokazywany jest w Kimai tylko raz.
  ```
  Dostępne: `note`, `tip`, `info`, `warning`, `danger`, `todo`, `question`, `example`.
- **Diagramy**: bloki `mermaid` (flowchart, sequenceDiagram, stateDiagram-v2, classDiagram,
  gantt). Preferujemy je nad obrazkami, bo są wersjonowane jako tekst.
- **Zrzuty ekranu**: plik PNG w `assets/`, osadzenie `![[nazwa.png]]` (Obsidian) —
  dodatkowo pod spodem zwykły link `![opis](assets/nazwa.png)` dla GitHuba nie jest
  wymagany, ale zalecany w README.
- **Tabele** do porównań, **listy zadań** `- [ ]` do kroków.

## Zasady treści

1. Pisz **dlaczego**, nie tylko **co**. Kod pokazuje co, dokumentacja wyjaśnia decyzje.
2. Każde twierdzenie o zewnętrznym API/bibliotece — z linkiem do źródła.
3. Każdy opis komponentu odpowiada na: *co robi*, *jak się go używa*, *od czego zależy*.
4. Dokument nieaktualny jest gorszy niż brak dokumentu — aktualizuj razem z kodem.

## Powiązane

- [[docs/procesy/commity|Konwencja commitów]]
- [[docs/procesy/zadania|Zadania w TODO]]
- [Obsidian — formatowanie](https://help.obsidian.md/Editing+and+formatting/Basic+formatting+syntax)
- [Obsidian — callouty](https://help.obsidian.md/Editing+and+formatting/Callouts)
- [Mermaid — składnia](https://mermaid.js.org/intro/syntax-reference.html)
