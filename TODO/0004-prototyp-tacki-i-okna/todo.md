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
> **do-zrobienia** · priorytet **p1** · [← tablica zadań](../README.md)

## Cel

Sprawdzić najbardziej ryzykowne założenia przed pisaniem właściwej aplikacji.
Kod prototypu jest do wyrzucenia — wynikiem są odpowiedzi i zrzuty ekranu.

## Pytania do sprawdzenia

- [ ] Ikona SNI z `QSystemTrayIcon` (PySide6, [ADR-0002](../../docs/decyzje/0002-stos-python-pyside6.md)) pojawia się we Flatpaku z samym
      `--talk-name=org.kde.StatusNotifierWatcher` (bez `--own-name`)
- [ ] Lewy klik → okno; prawy klik → menu — na Plasmie 6 Wayland
- [ ] Wariant A ([ADR-0003](../../docs/decyzje/0003-okno-szybkiej-obslugi-na-wayland.md)): bezramkowe okno
      narzędziowe — gdzie je stawia KWin / Mutter, czy chowanie po utracie fokusu działa
- [ ] Kolizja: klik w ikonę zabiera fokus → okno się chowa → `Trigger` pokazuje je znowu?
- [ ] Reguła okna KWin (pozycja przy panelu) — czy da się ją podpowiedzieć użytkownikowi
- [ ] Wariant B: `layer-shell-qt` jako moduł w manifeście Flatpaka — czy da się zbudować
      i zakotwiczyć okno przy panelu Plasmy; decyzja: dokładamy albo porzucamy
- [ ] Zmiana ikony/tooltipu co minutę (czas timera) jest widoczna
- [ ] GNOME + AppIndicator: ikona, klik, tooltip/etykieta
- [ ] GNOME bez rozszerzenia: wykrycie braku watchera i tryb okna
- [ ] Zapis/odczyt sekretu przez libsecret w piaskownicy (KWallet)

## Materiały

- `prototyp/` — kod spike'a (do wyrzucenia)
- `zrzuty/` — zrzuty z każdego pulpitu, np. `kde-tacka.png`, `gnome-appindicator.png`
- `testy/` — raport z odpowiedziami na pytania i logi uruchomień
- `notatki/` — ustalenia o `layer-shell-qt`

## Dziennik

### 2026-09-25
- Utworzono zadanie.
- Stos wybrany (0003 zamknięte) → status do-zrobienia.
- ADR-0003: dodano pytania o wariant A i B okna.

## Wynik
