---
noteId: "0b0085cf5ff34570a69f31d3a27253e6"
tytul: "Ustalenia prototypu 0004 — tacka i okno"
tags: [prototyp, tray, wayland, kde]
utworzono: 2026-09-25 20:02
zaktualizowano: 2026-09-25 20:02
---

# Ustalenia prototypu 0004

Prototyp: [prototyp/tray_demo.py](../prototyp/tray_demo.py) (do wyrzucenia). Środowisko:
Fedora 44, **KDE Plasma 6.7.5, Wayland**, monitor 2560×1440, PySide6 / Qt 6.11.2 (lokalnie,
jeszcze nie we Flatpaku). Kliknięcia symulowane metodą `Activate` obiektu SNI przez D-Bus,
czyli tą samą, którą wywołuje panel Plasmy.

## KDE Plasma (Wayland) — sprawdzone automatycznie

| Pytanie | Wynik | Dowód |
|---|---|---|
| Czy `QSystemTrayIcon` pokazuje ikonę? | **tak** — `tray_available: true`, SNI zarejestrowany (`Category=ApplicationStatus`, `Status=Active`, `ItemIsMenu=false`, menu przez `/MenuBar` = dbusmenu) | [log](../testy/log-kde-tool.jsonl), ![ikona](../zrzuty/kde-tacka-ikona.png) |
| Lewy klik → okno? | **tak** — `Activate` daje `ActivationReason.Trigger`, okno się pokazuje i dostaje fokus (`active: true`) | [log](../testy/log-kde-tool.jsonl) |
| Czy aplikacja zna pozycję ikony / okna? | **nie** — `tray.geometry()` = 0,0,0,0, pozycja okna z Qt = 0,0 (Wayland) | [log](../testy/log-kde-tool.jsonl) |
| Gdzie KWin stawia okno bezramkowe (wariant A)? | **na środku ekranu** (460×560, środek x=1279 na 2560) | ![okno A](../zrzuty/kde-tool-okno.png) |
| Tooltip z czasem timera | **odświeża się co sekundę** (`Kimai Tray — 0:00:22 — …` → `0:00:24`); tekst trafia do tytułu tooltipa SNI | [log](../testy/log-kde-layer.jsonl) |
| Zmiana ikony (szara → zielona) | **działa** | ![okno B](../zrzuty/kde-layer-okno.png) |
| Wariant B: `layer-shell-qt` z Pythona | **działa** — PySide nie ma wiązań, ale `LayerShellQt::Window::get(QWindow*)` przez `ctypes` + `setProperty` (anchors, layer, keyboardInteractivity, margins, scope) ustawia wszystko (`set_ok: true`); odczyt enumów z PySide niemożliwy (brak konwertera) — bez znaczenia | [log](../testy/log-kde-layer.jsonl) |
| Gdzie stoi okno w wariancie B? | **prawy dolny róg, tuż nad panelem**: 12 px od prawej (margines), 60 px od dołu (12 px + panel — kompozytor respektuje strefę panelu) | ![okno B](../zrzuty/kde-layer-okno.png) |

## Do sprawdzenia ręcznie (wymaga prawdziwego kliknięcia)

- Kolizja: kliknięcie ikony przy otwartym oknie (fokus → panel → okno się chowa → `Trigger` pokazuje je znowu?).
- Czy okno wariantu B chowa się po kliknięciu gdzie indziej (warstwa `layer-shell` może nie dostawać `WindowDeactivate`).
- Czy w oknie wariantu B da się pisać (`keyboardInteractivity=OnDemand`).
- Menu kontekstowe (prawy klik) — pozycja przy ikonie.

## Nie sprawdzone (zablokowane)

- **Flatpak** — wymaga pobrania `org.kde.Sdk//6.11` (1,2 GB) i `io.qt.PySide.BaseApp//6.11` (346 MB); czeka na zgodę użytkownika.
- **GNOME** — na tej maszynie nie ma GNOME Shell (ani rozszerzenia AppIndicator).

## Wnioski (wstępne)

- Wariant B jest technicznie osiągalny z PySide bez kompilacji — ważne dla ADR-0003.
- Konsekwencja wariantu B: `QT_WAYLAND_SHELL_INTEGRATION=layer-shell` działa dla **całego procesu**
  (każde okno staje się powierzchnią warstwy) — okno ustawień musiałoby być osobnym procesem
  albo zmienna ustawiana tylko dla okna szybkiej obsługi (do zbadania).
- `layer-shell-qt` nie jest w `org.kde.Platform` — we Flatpaku trzeba go dołożyć modułem albo
  wziąć z hosta (nie da się). Do sprawdzenia przy budowie Flatpaka.
