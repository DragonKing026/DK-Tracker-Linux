---
noteId: "ef7876ae9f35445294f486428763a4f6"
tytul: "Awaria po kliknięciu ikony: pętla rozmiaru płótna"
numer: "0076"
status: w-trakcie
priorytet: p0
tags: [todo, bug, okno-przy-tacce, awaria]
zalezy_od: ["0066-plotno-okna-przy-tacce"]
utworzono: 2026-09-28 10:30
zaktualizowano: 2026-09-28 10:42
zamknieto:
---

# 0076 — Awaria po kliknięciu ikony: pętla rozmiaru płótna

> [!info] Status
> **w-trakcie** · priorytet **p0** · [← tablica zadań](../../README.md)

## Cel

Kliknięcie ikony w tacce nie wywraca aplikacji (SIGSEGV), gdy zawartość okna jest wyższa niż zapamiętany panel.

## Kontekst

- Zgłoszenie użytkownika 2026-09-28 10:30: 0.10.7 z Flatpaka pada przy każdym kliknięciu ikony
  (`QWaylandShmBuffer: failed: Zły argument`, potem SIGSEGV w QtGui).
- Pomiar ([log](testy/diagnoza-flatpak.log)): panel 630×420 (zapamiętany), minimum zawartości 513 px (formularz 306 px).
  Układ okna z `SetDefaultConstraint` wymusza minimum okna = górny margines + minimum zawartości, a górny margines
  płótna ([0066](../../ZROBIONE/0066-plotno-okna-przy-tacce/todo.md)) to „wysokość płótna − panel”. Okno rośnie
  o 93 px, margines też — bez końca, aż bufor Waylanda nie powstaje.
- Ten sam błąd w kodzie 0.10.6 uruchomionym w tym samym Flatpaku — to nie regresja z
  [0075](../../ZROBIONE/0075-okno-na-ekranie-kliknietej-tacki/todo.md), tylko ukryty błąd płótna.

## Kryteria akceptacji

- [x] Test: zawartość wyższa niż panel nie powiększa płótna; panel rośnie do minimum zawartości (w granicach płótna)
- [ ] Flatpak / system: kliknięcie ikony przy tym stanie nie wywraca aplikacji
- [x] Dokumentacja zaktualizowana
- [x] Wydanie z poprawką

## Kroki

- [x] W trybie płótna układ nie ustala minimum okna (`SetNoConstraint`)
- [x] Panel nie niższy niż minimum zawartości; także gdy zawartość rośnie (LayoutRequest)
- [x] Wydanie 0.10.8

## Materiały

- [testy/diagnoza-flatpak.log](testy/diagnoza-flatpak.log) — rozmiary okna i układu w pętli (Flatpak 0.10.7)

## Dziennik

### 2026-09-28 10:30

- Utworzono zadanie. Przyczyna ustalona pomiarem w Flatpaku (A/B: z i bez `wantsToBeOnActiveScreen`, kod 0.10.6
  i 0.10.7 w tym samym środowisku — pętla wszędzie).
- **10:30** Start pracy.

### 2026-09-28 10:42

- Poprawka `1776709` (test pada bez niej), dokumentacja `65ccb9c`
  ([layer-shell-qt](../../../docs/integracje/layer-shell-qt.md)), wydanie 0.10.8 `22e0671`; strona 0.10.7 usunięta.
- Zainstalowana 0.10.8 z zapamiętanym stanem użytkownika: pokaż/schowaj ×2 bez awarii (jedna zmiana rozmiaru płótna).
  Czeka na potwierdzenie prawdziwym kliknięciem ikony.

## Wynik

<!-- Wypełniane przy zamknięciu: co powstało, gdzie, co zostało na później. -->
