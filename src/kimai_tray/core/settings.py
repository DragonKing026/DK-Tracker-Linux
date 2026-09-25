"""Settings and remembered state, stored as JSON in XDG directories.

The API token is never stored here — it lives in the system secret store (plan 2).
Inside Flatpak, XDG_CONFIG_HOME / XDG_STATE_HOME already point into ~/.var/app/<id>/.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, fields, replace
from pathlib import Path

APP_DIR = "kimai-tray"


@dataclass(frozen=True)
class Settings:
    url: str = ""
    language: str = "auto"  # auto | pl | en
    min_description: int = 15  # 0 turns the check off
    long_timer_hours: float = 8.0  # 0 turns N-01 off
    notify_connection: bool = True
    notify_menu_actions: bool = True
    autostart: bool = False

    def normalized(self) -> Settings:
        return replace(
            self,
            url=self.url.strip().rstrip("/"),
            min_description=max(0, int(self.min_description)),
            long_timer_hours=max(0.0, float(self.long_timer_hours)),
        )

    def warnings(self) -> list[str]:
        return ["warnHttp"] if self.url.strip().lower().startswith("http://") else []


@dataclass(frozen=True)
class Memory:
    last_project: int | None = None
    last_activity: int | None = None
    billable_allowed: bool = True  # cleared by saving the settings
    kimai_locale: str = "en"  # Kimai has no locale-free /timesheet/ route


def _base(variable: str, fallback: Path) -> Path:
    value = os.environ.get(variable)
    return Path(value) if value else fallback


def config_path() -> Path:
    return _base("XDG_CONFIG_HOME", Path.home() / ".config") / APP_DIR / "settings.json"


def state_path() -> Path:
    return _base("XDG_STATE_HOME", Path.home() / ".local" / "state") / APP_DIR / "state.json"


def load_json[T](cls: type[T], path: Path) -> T:
    """Defaults for a missing or broken file; keys from other versions are ignored."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return cls()
    if not isinstance(data, dict):
        return cls()
    defaults = cls()
    accepted = {
        field.name: data[field.name]
        for field in fields(cls)  # type: ignore[arg-type]
        if field.name in data and _fits(getattr(defaults, field.name), data[field.name])
    }
    return cls(**accepted)


def _fits(default: object, value: object) -> bool:
    """A hand-edited field of the wrong type falls back to its default, not the whole file."""
    if isinstance(default, bool) or isinstance(value, bool):
        return isinstance(default, bool) and isinstance(value, bool)
    if default is None:  # optional ids
        return value is None or isinstance(value, int)
    if isinstance(default, float):
        return isinstance(value, int | float)
    return isinstance(value, type(default))


def save_json(value: object, path: Path) -> None:
    """Written to a temporary file first, so a crash never leaves half a file behind."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(asdict(value), indent=2, ensure_ascii=False), encoding="utf-8")  # type: ignore[call-overload]
    temporary.replace(path)
