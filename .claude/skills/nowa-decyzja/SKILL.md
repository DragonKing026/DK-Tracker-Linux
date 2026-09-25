---
name: nowa-decyzja
description: Use when a hard-to-reverse architectural or technology decision is made or proposed in this project (stack, library choice, storage, packaging) — records it as a numbered ADR in docs/decyzje/.
---

# nowa-decyzja — ADR (Architecture Decision Record)

## Kroki

1. Numer: `ls docs/decyzje | grep -E '^[0-9]{4}-' | sort | tail -1` → +1.
2. Plik `docs/decyzje/NNNN-<slug>.md`:

   ```markdown
   ---
   noteId: "<frontmatter.py noteid>"
   tytul: <Decyzja>
   tags: [adr]
   status: proponowana | zaakceptowana | odrzucona | zastapiona
   zastapiona_przez:
   utworzono: <RRRR-MM-DD GG:MM>
   zaktualizowano: <RRRR-MM-DD GG:MM>
   ---

   # ADR-NNNN: <Decyzja>

   ## Kontekst          — problem, ograniczenia, wymagania
   ## Rozważane opcje   — tabela: opcja / zalety / wady
   ## Decyzja           — co wybraliśmy (jednym zdaniem pogrubionym)
   ## Uzasadnienie      — dlaczego
   ## Konsekwencje      — co zyskujemy, co tracimy, co trzeba zrobić dalej
   ## Powiązane         — zadania, integracje
   ```
3. Decyzję ze statusem `zaakceptowana` może nadać tylko użytkownik (lub wprost ją
   zaakceptować w rozmowie). Agent tworzy ADR jako `proponowana`.
4. Zastępując decyzję — nie usuwaj starej: ustaw `status: zastapiona` i `zastapiona_przez`.
5. Dodaj wiersz do `docs/decyzje/README.md`.
6. Commit: `docs(adr): <zaproponuj|zaakceptuj> ADR-NNNN <slug>`.
