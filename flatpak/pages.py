"""Files that turn an OSTree repository on GitHub Pages into a Flatpak remote people can install from.

    python3 flatpak/pages.py <site-dir> <base-url> <public-key.gpg>

writes <site-dir>/ws-tracker-tray.flatpakrepo (adds the remote, updates come through Discover or GNOME
Software), <site-dir>/pl.websystems.WsTrackerTray.flatpakref (installs the app in one command) and a
small index.html. The repository itself goes to <site-dir>/repo (flatpak/publikuj.sh copies it).
Format: https://docs.flatpak.org/en/latest/flatpak-command-reference.html (.flatpakrepo, .flatpakref).
"""

from __future__ import annotations

import base64
import html
import sys
from pathlib import Path

APP_ID = "pl.websystems.WsTrackerTray"
TITLE = "WS Tracker Tray"
REMOTE = "ws-tracker-tray"
BRANCH = "master"  # flatpak-builder's default branch; the GitHub action builds it too
FLATHUB = "https://dl.flathub.org/repo/flathub.flatpakrepo"  # where the KDE runtime and PySide base come from


def _key(public_key: bytes) -> str:
    return base64.b64encode(public_key).decode("ascii")


def flatpakrepo(base_url: str, public_key: bytes) -> str:
    return (
        "[Flatpak Repo]\n"
        f"Title={TITLE}\n"
        f"Url={base_url.rstrip('/')}/repo/\n"
        f"Homepage={base_url.rstrip('/')}/\n"
        f"Comment=Kimai time tracking in the system tray\n"
        f"GPGKey={_key(public_key)}\n"
    )


def flatpakref(base_url: str, public_key: bytes) -> str:
    return (
        "[Flatpak Ref]\n"
        f"Title={TITLE}\n"
        f"Name={APP_ID}\n"
        f"Branch={BRANCH}\n"
        f"Url={base_url.rstrip('/')}/repo/\n"
        f"SuggestRemoteName={REMOTE}\n"
        "IsRuntime=false\n"
        f"RuntimeRepo={FLATHUB}\n"
        f"GPGKey={_key(public_key)}\n"
    )


def index_html(base_url: str) -> str:
    url = html.escape(base_url.rstrip("/"))
    return f"""<!doctype html>
<html lang="pl">
<head><meta charset="utf-8"><title>{TITLE} — repozytorium Flatpak</title></head>
<body>
<h1>{TITLE}</h1>
<p>Instalacja — aktualizacje przyjdą same (Discover, GNOME Software, <code>flatpak update</code>):</p>
<pre>flatpak install --user {url}/{APP_ID}.flatpakref</pre>
<p>Samo źródło aktualizacji: <a href="{REMOTE}.flatpakrepo">{REMOTE}.flatpakrepo</a> ·
<a href="https://github.com/DragonKing026/Kimai-App--Linux-">kod źródłowy</a></p>
</body>
</html>
"""


def write_site(site: Path, base_url: str, public_key_file: Path) -> None:
    key = public_key_file.read_bytes()
    site.mkdir(parents=True, exist_ok=True)
    (site / f"{REMOTE}.flatpakrepo").write_text(flatpakrepo(base_url, key), encoding="utf-8")
    (site / f"{APP_ID}.flatpakref").write_text(flatpakref(base_url, key), encoding="utf-8")
    (site / "index.html").write_text(index_html(base_url), encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    write_site(Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]))
