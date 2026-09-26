"""Settings as a page of the main window (F-01, F-13, F-21, F-22), not a window of their own.

The controller talks to it as it talked to the settings dialog: `load`, `show_status`,
`set_busy`, `set_secrets_problem`, `retranslate`, and `saveRequested` / `testRequested`.
The token field starts empty: a token already in the wallet stays there unless a new one is
typed, so the token is never read back into the page (spec 1.0, section 8).
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from typing import Any

from PySide6.QtCore import Property, QObject, Signal, Slot

from dk_tracker.core.settings import Settings

LANGUAGES = (("auto", "optLangAuto"), ("pl", "optLangPl"), ("en", "optLangEn"))
THEMES = (("auto", "optThemeAuto"), ("light", "optThemeLight"), ("dark", "optThemeDark"))


class SettingsForm(QObject):
    saveRequested = Signal(object, object)  # Settings, new token or None to keep the stored one
    testRequested = Signal(str, str)  # address, token as typed ("" = the stored one)
    formChanged = Signal()
    loaded = Signal()  # the fields take the values again (typing does not come back through `form`)

    def __init__(self, t: Callable[..., str], parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._t = t
        self._loaded = Settings()
        self._has_token = False
        self._secrets_problem: str | None = None
        self._url = ""
        self._form: dict[str, Any] = {}
        self._status, self._status_ok, self._busy = "", True, False
        self.load(Settings(), has_token=False)

    def _get_form(self) -> dict[str, Any]:
        return self._form

    form = Property("QVariantMap", _get_form, notify=formChanged)

    # -- from the controller ---------------------------------------------------------

    def load(self, settings: Settings, *, has_token: bool) -> None:
        self._loaded, self._has_token, self._url = settings, has_token, settings.url
        self._status = ""
        self._refresh()
        self.loaded.emit()

    def set_secrets_problem(self, key: str | None) -> None:
        self._secrets_problem = key
        self._refresh()

    def show_status(self, text: str, *, ok: bool) -> None:
        self._status, self._status_ok = text, ok
        self._refresh()

    def set_busy(self, busy: bool) -> None:
        self._busy = busy
        self._refresh()

    def set_autostart(self, enabled: bool) -> None:
        """The portal refused autostart: the switch goes back."""
        self._loaded = replace(self._loaded, autostart=enabled)
        self._refresh()
        self.loaded.emit()

    def retranslate(self, t: Callable[..., str]) -> None:
        self._t = t
        self._refresh()

    # -- from QML --------------------------------------------------------------------

    @Slot(str)
    def urlEdited(self, url: str) -> None:  # noqa: N802
        self._url = url
        self._refresh()

    @Slot("QVariantMap", str)
    def save(self, values: dict[str, Any], token: str) -> None:
        settings = replace(
            self._loaded,
            url=str(values.get("url", "")),
            language=str(values.get("language", "auto")),
            min_description=int(values.get("minDescription", 0)),
            long_timer_hours=float(values.get("longTimer", 0.0)),
            notify_connection=bool(values.get("notifyConnection", True)),
            notify_menu_actions=bool(values.get("notifyMenu", True)),
            autostart=bool(values.get("autostart", False)),
            show_tray=bool(values.get("showTray", True)),
            theme=str(values.get("theme", "auto")),
        ).normalized()
        token = token.strip()
        if not settings.url:
            self.show_status(self._t("optUrlRequired"), ok=False)
            return
        if not token and not self._has_token:
            self.show_status(self._t("optTokenRequired"), ok=False)
            return
        self.saveRequested.emit(settings, token or None)

    @Slot(str, str)
    def test(self, url: str, token: str) -> None:
        self.show_status(self._t("optTesting"), ok=True)
        self.testRequested.emit(url.strip().rstrip("/"), token.strip())

    # -- internals -------------------------------------------------------------------

    def _refresh(self) -> None:
        s, t = self._loaded, self._t
        notes = [t(key) for key in replace(s, url=self._url).warnings()]
        if self._secrets_problem:
            notes.append(t(self._secrets_problem))
        self._form = {
            "url": s.url,
            "language": s.language,
            "languages": [{"code": code, "label": t(key)} for code, key in LANGUAGES],
            "minDescription": s.min_description,
            "longTimer": s.long_timer_hours,
            "notifyConnection": s.notify_connection,
            "notifyMenu": s.notify_menu_actions,
            "autostart": s.autostart,
            "showTray": s.show_tray,
            "theme": s.theme,
            "themes": [{"code": code, "label": t(key)} for code, key in THEMES],
            "tokenPlaceholder": t("optTokenKeep") if self._has_token else "",
            "warning": "\n\n".join(notes),
            "status": self._status,
            "okStatus": self._status_ok,
            "busy": self._busy,
        }
        self.formChanged.emit()
