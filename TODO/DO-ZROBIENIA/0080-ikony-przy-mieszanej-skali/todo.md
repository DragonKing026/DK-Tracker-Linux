---
noteId: "966633a532224c8ca18386fe5b14c5a1"
tytul: "Ikony okna przesunięte i za duże przy ekranach o różnej skali"
numer: "0080"
status: do-zrobienia
priorytet: p1
tags: [todo, wyglad, ikony]
zalezy_od: []
utworzono: 2026-10-09 16:33
zaktualizowano: 2026-10-09 16:33
zamknieto:
---

# 0080 — Ikony okna przesunięte i za duże przy ekranach o różnej skali

> [!info] Status
> **do zrobienia** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Ikony okna głównego (pasek boczny, strzałki list, zegar, znak DK) mają swój rozmiar i są wyśrodkowane
na każdym ekranie, także gdy w sesji jest ekran o innej skali.

## Kontekst

- Zgłoszenie użytkownika w 0.10.16: ikony „po przesuwane” — za duże, zjechane w dół i w prawo, zębatka
  ustawień wystaje poza przycisk.
- Sesja KDE Wayland ma wirtualny ekran „Telefon” ze skalą 2, a okno stoi na DP-6 ze skalą 1.
  `QGuiApplication.devicePixelRatio()` to wtedy 2.
- Dostawca `image://glyph` / `image://icons` w
  [window.py](../../../src/dk_tracker/ui/main_window/window.py) zwracał `QIcon.pixmap()` (skala aplikacji,
  czyli 2×), a `mark()` w [icons.py](../../../src/dk_tracker/ui/icons.py) rysuje zawsze 2×. Qt Quick bierze
  rozmiar pixmapy od dostawcy dosłownie, więc ikona wychodziła większa niż `sourceSize`. Do tego minimum 16 px
  powiększało kłódkę 12 px.
- Powiązane: [wygląd okna głównego](../../../docs/architektura/wyglad-okna-glownego.md).

## Kryteria akceptacji

- [ ] Dostawca zwraca pixmapę dokładnie w żądanym rozmiarze (bez skali aplikacji, bez minimum 16 px).
- [ ] Obrazy ikon w QML mają jawny rozmiar, więc nie rosną nawet przy większej pixmapie.
- [ ] Test: dostawca zwraca żądany rozmiar.
- [ ] Wydanie z poprawką, sprawdzone u użytkownika.

## Kroki

- [ ] Dostawca ikon: rysowanie w żądanym rozmiarze.
- [ ] QML: jawne `width`/`height` ikon.
- [ ] Test, zrzuty, wydanie.

## Materiały

![Przed poprawką: ikony za duże i przesunięte](zrzuty/przed-ikony-przesuniete.png)

## Dziennik

### 2026-10-09 16:33

- Utworzono zadanie. Przyczyna ustalona przez `kscreen-doctor -o`: ekran „Telefon” ze skalą 2.

## Wynik

<!-- Wypełniane przy zamknięciu: co powstało, gdzie, co zostało na później. -->
