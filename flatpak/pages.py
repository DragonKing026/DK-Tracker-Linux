"""Files that turn an OSTree repository on GitHub Pages into a Flatpak remote people can install from.

    python3 flatpak/pages.py <site-dir> <base-url> <public-key.gpg>

writes <site-dir>/dk-tracker.flatpakrepo (adds the remote, updates come through Discover or GNOME
Software), <site-dir>/io.github.dragonking026.DK-Tracker-Linux.flatpakref (installs the app in one
command) and the project page: flatpak/strona/ (index.html filled with the address and the newest
release from the MetaInfo file, strona.css, strona.js), the app icon and the screenshots.
The repository itself goes to <site-dir>/repo (flatpak/publikuj.sh copies it).
Format: https://docs.flatpak.org/en/latest/flatpak-command-reference.html (.flatpakrepo, .flatpakref).
"""

from __future__ import annotations

import base64
import html
import shutil
import sys
from pathlib import Path
from xml.etree import ElementTree

APP_ID = "io.github.dragonking026.DK-Tracker-Linux"
TITLE = "DK Tracker"
REMOTE = "dk-tracker"
BRANCH = "master"  # flatpak-builder's default branch; the GitHub action builds it too
ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "flatpak" / "strona"
METAINFO = ROOT / "data" / f"{APP_ID}.metainfo.xml"
ASSETS = (
    ROOT / "data" / "icons" / "dk-tracker.svg",
    ROOT / "docs" / "assets" / "zrzuty" / "okno-ciemny-motyw.png",
    ROOT / "docs" / "assets" / "zrzuty" / "okno-glowne-wpisy.png",
    ROOT / "docs" / "assets" / "zrzuty" / "okno-glowne-edycja.png",
    ROOT / "docs" / "assets" / "zrzuty" / "okno-glowne-podsumowania.png",
    ROOT / "docs" / "assets" / "zrzuty" / "okno-glowne-kalendarz.png",
)
FLATHUB = "https://dl.flathub.org/repo/flathub.flatpakrepo"  # where the KDE runtime and PySide base come from


def _key(public_key: bytes) -> str:
    return base64.b64encode(public_key).decode("ascii")


def flatpakrepo(base_url: str, public_key: bytes) -> str:
    return (
        "[Flatpak Repo]\n"
        f"Title={TITLE}\n"
        f"Url={base_url.rstrip('/')}/repo/\n"
        f"Homepage={base_url.rstrip('/')}/\n"
        f"Comment=Kimai client for the Linux desktop\n"
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


def latest_release(metainfo: Path = METAINFO) -> tuple[str, str]:
    """Version and date of the newest release in the AppStream file (the first <release>)."""
    release = ElementTree.parse(metainfo).getroot().find("releases/release")
    if release is None:
        raise ValueError(f"{metainfo} has no <release>")
    return release.get("version", ""), release.get("date", "")


def index_html(base_url: str, version: str, date: str) -> str:
    page = (PAGE / "index.html").read_text(encoding="utf-8")
    for name, value in {"url": base_url.rstrip("/"), "version": version, "date": date}.items():
        page = page.replace("{{" + name + "}}", html.escape(value))
    if "{{" in page:
        raise ValueError("flatpak/strona/index.html has a placeholder pages.py does not fill")
    return page


def write_site(site: Path, base_url: str, public_key_file: Path) -> None:
    key = public_key_file.read_bytes()
    site.mkdir(parents=True, exist_ok=True)
    (site / f"{REMOTE}.flatpakrepo").write_text(flatpakrepo(base_url, key), encoding="utf-8")
    (site / f"{APP_ID}.flatpakref").write_text(flatpakref(base_url, key), encoding="utf-8")
    (site / "index.html").write_text(index_html(base_url, *latest_release()), encoding="utf-8")
    for name in ("strona.css", "strona.js"):
        shutil.copyfile(PAGE / name, site / name)
    for source in ASSETS:
        shutil.copyfile(source, site / source.name)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    write_site(Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]))
