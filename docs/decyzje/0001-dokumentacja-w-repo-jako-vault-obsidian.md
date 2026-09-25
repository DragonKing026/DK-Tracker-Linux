---
noteId: "c4cae3aae36d410786652c4a79b786cf"
tytul: Dokumentacja i zadania w repo jako vault Obsidiana
tags: [adr, dokumentacja, proces]
status: zaakceptowana
zastapiona_przez:
utworzono: 2026-09-25 17:18
zaktualizowano: 2026-09-25 17:47
---

# ADR-0001: Dokumentacja i zadania w repo jako vault Obsidiana

## Kontekst

Użytkownik chce pełnej, bieżącej dokumentacji projektu, zadań rozpisanych jako foldery
z plikami przyjaznymi Obsidianowi, zrzutów i diagramów w plikach oraz historii w gicie.
Pracę wykonują w dużej mierze agenci AI, którzy muszą szybko odnaleźć kontekst.

## Rozważane opcje

| Opcja | Zalety | Wady |
| --- | --- | --- |
| Markdown w repo, format Obsidiana | wersjonowane z kodem, czytelne dla agentów i ludzi, graf linków, działa offline | wikilinki nie są klikalne na GitHubie |
| Zewnętrzna wiki / Notion / Jira | wygodne dla nietechnicznych | rozjeżdża się z kodem, agent nie ma dostępu offline |
| Tylko README + komentarze w kodzie | minimum pracy | brak miejsca na decyzje, integracje, zadania |

## Decyzja

**Cała dokumentacja (`docs/`) i zadania (`TODO/`) żyją w repozytorium jako Markdown
w konwencji Obsidiana (frontmatter, callouty, mermaid) z względnymi linkami markdown.**

## Uzasadnienie

Dokumentacja zmienia się w tych samych commitach co kod, więc nie traci aktualności;
agent czyta ją bez dodatkowych narzędzi; użytkownik przegląda ją w Obsidianie.

## Konsekwencje

- **Rewizja 2026-09-25:** początkowo używaliśmy wikilinków `[[...]]`. Na prośbę
  użytkownika zastąpiono je względnymi linkami markdown, które działają też w VS Code
  i na GitHubie. Spójność linków pilnuje skill `sprawdz-linki`.
- Każda zmiana zachowania wymaga aktualizacji docs (reguła w [AGENTS.md](../../AGENTS.md)).
- Zrzuty ekranu zwiększają rozmiar repo — trzymamy PNG w rozsądnej rozdzielczości.

## Powiązane

- [Zasady dokumentowania](../procesy/dokumentowanie.md)
- [Zadania w TODO](../procesy/zadania.md)
