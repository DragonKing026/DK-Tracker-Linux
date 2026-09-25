---
name: nowa-integracja
description: Use before adding any external dependency, API, library, system service or protocol to this project — creates docs/integracje/<slug>.md with verified facts and links to official documentation, and registers it in the integrations index.
---

# nowa-integracja — dokument integracji

Każda integracja zewnętrzna (API Kimai, biblioteka UI, D-Bus/tacka, portal Flatpaka,
magazyn sekretów…) ma **osobny plik** w `docs/integracje/`. Bez niego nie dodajemy zależności.

## Kroki

1. **Zbierz fakty ze źródeł** — Context7 (`resolve-library-id` → `query-docs`) albo
   oficjalna dokumentacja przez WebFetch. Nie pisz z pamięci. Zanotuj wersję, której dotyczy.
2. **Utwórz** `docs/integracje/<slug>.md` według struktury:

   ```markdown
   ---
   noteId: "<frontmatter.py noteid>"
   tytul: <Nazwa>
   tags: [integracja, <obszar>]
   status_integracji: planowana | w-uzyciu | porzucona
   wersja: <wersja/zakres wersji, jeśli dotyczy>
   utworzono: <data>
   zaktualizowano: <data>
   ---

   # <Nazwa>

   > [!info] W skrócie
   > Jedno zdanie: czym jest i po co nam.

   ## Do czego używamy
   ## Jak to działa (z diagramem mermaid, jeśli jest przepływ)
   ## Konfiguracja / uprawnienia (np. finish-args Flatpaka)
   ## Pułapki i ograniczenia   ← z callout [!warning]
   ## Gdzie w kodzie           ← ścieżki modułów (po implementacji)
   ## Dokumentacja             ← lista linków do oficjalnych źródeł
   ## Powiązane                ← linki markdown do ADR, zadań, innych integracji
   ```
3. **Indeks** — dodaj wiersz w `docs/integracje/README.md` (tabela integracji).
4. **Linki**: `python3 .claude/skills/sprawdz-linki/linki.py sprawdz`.
5. **Commit**: `docs(integracje): opisz <nazwa>`.

## Sprawdź

- [ ] każdy fakt o zewnętrznym systemie ma link do źródła
- [ ] sekcja „Pułapki” nie jest pusta (jeśli naprawdę brak — napisz to wprost)
