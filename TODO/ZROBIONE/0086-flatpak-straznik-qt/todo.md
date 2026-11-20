---
noteId: "b09f0e89c9744d95b369a3b6d6f9fad2"
tytul: "Ochrona paczki przed aktualizacją Qt w runtime"
numer: "0086"
status: zrobione
priorytet: p2
tags: [todo, flatpak, ci]
zalezy_od: ["0085-flatpak-qt-6-11-3"]
utworzono: 2026-11-02 17:13
zaktualizowano: 2026-11-20 11:42
zamknieto: 2026-11-20 11:42
---

# 0086 — Ochrona paczki przed aktualizacją Qt w runtime

> [!info] Status
> **zrobione** · priorytet **p2** · [← tablica zadań](../../README.md)

## Cel

Skrócić czas, przez który aktualizacja Qt w runtime'ie zostawia użytkowników z niedziałającą paczką.

## Kontekst

- Awaria z [0085](../0085-flatpak-qt-6-11-3/todo.md) może wrócić przy każdej łatce Qt
  ([pułapka w dokumentacji Flatpaka](../../../docs/integracje/flatpak.md)).
- Zgłoszenie: [issue #3](https://github.com/DragonKing026/DK-Tracker-Linux/issues/3).
- Warianty do decyzji użytkownika: codzienne sprawdzanie w CI z automatyczną przebudową, gdy BaseApp ma już wersję Qt
  z runtime'u (nie zamyka przerwy do pojawienia się BaseApp), albo Qt dołączone do paczki (usuwa problem, ale większa
  paczka i nowy projekt integracji z pulpitem i `layer-shell-qt`).

## Kryteria akceptacji

- [x] Wybrany wariant zapisany jako decyzja — [ADR-0008](../../../docs/decyzje/0008-qt-w-paczce-flatpak.md)
- [x] Rozjazd wersji Qt wykrywany bez zgłoszenia od użytkownika — Qt w paczce usuwa rozjazd; strażnik
  [straznik.yml](../../../.github/workflows/straznik.yml) codziennie uruchamia samotest wydanej paczki
- [x] Dokumentacja zaktualizowana

## Kroki

- [x] Decyzja użytkownika o wariancie — oba: Qt w paczce i strażnik
- [x] Weryfikacja koła PySide6 (moduły, wtyczka Wayland, ICU) i oficjalnych binariów Qt (nagłówki dla layer-shell-qt)
- [x] Manifest na `org.freedesktop.Platform` 26.08, krb5, przycięcie Qt
- [x] Samotest [selfcheck.py](../../../src/dk_tracker/ui/selfcheck.py), strażnik
  [straznik.py](../../../flatpak/straznik.py) z testami
- [x] Test na żywo na KDE (tacka, okno przy tacce, portfel, Kimai) i wydanie 0.10.20

## Materiały

Brak.

## Dziennik

### 2026-11-02 17:13

- Utworzono zadanie.

### 2026-11-20

- **10:21** Decyzja użytkownika: oba warianty — Qt dołączone do paczki (PySide6 z PyPI na org.freedesktop.Platform) i
  strażnik w CI. Start od weryfikacji wheela PySide6.
- **10:36** Pierwszy build przeszedł, ale samotest w paczce: `ImportError: libgssapi_krb5.so.2` — runtime freedesktop
  nie ma Kerberosa, a QtNetwork z koła go linkuje. Dodany moduł krb5 1.22.2 (z `WARN_CFLAGS=-Wall`, bo GCC z SDK 26.08
  łamie `-Werror=discarded-qualifiers`).
- **10:50** Paczka 0.10.20: bundle 47 MB (było 71 MB), po instalacji 208 MB; samotest w kontenerze: Qt 6.11.3, okno
  główne z QML, `layer-shell-qt` ładuje się.
- **10:55** Test na żywo (KDE Plasma, Wayland): tacka, okno `layer`, token z portfela, Kimai — użytkownik: „Wszystko
  gra”.
- **11:05** Wydanie z tagu przerwał niestabilny test (zapis rozmiaru okna w wątku Kimai bez `h.settle()`) — poprawiony.
- **11:15** Ponowienie padło na budowie w CI: runtime'y preinstalowane w obrazie `freedesktop-26.08` nie dają się
  zaktualizować (`Invalid cross-device link`). Workflowy budują na pustej instalacji (`FLATPAK_SYSTEM_DIR`), tag
  `v0.10.20` (nic z niego nie wyszło) przeniesiony na commit z poprawką.
- **11:40** Wydanie 0.10.20 opublikowane; strona 0.10.19 usunięta (tag został); u użytkownika 0.10.20 z repozytorium
  `dk-tracker`.
- **11:42** Wydanie 0.10.20 z Qt w paczce i strażnik; issue #3 zamknięte.

## Wynik

- Qt w paczce: [ADR-0008](../../../docs/decyzje/0008-qt-w-paczce-flatpak.md),
  [manifest](../../../flatpak/io.github.dragonking026.DK-Tracker-Linux.yml),
  [Flatpak](../../../docs/integracje/flatpak.md#qt-w-paczce-adr-0008); wydanie 0.10.20.
- Strażnik: [straznik.yml](../../../.github/workflows/straznik.yml), [straznik.py](../../../flatpak/straznik.py),
  opis w [GitHub Actions](../../../docs/integracje/github-actions.md#strażnik-qt). W repozytorium włączone „Allow
  GitHub Actions to create and approve pull requests”.
- Samotest: `flatpak run --command=python3 io.github.dragonking026.DK-Tracker-Linux -m dk_tracker.ui.selfcheck`.
- Issue [#3](https://github.com/DragonKing026/DK-Tracker-Linux/issues/3) zamknięte.
