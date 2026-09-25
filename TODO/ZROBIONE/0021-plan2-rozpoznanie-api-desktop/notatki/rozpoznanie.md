---
noteId: "f21bd94aebb64ed2b84759e91d771dce"
tytul: "Rozpoznanie API integracji desktopowych (Plan 2)"
tags: [plan-2, dbus, sekrety, portale, notatki]
utworzono: 2026-09-25 20:46
zaktualizowano: 2026-09-25 20:46
---

# Rozpoznanie API integracji desktopowych

Sprawdzone 2026-09-25 20:46 na Fedorze 44, KDE Plasma 6.7.5 (Wayland), jeepney, **na hoście i z wnętrza
Flatpaka** (`pl.websystems.KimaiTray.Prototyp`, jeepney podany przez `PYTHONPATH`).
Skrypty: [probe_secret.py](../prototyp/probe_secret.py), [probe_notify.py](../prototyp/probe_notify.py),
[probe_background.py](../prototyp/probe_background.py).

## Secret Service (`org.freedesktop.secrets`, ksecretd/KWallet)

| Krok | Wynik |
| --- | --- |
| `OpenSession("plain")` | sesja `/org/freedesktop/secrets/session/N` |
| `ReadAlias("default")` | `/org/freedesktop/secrets/collection/kdewallet` |
| `Collection.CreateItem(props, (session, b"", secret, "text/plain"), replace=True)` — sygnatura `a{sv}(oayays)b` | ścieżka elementu, prompt `/` (brak promptu — portfel otwarty) |
| `Service.SearchItems(attrs)` | `(unlocked, locked)` |
| `Service.GetSecrets(items, session)` — `aoo` | `{item: (session, params, value, content_type)}` |
| `Item.Delete()` | prompt `/`; po usunięciu `SearchItems` puste |
| Właściwość `Collection.Locked` | `False` |
| **Flatpak bez** `--talk-name=org.freedesktop.secrets` | odpowiedź **błędu D-Bus** — kod musi sprawdzać typ odpowiedzi |
| **Flatpak z** `--talk-name=org.freedesktop.secrets` | pełny cykl działa |

Właściwości elementu: `org.freedesktop.Secret.Item.Label` (`s`) i
`org.freedesktop.Secret.Item.Attributes` (`a{ss}`).

## Portal Notification (`org.freedesktop.portal.Notification`)

| Krok | Wynik |
| --- | --- |
| wersja interfejsu | **1** (backend `plasmanotify`) |
| `AddNotification(id, {title, body, priority, buttons: aa{sv}[{label, action, target}]})` | przyjęte (host i Flatpak) |
| Klik przycisku | sygnał `ActionInvoked(id, action, parameter)` — np. `("long-timer-123", "keep", [{"activation-token": "kwin-295"}])` |
| Parametr przycisku | zawiera **dane platformy** (`activation-token`) — numer wpisu bierzemy z **identyfikatora powiadomienia**, nie z `target` |
| Host (poza Flatpakiem) i Flatpak | kliknięcie dociera w obu przypadkach |
| `RemoveNotification(id)` | usuwa powiadomienie także z historii |

## Portal Background (`org.freedesktop.portal.Background`)

| Krok | Wynik |
| --- | --- |
| wersja interfejsu | **2** |
| `RequestBackground("", {handle_token, reason, autostart: false})` | obiekt Request; sygnał `Request.Response` → `(0, {background: True, autostart: False})`; na ścieżkę `/org/freedesktop/portal/desktop/request/<sender>/<token>` trzeba zapisać się **przed** wywołaniem |
| `SetStatus({message})` na hoście | **błąd**: „Only sandboxed applications can set background status” — pomijamy bez błędu |
| `SetStatus` z Flatpaka | działa |
| Autostart | niesprawdzany (`autostart=false`, żeby nie zmieniać systemu); `~/.config/autostart` bez zmian |

## Wnioski do Planu 2

- Jeden mały moduł D-Bus: wywołanie metody z rozpoznaniem odpowiedzi-błędu i wzorzec Request/Response portali.
- Sekrety: sesja `plain`, kolekcja `default`, atrybuty `application` + `url`; brak usługi / odmowa → „brak magazynu
  sekretów”.
- Powiadomienia: identyfikator `long-timer-<id>` niesie numer wpisu; akcje `stop`/`keep`/`settings`.
- Autostart: `RequestBackground(autostart, commandline)`; `SetStatus` tylko we Flatpaku (błąd na hoście ignorowany).
