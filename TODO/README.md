---
noteId: "cac7a114c5cb4e29b37b72cfb350f540"
tytul: Tablica zadań
tags: [todo, tablica]
utworzono: 2026-09-25 17:14
zaktualizowano: 2026-09-28 10:30
---

# Tablica zadań

Zasady: [Zadania w folderze TODO](../docs/procesy/zadania.md) · Szablon: [_szablon](_szablon/todo.md)

Zadania leżą w podfolderach według statusu. Przy zmianie statusu folder zadania jest
przenoszony (skill [zmien-status-zadania](../.claude/skills/zmien-status-zadania/SKILL.md)).

| Folder | Statusy |
| --- | --- |
| [DO-ZROBIENIA/](DO-ZROBIENIA) | 💡 `pomysl` · 📋 `do-zrobienia` |
| [W-TRAKCIE/](W-TRAKCIE) | 🔨 `w-trakcie` · ⛔ `zablokowane` |
| [ZROBIONE/](ZROBIONE) | ✅ `zrobione` · 🗑️ `porzucone` |

<!-- tablica:start -->

## W trakcie

| Nr | Zadanie | Status | Priorytet | Zależy od |
| --- | --- | --- | --- | --- |
| 0076 | [Awaria po kliknięciu ikony: pętla rozmiaru płótna](W-TRAKCIE/0076-petla-rozmiaru-plotna/todo.md) | 🔨 w-trakcie | p0 | [0066](ZROBIONE/0066-plotno-okna-przy-tacce/todo.md) ✅ |

## Do zrobienia

| Nr | Zadanie | Status | Priorytet | Zależy od |
| --- | --- | --- | --- | --- |
| 0020 | [Testy ręczne na GNOME (tacka, okno, Flatpak)](DO-ZROBIENIA/0020-testy-gnome/todo.md) | 📋 do-zrobienia | p2 | [0004](ZROBIONE/0004-prototyp-tacki-i-okna/todo.md) ✅ |
| 0062 | [0.9.2: pełna aplikacja „DK Tracker”, tacka jako opcja — do omówienia](DO-ZROBIENIA/0062-aplikacja-ws-tracker/todo.md) | 💡 pomysl | p2 | [0056](ZROBIONE/0056-identyfikator-i-wydawca/todo.md) ✅ |

## Zrobione

