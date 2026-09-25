---
noteId: "3bd05b294c5f44a1b6bd803bbe09249e"
tytul: "Drobne uwagi z recenzji Planu 2 (desktop)"
numer: "0027"
status: w-trakcie
priorytet: p3
tags: [todo, desktop, recenzja]
zalezy_od: ["0026"]
utworzono: 2026-09-25 21:06
zaktualizowano: 2026-09-25 21:10
---

# 0027 — Drobne uwagi z recenzji Planu 2 (desktop)

> [!info] Status
> **w-trakcie** · priorytet **p3** · [← tablica zadań](../../README.md)

## Cel

Zdecydować z użytkownikiem, które drobne uwagi z końcowej recenzji Planu 2 poprawić (teraz, w Planie 3
albo wcale). Recenzja: model opus, commity `6ed7042..577cd54`, 0 krytycznych, 1 ważna, 9 drobnych.
Ważną (I1: surowe wyjątki z usługi sekretów, wygasła sesja) poprawiono w commicie `0cbd5e9`.

## Kontekst

- [Plan 2](../../../docs/plany/2026-09-25-plan-2-desktop.md), [specyfikacja](../../../docs/specyfikacja/2026-09-25-kimai-tray-1.0.md)
- Kod: [src/kimai_tray/desktop/](../../../src/kimai_tray/desktop/), [notification_policy.py](../../../src/kimai_tray/core/notification_policy.py)
- Rozpoznanie API: [rozpoznanie.md](../../ZROBIONE/0021-plan2-rozpoznanie-api-desktop/notatki/rozpoznanie.md)

## Kryteria akceptacji

- [ ] Każda uwaga: poprawiona (test RED→GREEN), przeniesiona do Planu 3 albo świadomie odrzucona z uzasadnieniem w dzienniku

## Kroki (uwagi odłożone)

- [ ] **M1** `entry_id_from` używa `str.isdigit()` — przepuszcza np. „²”, potem `int()` rzuca `ValueError`. Identyfikatory nadajemy sami, więc ryzyko znikome. Poprawka: `re.fullmatch(r"[0-9]+", …)`.
- [ ] **M2** `SecretServiceStore.get`: surowy `KeyError`, gdy `GetSecrets` pominie wpis (wyścig z usunięciem), i `UnicodeDecodeError` przy sekrecie nie-UTF-8. Poprawka: `.get()` → `None`; błąd dekodowania → `None` albo `SecretsUnavailable`.
- [ ] **M3** `portal_request` po przekroczeniu czasu nie wywołuje `Request.Close` (okno portalu może zostać) i nie porównuje zwróconego uchwytu z oczekiwanym.
- [ ] **M4** Po przekroczeniu czasu okna odblokowania portfela nie wołamy `Prompt.Dismiss` — okno zostaje na ekranie.
- [ ] **M5** `_JeepneyExpectation.close()` nie jest idempotentne — drugie wywołanie rzuca `KeyError` (ważne przy zamykaniu w Planie 3).
- [ ] **M6** Odpowiedź na `AddMatch` nie jest sprawdzana — przy błędzie `wait` czeka do końca limitu czasu.
- [ ] **M7** Reguły dopasowania bez `sender` — dowolny proces sesji może podrobić `ActionInvoked` (np. „stop”). Wymaga unikalnej nazwy portalu z `GetNameOwner`.
- [ ] **M8** `listen()` działa na tej samej szynie co `show()` — Plan 3 musi dać nasłuchowi osobne połączenie (jedno na wątek) i sprawdzić, czy `ActionInvoked` do niego dociera.
- [ ] **M9** Brakujące testy: `get` przy dwóch pasujących wpisach, przekroczenie czasu okna odblokowania, ścieżka `set` przy braku usługi.

## Materiały

## Dziennik

### 2026-09-25
- **21:06** Utworzono z końcowej recenzji Planu 2.
- **21:10** Start: techniczne uwagi poprawiam sam, decyzje produktowe do omówienia z użytkownikiem.
