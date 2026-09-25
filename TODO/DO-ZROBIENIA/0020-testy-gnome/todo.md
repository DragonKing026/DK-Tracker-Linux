---
noteId: "d8e697a0e5934cd78c1df9ec58540351"
tytul: "Testy ręczne na GNOME (tacka, okno, Flatpak)"
numer: "0020"
status: do-zrobienia
priorytet: p2
tags: [todo, testy, gnome]
zalezy_od: ["0004"]
utworzono: 2026-09-25 20:39
zaktualizowano: 2026-09-25 20:39
zamknieto:
---

# 0020 — Testy ręczne na GNOME

> [!info] Status
> **do-zrobienia** · priorytet **p2** · [← tablica zadań](../../README.md)

## Cel

Sprawdzić na GNOME to, co [prototyp 0004](../../ZROBIONE/0004-prototyp-tacki-i-okna/notatki/ustalenia.md)
sprawdził na KDE. Wykonują inne osoby (stacja deweloperska ma tylko KDE) — decyzja użytkownika.

## Kontekst

- [ADR-0005](../../../docs/decyzje/0005-okno-przy-tacce-na-kde.md): na GNOME okno bezramkowe (bez `layer-shell`).
- [GNOME AppIndicator](../../../docs/integracje/gnome-appindicator.md): bez rozszerzenia brak tacki.
- Najlepiej wykonać na paczce z Planu 4; wcześniej można na prototypie
  (`flatpak install --user --bundle pl.websystems.KimaiTray.Prototyp.flatpak` —
  plik z `prototyp/flatpak/buduj-w-dockerze.sh` zadania 0004).

## Kryteria akceptacji

- [ ] Fedora Workstation (GNOME) **z** rozszerzeniem AppIndicator: ikona, lewy klik → okno, prawy → menu, tooltip
- [ ] GNOME **bez** rozszerzenia: aplikacja działa jako zwykłe okno + podpowiedź o rozszerzeniu
- [ ] Ubuntu (rozszerzenie domyślnie włączone): jak wyżej
- [ ] Gdzie staje okno, czy chowa się po kliknięciu obok, czy da się pisać, co robi klik ikony przy otwartym oknie
- [ ] Wyniki i zrzuty w `testy/` i `zrzuty/` tego zadania (bez prywatnej zawartości pulpitu)

## Kroki

- [ ] Przygotować instrukcję dla testerów (instalacja paczki, lista kroków 1–5 jak w 0004)
- [ ] Zebrać wyniki

## Materiały

## Dziennik

### 2026-09-25
- **20:39** Utworzono po prototypie 0004 (GNOME niedostępny na stacji deweloperskiej).

## Wynik

<!-- Wypełniane przy zamknięciu. -->