| Nr | Zadanie | Status | Zamknięto |
| --- | --- | --- | --- |
| 0001 | [Struktura agenta i dokumentacji](ZROBIONE/0001-struktura-agenta-i-dokumentacja/todo.md) | ✅ zrobione | 2026-09-25 17:23 |
| 0002 | [Specyfikacja projektu (design) i plan implementacji](ZROBIONE/0002-specyfikacja-projektu/todo.md) | ✅ zrobione | 2026-09-25 19:15 |
| 0003 | [Wybór stosu technologicznego](ZROBIONE/0003-wybor-stosu/todo.md) | ✅ zrobione | 2026-09-25 17:29 |
| 0004 | [Prototyp: ikona w tacce i okno na KDE i GNOME we Flatpaku](ZROBIONE/0004-prototyp-tacki-i-okna/todo.md) | ✅ zrobione | 2026-09-25 20:39 |
| 0005 | [Plan 1 · Zadanie 1: Szkielet projektu Python i test architektury](ZROBIONE/0005-plan1-szkielet-projektu-python-i-test/todo.md) | ✅ zrobione | 2026-09-25 19:01 |
| 0006 | [Plan 1 · Zadanie 2: Błędy (`errors.py`)](ZROBIONE/0006-plan1-bledy/todo.md) | ✅ zrobione | 2026-09-25 19:01 |
| 0007 | [Plan 1 · Zadanie 3: Modele danych (`models.py`)](ZROBIONE/0007-plan1-modele-danych/todo.md) | ✅ zrobione | 2026-09-25 19:01 |
| 0008 | [Plan 1 · Zadanie 4: Czas i strefy (`timefmt.py`)](ZROBIONE/0008-plan1-czas-i-strefy/todo.md) | ✅ zrobione | 2026-09-25 19:02 |
| 0009 | [Plan 1 · Zadanie 5: Walidacja opisu (`validation.py`, F-11)](ZROBIONE/0009-plan1-walidacja-opisu/todo.md) | ✅ zrobione | 2026-09-25 19:02 |
| 0010 | [Plan 1 · Zadanie 6: Grupowanie list i reguły billable (`grouping.py`, `billable.py`, F-06/F-08/F-09)](ZROBIONE/0010-plan1-grupowanie-list-i-reguly-billable/todo.md) | ✅ zrobione | 2026-09-25 19:02 |
| 0011 | [Plan 1 · Zadanie 7: Klient Kimai API (`kimai_client.py`)](ZROBIONE/0011-plan1-klient-kimai-api/todo.md) | ✅ zrobione | 2026-09-25 19:02 |
| 0012 | [Plan 1 · Zadanie 8: Ustawienia i pamięć aplikacji (`settings.py`)](ZROBIONE/0012-plan1-ustawienia-i-pamiec-aplikacji/todo.md) | ✅ zrobione | 2026-09-25 19:02 |
| 0013 | [Plan 1 · Zadanie 9: Tłumaczenia PL/EN (`i18n.py`, `locales/`, F-13)](ZROBIONE/0013-plan1-tlumaczenia-pl-en/todo.md) | ✅ zrobione | 2026-09-25 19:03 |
| 0014 | [Plan 1 · Zadanie 10: Tracker — stan i odświeżanie (`tracker.py` część 1)](ZROBIONE/0014-plan1-tracker-stan-i-odswiezanie/todo.md) | ✅ zrobione | 2026-09-25 19:03 |
| 0015 | [Plan 1 · Zadanie 11: Tracker — akcje (`tracker.py` część 2, F-04…F-10)](ZROBIONE/0015-plan1-tracker-akcje/todo.md) | ✅ zrobione | 2026-09-25 19:03 |
| 0016 | [Plan 1 · Zadanie 12: Polityka powiadomień (`notification_policy.py`, F-21)](ZROBIONE/0016-plan1-polityka-powiadomien/todo.md) | ✅ zrobione | 2026-09-25 19:03 |
| 0017 | [Plan 1 · Zadanie 13: Testy kontraktowe na Kimai w Dockerze](ZROBIONE/0017-plan1-testy-kontraktowe-na-kimai-w/todo.md) | ✅ zrobione | 2026-09-25 19:04 |
| 0018 | [Plan 1 · Zadanie 14: Komendy, pokrycie i dokumentacja rdzenia](ZROBIONE/0018-plan1-komendy-pokrycie-i-dokumentacja-rdzenia/todo.md) | ✅ zrobione | 2026-09-25 19:05 |
| 0019 | [Drobne uwagi z recenzji Planu 1 (rdzeń)](ZROBIONE/0019-drobne-uwagi-z-recenzji-planu-1/todo.md) | ✅ zrobione | 2026-09-25 19:55 |
| 0021 | [Plan 2 — rozpoznanie API integracji desktopowych](ZROBIONE/0021-plan2-rozpoznanie-api-desktop/todo.md) | ✅ zrobione | 2026-09-25 21:06 |
| 0022 | [Plan 2 · Zadanie 1: Szyna D-Bus (`desktop/bus.py`)](ZROBIONE/0022-plan2-szyna-dbus/todo.md) | ✅ zrobione | 2026-09-25 21:00 |
| 0023 | [Plan 2 · Zadanie 2: Token w magazynie sekretów (`desktop/secrets.py`)](ZROBIONE/0023-plan2-token-w-magazynie-sekretow/todo.md) | ✅ zrobione | 2026-09-25 21:01 |
| 0024 | [Plan 2 · Zadanie 3: Powiadomienia — tekst w rdzeniu, wysyłka przez portal](ZROBIONE/0024-plan2-powiadomienia-przez-portal/todo.md) | ✅ zrobione | 2026-09-25 21:01 |
| 0025 | [Plan 2 · Zadanie 4: Autostart i status w tle (`desktop/autostart.py`)](ZROBIONE/0025-plan2-autostart-i-status-w-tle/todo.md) | ✅ zrobione | 2026-09-25 21:02 |
| 0026 | [Plan 2 · Zadanie 5: Testy na prawdziwej sesji i komendy](ZROBIONE/0026-plan2-testy-na-zywo-i-komendy/todo.md) | ✅ zrobione | 2026-09-25 21:02 |
| 0027 | [Drobne uwagi z recenzji Planu 2 (desktop)](ZROBIONE/0027-drobne-uwagi-z-recenzji-planu-2/todo.md) | ✅ zrobione | 2026-09-25 21:48 |
| 0028 | [Plan 3 — projekt interfejsu (decyzje przed planem)](ZROBIONE/0028-plan3-projekt-ui/todo.md) | ✅ zrobione | 2026-09-25 23:06 |
| 0029 | [Plan 3 · Zadanie 1: Zależności UI, testy Qt i teksty interfejsu](ZROBIONE/0029-plan3-zaleznosci-i-teksty-ui/todo.md) | ✅ zrobione | 2026-09-25 23:08 |
| 0030 | [Plan 3 · Zadanie 2: Teksty tacki i listy w rdzeniu (`core/presentation.py`)](ZROBIONE/0030-plan3-teksty-w-rdzeniu/todo.md) | ✅ zrobione | 2026-09-25 23:08 |
| 0031 | [Plan 3 · Zadanie 3: Motyw i ikony (`ui/theme.py`, `ui/icons.py`)](ZROBIONE/0031-plan3-motyw-i-ikony/todo.md) | ✅ zrobione | 2026-09-25 23:08 |
| 0032 | [Plan 3 · Zadanie 4: Praca w tle (`ui/worker.py`)](ZROBIONE/0032-plan3-praca-w-tle/todo.md) | ✅ zrobione | 2026-09-25 23:09 |
| 0033 | [Plan 3 · Zadanie 5: Stan aplikacji i ikona w tacce (`ui/state.py`, `ui/tray.py`)](ZROBIONE/0033-plan3-stan-i-ikona-w-tacce/todo.md) | ✅ zrobione | 2026-09-25 23:09 |
| 0034 | [Plan 3 · Zadanie 6: Pasek trackera (`ui/form.py`)](ZROBIONE/0034-plan3-pasek-trackera/todo.md) | ✅ zrobione | 2026-09-25 23:09 |
| 0035 | [Plan 3 · Zadanie 7: Ostatnie wpisy (`ui/recent.py`)](ZROBIONE/0035-plan3-ostatnie-wpisy/todo.md) | ✅ zrobione | 2026-09-25 23:09 |
| 0036 | [Plan 3 · Zadanie 8: Okno szybkiej obsługi i jego miejsce (`ui/popup.py`, `ui/placement.py`)](ZROBIONE/0036-plan3-okno-szybkiej-obslugi/todo.md) | ✅ zrobione | 2026-09-25 23:10 |
| 0037 | [Plan 3 · Zadanie 9: Ustawienia (`ui/settings_dialog.py`)](ZROBIONE/0037-plan3-ustawienia/todo.md) | ✅ zrobione | 2026-09-25 23:10 |
| 0038 | [Plan 3 · Zadanie 10: Usługi pulpitu w wątkach UI (`ui/desktop_bridge.py`)](ZROBIONE/0038-plan3-most-do-dbus/todo.md) | ✅ zrobione | 2026-09-25 23:10 |
| 0039 | [Plan 3 · Zadanie 11: Kontroler aplikacji (`ui/app.py`)](ZROBIONE/0039-plan3-kontroler/todo.md) | ✅ zrobione | 2026-09-25 23:10 |
| 0040 | [Plan 3 · Zadanie 12: Start aplikacji (`ui/main.py`, `__main__.py`)](ZROBIONE/0040-plan3-start-aplikacji/todo.md) | ✅ zrobione | 2026-09-25 23:11 |
| 0041 | [Plan 3 · Zadanie 13: Test na żywo na KDE z Kimai w Dockerze](ZROBIONE/0041-plan3-test-na-zywo/todo.md) | ✅ zrobione | 2026-09-26 09:51 |
| 0042 | [Poprawki UI po teście na żywo (Plan 3)](ZROBIONE/0042-poprawki-po-tescie-na-zywo/todo.md) | ✅ zrobione | 2026-09-26 00:47 |
| 0043 | [Dokumenty zgodne z markdownlint](ZROBIONE/0043-markdownlint/todo.md) | ✅ zrobione | 2026-09-25 23:45 |
| 0044 | [Drobne uwagi z recenzji Planu 3 (ui)](ZROBIONE/0044-drobne-uwagi-z-recenzji-planu-3/todo.md) | ✅ zrobione | 2026-09-26 10:14 |
| 0045 | [Plan 4 — projekt paczki Flatpak (decyzje przed planem)](ZROBIONE/0045-plan4-projekt-flatpak/todo.md) | ✅ zrobione | 2026-09-26 13:36 |
| 0046 | [Plan 4 · Zadanie 1: Wersja 0.9.0 i licencja w pakiecie](ZROBIONE/0046-plan4-wersja-licencja/todo.md) | ✅ zrobione | 2026-09-26 11:30 |
| 0047 | [Plan 4 · Zadanie 2: MetaInfo (AppStream) i plik `.desktop`](ZROBIONE/0047-plan4-metainfo/todo.md) | ✅ zrobione | 2026-09-26 11:48 |
| 0048 | [Plan 4 · Zadanie 3: Manifest Flatpaka i zależności Pythona](ZROBIONE/0048-plan4-manifest/todo.md) | ✅ zrobione | 2026-09-26 11:48 |
| 0049 | [Plan 4 · Zadanie 4: Budowa lokalna w kontenerze (`flatpak/buduj.sh`)](ZROBIONE/0049-plan4-budowa-lokalna/todo.md) | ✅ zrobione | 2026-09-26 11:54 |
| 0050 | [Plan 4 · Zadanie 5: Repozytorium Flatpaka dla GitHub Pages](ZROBIONE/0050-plan4-repo-pages/todo.md) | ✅ zrobione | 2026-09-26 11:55 |
| 0051 | [Plan 4 · Zadanie 6: GitHub Actions — testy i wydanie](ZROBIONE/0051-plan4-github-actions/todo.md) | ✅ zrobione | 2026-09-26 11:58 |
| 0052 | [Plan 4 · Zadanie 7: Proces wydania i instrukcja instalacji](ZROBIONE/0052-plan4-proces-wydania/todo.md) | ✅ zrobione | 2026-09-26 11:59 |
| 0053 | [Plan 4 · Zadanie 8: Pierwsze wydanie 0.9.0 (z użytkownikiem)](ZROBIONE/0053-plan4-pierwsze-wydanie/todo.md) | ✅ zrobione | 2026-09-26 13:36 |
| 0054 | [Podobne aplikacje: KimaiTray i KimTrack w dokumentacji](ZROBIONE/0054-podobne-aplikacje/todo.md) | ✅ zrobione | 2026-09-26 11:43 |
| 0055 | [Zmiana nazwy na WS Tracker Tray](ZROBIONE/0055-zmiana-nazwy-ws-tracker-tray/todo.md) | ✅ zrobione | 2026-09-26 11:48 |
| 0056 | [Identyfikator aplikacji i wydawca — firma czy prywatnie](ZROBIONE/0056-identyfikator-i-wydawca/todo.md) | ✅ zrobione | 2026-09-26 14:55 |
| 0057 | [Drobne uwagi z recenzji Planu 4](ZROBIONE/0057-drobne-uwagi-z-recenzji-planu-4/todo.md) | ✅ zrobione | 2026-09-26 12:40 |
| 0058 | [Długie opisy na liście ostatnich wpisów: 2,5 linii i rozwijanie kliknięciem](ZROBIONE/0058-dlugie-opisy-na-liscie/todo.md) | ✅ zrobione | 2026-09-26 13:35 |
| 0059 | [Wyszukiwanie we wszystkich wpisach Kimai (F-33)](ZROBIONE/0059-wyszukiwanie-wpisow/todo.md) | ✅ zrobione | 2026-09-26 13:35 |
| 0060 | [Zmiana projektu i rodzaju pracy trwającego wpisu (F-34)](ZROBIONE/0060-zmiana-projektu-trwajacego-wpisu/todo.md) | ✅ zrobione | 2026-09-26 13:35 |
| 0061 | [Domyślny projekt i rodzaj pracy z ostatniego wpisu w Kimai](ZROBIONE/0061-domyslnie-ostatni-wpis/todo.md) | ✅ zrobione | 2026-09-26 13:35 |
| 0063 | [Własna ikona i nazwa „WS Tracker” w 0.9.1](ZROBIONE/0063-ikona-ws-tracker/todo.md) | ✅ zrobione | 2026-09-26 13:59 |
| 0064 | [Licencja GPL-3.0-or-later zamiast AGPL](ZROBIONE/0064-licencja-gpl/todo.md) | ✅ zrobione | 2026-09-26 14:14 |
| 0065 | [Poprawki po 0.9.1: zmiana rozmiaru okna, mała ikona, zrzut w Discover](ZROBIONE/0065-poprawki-po-0-9-1/todo.md) | ✅ zrobione | 2026-09-26 14:51 |
| 0066 | [Zmiana rozmiaru okna przy tacce bez skoków: przezroczyste płótno i panel](ZROBIONE/0066-plotno-okna-przy-tacce/todo.md) | ✅ zrobione | 2026-09-26 14:51 |
| 0067 | [Na GitHubie tylko najnowsze wydanie; starsze jako tagi](ZROBIONE/0067-tylko-najnowsze-wydanie/todo.md) | ✅ zrobione | 2026-09-26 15:45 |
| 0068 | [Pole opisu w okienku rośnie z kolejnymi liniami](ZROBIONE/0068-pole-opisu-rosnie/todo.md) | ✅ zrobione | 2026-09-26 17:15 |
| 0069 | [Plan 5: okno główne 0.10.0 — wykonanie](ZROBIONE/0069-plan5-okno-glowne/todo.md) | ✅ zrobione | 2026-09-26 19:32 |
| 0070 | [Plan 6: podsumowania 0.10.3 — wykonanie](ZROBIONE/0070-plan6-podsumowania/todo.md) | ✅ zrobione | 2026-09-27 12:58 |
| 0071 | [Strona projektu na GitHub Pages — nowy wygląd i workflow „Strona”](ZROBIONE/0071-strona-github-pages/todo.md) | ✅ zrobione | 2026-09-27 12:36 |
| 0072 | [O programie i wersja w ustawieniach (0.10.4)](ZROBIONE/0072-o-programie/todo.md) | ✅ zrobione | 2026-09-27 13:07 |
| 0073 | [Plan 7: kalendarz 0.10.5 — wykonanie](ZROBIONE/0073-plan7-kalendarz/todo.md) | ✅ zrobione | 2026-09-27 13:44 |
| 0074 | [Opis DK Tracker jako pełnego klienta Kimai: README, dokumentacja, strona, zrzuty](ZROBIONE/0074-opis-pelnej-aplikacji/todo.md) | ✅ zrobione | 2026-09-27 14:12 |
| 0075 | [Okno przy tacce na ekranie klikniętej ikony](ZROBIONE/0075-okno-na-ekranie-kliknietej-tacki/todo.md) | ✅ zrobione | 2026-09-28 07:40 |

<!-- tablica:end -->

## Widok dynamiczny (Obsidian + Dataview)

Jeśli masz wtyczkę [Dataview](https://blacksmithgu.github.io/obsidian-dataview/), te
bloki pokażą tabele na żywo z frontmatterów zadań:

```dataview
TABLE status, priorytet, zalezy_od AS "zależy od", zaktualizowano
FROM "TODO/W-TRAKCIE" OR "TODO/DO-ZROBIENIA"
WHERE file.name = "todo"
SORT numer ASC
```

```dataview
TABLE status, zamknieto
FROM "TODO/ZROBIONE"
WHERE file.name = "todo"
SORT numer ASC
```
