---
tytul: "Prototyp: ikona w tacce i okno na KDE i GNOME we Flatpaku"
numer: "0004"
status: do-zrobienia
priorytet: p1
tagi: [todo, spike, tray, wayland]
zalezy_od: ["0003-wybor-stosu"]
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
zamknieto:
---

# 0004 — Prototyp tacki i okna (spike)

> [!info] Status
> **do-zrobienia** · priorytet **p1** · [[TODO/README|← tablica zadań]]

## Cel

Sprawdzić najbardziej ryzykowne założenia przed pisaniem właściwej aplikacji.
Kod prototypu jest do wyrzucenia — wynikiem są odpowiedzi i zrzuty ekranu.

## Pytania do sprawdzenia

- [ ] Ikona SNI z `QSystemTrayIcon` (PySide6, [[docs/decyzje/0002-stos-python-pyside6|ADR-0002]]) pojawia się we Flatpaku z samym
      `--talk-name=org.kde.StatusNotifierWatcher` (bez `--own-name`)
- [ ] Lewy klik → okno; prawy klik → menu — na Plasmie 6 Wayland
- [ ] Gdzie pojawia się okno na Waylandzie i czy da się je sensownie zakotwiczyć
- [ ] Zmiana ikony/tooltipu co minutę (czas timera) jest widoczna
- [ ] GNOME + AppIndicator: ikona, klik, tooltip/etykieta
- [ ] GNOME bez rozszerzenia: wykrycie braku watchera i tryb okna
- [ ] Zapis/odczyt sekretu przez libsecret w piaskownicy (KWallet)

## Diagramy i zrzuty

Zrzuty z każdego pulpitu → `assets/`.

## Dziennik

### 2026-09-25
- Utworzono zadanie.
- Stos wybrany (0003 zamknięte) → status do-zrobienia.

## Wynik
