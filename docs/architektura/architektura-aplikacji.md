---
tytul: Architektura aplikacji
tagi: [architektura, komponenty, przeplywy]
status_dokumentu: szkic
utworzono: 2026-09-25
zaktualizowano: 2026-09-25
---

# Architektura aplikacji

> [!warning] Szkic logiczny
> Ten dokument opisuje podział na komponenty **niezależnie od języka i biblioteki UI**.
> Zostanie doprecyzowany (nazwy modułów, ścieżki plików) po zatwierdzeniu stosu
> w ADR i specyfikacji projektu — patrz [[TODO/README|zadania fazy 1]].

## Warstwy

```mermaid
flowchart TB
    subgraph UI["Warstwa prezentacji"]
        TRAY[Tray<br/>ikona + menu + tooltip]
        WIN[Okno szybkiej obsługi<br/>tracker + lista ostatnich]
        SET[Okno ustawień]
    end
    subgraph APP["Warstwa aplikacji"]
        STORE[Stan aplikacji<br/>running, projekty, wpisy, sumy]
        POLL[Harmonogram odświeżania<br/>co 60 s + na żądanie]
        ACT[Akcje<br/>start, stop, wznów, edytuj, billable]
    end
    subgraph DOM["Domena (czysta logika, bez I/O)"]
        VAL[Walidacja opisu F-11]
        BILL[Reguły billable F-09]
        FMT[Formatowanie czasu i dni]
        GRP[Grupowanie wpisów po dniach, projektów po klientach]
    end
    subgraph INFRA["Infrastruktura"]
        API[Klient Kimai API]
        CFG[Ustawienia<br/>plik konfiguracyjny]
        SEC[Sekrety<br/>Secret Service]
        NOT[Powiadomienia / autostart<br/>portale XDG]
    end
    TRAY --> ACT
    WIN --> ACT
    SET --> CFG
    SET --> SEC
    ACT --> API
    ACT --> STORE
    POLL --> API
    POLL --> STORE
    STORE --> TRAY
    STORE --> WIN
    ACT --> VAL
    ACT --> BILL
    WIN --> FMT
    WIN --> GRP
    API --> SEC
```

## Komponenty

| Komponent | Odpowiedzialność | Zależy od | Funkcje |
|---|---|---|---|
| **Klient Kimai API** | HTTP + Bearer, mapowanie błędów (`ApiError`, `isBillableRejected`, zbieranie błędów formularza), format dat lokalnych, stronicowanie | sekrety, ustawienia | F-01, F-04…F-12, F-14 |
| **Domena** | walidacja opisu, domyślne billable, formatowanie `h:mm`/`47m`, nazwy dni, grupowanie | nic | F-02, F-08, F-09, F-11, F-12 |
| **Stan aplikacji** | jedno źródło prawdy o trwającym wpisie, listach i sumach; powiadamia UI o zmianach | API, domena | wszystkie |
| **Harmonogram** | odświeżanie co 60 s (jak `chrome.alarms` we wtyczce), natychmiast po akcjach, tyk zegara co 1 s gdy okno otwarte | stan | F-02, F-12 |
| **Tray** | ikona zależna od stanu, tooltip z czasem, menu kontekstowe, otwieranie okna | stan, akcje | F-02, F-20 |
| **Okno szybkiej obsługi** | odpowiednik popupu wtyczki | stan, akcje, domena | F-03…F-10, F-12 |
| **Okno ustawień** | URL, token, język, min. długość opisu, test połączenia | ustawienia, sekrety, API | F-01, F-13 |
| **Ustawienia** | trwały zapis nie-sekretnych ustawień i „ostatni wybór” | system plików (XDG config) | F-01, F-06 |
| **Sekrety** | zapis/odczyt tokenu w magazynie systemu | Secret Service / portal | F-01 |

**Zasada**: domena nie wie nic o UI ani HTTP — dzięki temu testujemy ją jednostkowo
i przenosimy 1:1 z testowalnej logiki wtyczki (`validate.js`, formatowanie).

## Przepływ: start timera

```mermaid
sequenceDiagram
    actor U as Użytkownik
    participant W as Okno
    participant A as Akcje
    participant D as Domena
    participant K as Klient API
    participant S as Stan
    participant T as Tray
    U->>W: opis + projekt + czynność, Enter
    W->>A: start(projekt, czynność, opis, billable?)
    A->>D: validateDescription(opis, min)
    D-->>A: ok / short / generic
    alt opis niepoprawny
        A-->>W: błąd walidacji
    else ok
        A->>K: POST /api/timesheets (billable tylko gdy ruszony)
        alt 400 "extra fields" i billable wysłany
            K-->>A: ApiError 400
            A->>S: zablokuj billable
            A->>K: POST /api/timesheets (bez billable)
        end
        K-->>A: wpis
        A->>S: running = wpis, zapamiętaj ostatni wybór
        S-->>T: stan = trwa
        S-->>W: odśwież widok
    end
```

## Przepływ: cykl odświeżania

```mermaid
sequenceDiagram
    participant H as Harmonogram
    participant K as Klient API
    participant S as Stan
    participant T as Tray
    loop co 60 s
        H->>K: GET /api/timesheets/active
        alt sukces
            K-->>H: [] albo [wpis]
            H->>S: aktualizuj running
            S-->>T: ikona + tooltip (np. „1:22 — Projekt X”)
        else błąd
            H->>S: stan = błąd
            S-->>T: ikona błędu
        end
    end
```

## Otwarte kwestie architektoniczne

- [ ] Stos technologiczny (język, UI toolkit, tray) — ADR
- [ ] Forma „popupu” na Waylandzie (okno, okno bez ramki, panel, samo menu) — ADR
- [ ] Runtime Flatpaka (KDE vs GNOME vs Freedesktop) — wynika ze stosu
- [ ] Sposób przechowywania tokenu (Secret Service bezpośrednio vs portal Secret)

## Powiązane

- [[docs/architektura/funkcje|Katalog funkcji]]
- [[docs/integracje/README|Integracje]]
- [[docs/decyzje/README|Decyzje]]
