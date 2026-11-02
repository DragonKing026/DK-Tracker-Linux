---
noteId: "b09f0e89c9744d95b369a3b6d6f9fad2"
tytul: "Ochrona paczki przed aktualizacją Qt w runtime"
numer: "0086"
status: pomysl
priorytet: p2
tags: [todo, flatpak, ci]
zalezy_od: ["0085-flatpak-qt-6-11-3"]
utworzono: 2026-11-02 17:13
zaktualizowano: 2026-11-02 17:13
zamknieto:
---

# 0086 — Ochrona paczki przed aktualizacją Qt w runtime

> [!info] Status
> **pomysl** · priorytet **p2** · [← tablica zadań](../../README.md)

## Cel

Skrócić czas, przez który aktualizacja Qt w runtime'ie zostawia użytkowników z niedziałającą paczką.

## Kontekst

- Awaria z [0085](../../ZROBIONE/0085-flatpak-qt-6-11-3/todo.md) może wrócić przy każdej łatce Qt
  ([pułapka w dokumentacji Flatpaka](../../../docs/integracje/flatpak.md)).
- Zgłoszenie: [issue #3](https://github.com/DragonKing026/DK-Tracker-Linux/issues/3).
- Warianty do decyzji użytkownika: codzienne sprawdzanie w CI z automatyczną przebudową, gdy BaseApp ma już wersję Qt
  z runtime'u (nie zamyka przerwy do pojawienia się BaseApp), albo Qt dołączone do paczki (usuwa problem, ale większa
  paczka i nowy projekt integracji z pulpitem i `layer-shell-qt`).

## Kryteria akceptacji

- [ ] Wybrany wariant zapisany jako decyzja
- [ ] Rozjazd wersji Qt wykrywany bez zgłoszenia od użytkownika
- [ ] Dokumentacja zaktualizowana

## Kroki

- [ ] Decyzja użytkownika o wariancie

## Materiały

Brak.

## Dziennik

### 2026-11-02 17:13

- Utworzono zadanie.

## Wynik

<!-- Wypełniane przy zamknięciu: co powstało, gdzie, co zostało na później. -->
