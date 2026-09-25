---
noteId: "e731518efd584a658c5e1da8c9e7d5d8"
tytul: "Prototyp: ikona w tacce i okno na KDE i GNOME we Flatpaku"
numer: "0004"
status: zrobione
priorytet: p1
tags: [todo, spike, tray, wayland]
zalezy_od: ["0003-wybor-stosu"]
utworzono: 2026-09-25 17:24
zaktualizowano: 2026-09-25 20:39
zamknieto: 2026-09-25 20:39
---

# 0004 — Prototyp tacki i okna (spike)

> [!info] Status
> **zrobione** · priorytet **p1** · [← tablica zadań](../../README.md)

## Cel

Sprawdzić najbardziej ryzykowne założenia przed pisaniem właściwej aplikacji.
Kod prototypu jest do wyrzucenia — wynikiem są odpowiedzi i zrzuty ekranu.

## Pytania do sprawdzenia

- [x] Ikona SNI z `QSystemTrayIcon` (PySide6, [ADR-0002](../../../docs/decyzje/0002-stos-python-pyside6.md)) pojawia się
      we Flatpaku z samym
      `--talk-name=org.kde.StatusNotifierWatcher` (bez `--own-name`)
- [x] Lewy klik → okno; prawy klik → menu — na Plasmie 6 Wayland
- [x] Wariant A ([ADR-0003](../../../docs/decyzje/0003-okno-szybkiej-obslugi-na-wayland.md)): bezramkowe okno
      narzędziowe — gdzie je stawia KWin / Mutter, czy chowanie po utracie fokusu działa
- [x] Kolizja: klik w ikonę zabiera fokus → okno się chowa → `Trigger` pokazuje je znowu?
- [ ] ~~Reguła okna KWin (pozycja przy panelu)~~ — **nieaktualne**: okno przy tacce przez `layer-shell` (ADR-0005),
      reguła KWin niepotrzebna
- [x] Wariant B: `layer-shell-qt` jako moduł w manifeście Flatpaka — czy da się zbudować
      i zakotwiczyć okno przy panelu Plasmy; decyzja: dokładamy albo porzucamy
- [x] Zmiana ikony/tooltipu co minutę (czas timera) jest widoczna
- [ ] GNOME + AppIndicator: ikona, klik, tooltip/etykieta → **przeniesione do
      [0020](../../DO-ZROBIENIA/0020-testy-gnome/todo.md)**
- [ ] GNOME bez rozszerzenia: wykrycie braku watchera i tryb okna → **przeniesione do
      [0020](../../DO-ZROBIENIA/0020-testy-gnome/todo.md)**
- [ ] Zapis/odczyt sekretu w piaskownicy (KWallet) — **niesprawdzone w prototypie**, przeniesione do Planu 2 (poza
      piaskownicą jeepney + ksecretd działa — ADR-0004)

## Materiały

- [prototyp/tray_demo.py](prototyp/tray_demo.py) — kod spike'a (do wyrzucenia)
- [notatki/ustalenia.md](notatki/ustalenia.md) — **wyniki**: co działa, co trzeba sprawdzić ręcznie, co zablokowane
- `zrzuty/` — wycinki (bez prywatnej zawartości pulpitu): [ikona w tacce](zrzuty/kde-tacka-ikona.png),
  [okno A — środek ekranu](zrzuty/kde-tool-okno.png), [okno B — przy panelu](zrzuty/kde-layer-okno.png)
- `testy/` — logi JSON uruchomień: [wariant A](testy/log-kde-tool.jsonl), [wariant B](testy/log-kde-layer.jsonl)

## Dziennik

### 2026-09-25

- Utworzono zadanie.
- Stos wybrany (0003 zamknięte) → status do-zrobienia.
- [ADR-0003](../../../docs/decyzje/0003-okno-szybkiej-obslugi-na-wayland.md): dodano pytania o wariant A i B okna.
- **19:56** Start spike'a: PySide6 lokalnie na Plasmie 6.7.5 Wayland, potem Flatpak.
- **20:02** KDE: tacka, klik (Trigger), tooltip co sekundę, wariant A (środek ekranu) i B (layer-shell przy panelu)
  sprawdzone automatycznie; czeka test ręczny, zgoda na pobranie SDK Flatpaka, GNOME.
- **20:39** Zamknięte: KDE i Flatpak sprawdzone, decyzje ADR-0005 i ADR-0006, GNOME → 0020.

## Wynik

Wszystkie pytania prototypu rozstrzygnięte na KDE Plasma 6.7.5 (Wayland), lokalnie i we Flatpaku —
[ustalenia](notatki/ustalenia.md):

- Tacka SNI działa we Flatpaku z samym `--talk-name=org.kde.StatusNotifierWatcher`.
- Okno na środku (bezramkowe) i okno przy tacce (`layer-shell-qt` przez `ctypes`) — oba działają;
  użytkownik wybrał okno przy tacce na KDE → [ADR-0005](../../../docs/decyzje/0005-okno-przy-tacce-na-kde.md) (zastępuje
  ADR-0003).
- Klik ikony przy otwartym oknie nie dociera do aplikacji → przycisk zamknięcia i `Esc`.
- Flatpak 1.18.2 (Fedora 44) nie buduje z `base:` → budowa w kontenerze Debian
  ([ADR-0006](../../../docs/decyzje/0006-budowanie-flatpaka-w-kontenerze.md)), paczka 70 MB, `layer-shell-qt` jako
  moduł.
- Na później: testy GNOME — zadanie [0020](../../DO-ZROBIENIA/0020-testy-gnome/todo.md) (inne osoby).
