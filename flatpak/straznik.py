"""Qt guard (0086, ADR-0008): keeps the Qt inside the Flatpak on the newest PySide6 patch release.

    python3 flatpak/straznik.py sprawdz     → bundled and newest version; exit 10 when a newer one exists
    python3 flatpak/straznik.py aktualizuj  → the manifest moves to the newest version (wheels, Qt headers)

Only versions inside the `ui` range of pyproject.toml, and only releases at least COOLDOWN_DAYS old (the same
cooldown as Dependabot). The manifest pins two PyPI wheels (shiboken6, pyside6-essentials) and the official Qt
binaries of the same version (headers for layer-shell-qt); all of them move together. Standard library only:
it runs in GitHub Actions before anything is installed.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import sys
import tomllib
import urllib.request
from collections.abc import Callable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "flatpak" / "io.github.dragonking026.DK-Tracker-Linux.yml"
PYPI = "https://pypi.org/pypi/{name}/json"
QT_REPO = (
    "https://download.qt.io/online/qtsdkrepository/linux_x64/desktop/qt6_{v}/qt6_{v}/qt.qt6.{v}.linux_gcc_64/"
)
QT_PARTS = ("qtbase", "qtdeclarative", "qtwayland")
WHEELS = ("shiboken6", "pyside6-essentials")
WHEEL_RE = re.compile(r"-cp\d+-abi3-manylinux_(\d+)_(\d+)_x86_64\.whl$")
COOLDOWN_DAYS = 7
EXIT_NEWER = 10

Fetch = Callable[[str], bytes]


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "dk-tracker-qt-guard"})
    with urllib.request.urlopen(request, timeout=300) as response:  # noqa: S310 — fixed https hosts
        return response.read()


def bundled_version(text: str) -> str:
    found = set(re.findall(r"/pyside6_essentials-([0-9.]+)-cp", text))
    if len(found) != 1:
        raise SystemExit(f"manifest: expected one pyside6_essentials wheel, found {sorted(found)}")
    return found.pop()


def _version_key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def ui_range(pyproject: Path = ROOT / "pyproject.toml") -> tuple[str, str]:
    """`PySide6>=6.11,<6.12` → ("6.11", "6.12")."""
    (spec,) = tomllib.loads(pyproject.read_text(encoding="utf-8"))["project"]["optional-dependencies"]["ui"]
    low, high = re.fullmatch(r"PySide6>=([0-9.]+),<([0-9.]+)", spec.replace(" ", "")).groups()
    return low, high


def newest_version(get: Fetch, low: str, high: str, today: dt.date) -> str:
    releases = json.loads(get(PYPI.format(name="pyside6-essentials")))["releases"]
    candidates = []
    for version, files in releases.items():
        if not re.fullmatch(r"\d+\.\d+\.\d+", version) or not files or any(f.get("yanked") for f in files):
            continue
        if not _version_key(low) <= _version_key(version) < _version_key(high):
            continue
        uploaded = min(dt.date.fromisoformat(f["upload_time"][:10]) for f in files)
        if (today - uploaded).days >= COOLDOWN_DAYS:
            candidates.append(version)
    if not candidates:
        raise SystemExit(f"PyPI: no pyside6-essentials release in [{low}, {high})")
    return max(candidates, key=_version_key)


def wheel(get: Fetch, name: str, version: str) -> tuple[str, str]:
    """URL and sha256 of the Linux x86-64 abi3 wheel with the lowest glibc it needs."""
    files = json.loads(get(PYPI.format(name=name).replace("/json", f"/{version}/json")))["urls"]
    linux = [(tuple(map(int, m.groups())), f) for f in files if (m := WHEEL_RE.search(f["filename"]))]
    if not linux:
        raise SystemExit(f"PyPI: {name} {version} has no manylinux x86_64 abi3 wheel")
    best = min(linux, key=lambda item: item[0])[1]
    return best["url"], best["digests"]["sha256"]


def qt_archives(get: Fetch, version: str) -> list[tuple[str, str]]:
    """URL and sha256 of the official Qt binaries (checked against the repository's sha1)."""
    base = QT_REPO.format(v=version.replace(".", ""))
    listing = get(base).decode()
    result = []
    for part in QT_PARTS:
        archive = rf'href="({re.escape(version)}-0-\d+{part}-Linux-[^"]+-X86_64\.7z)"'
        names = sorted(set(re.findall(archive, listing)))
        if len(names) != 1:
            raise SystemExit(f"Qt repository: expected one {part} archive for {version}, found {names}")
        url = base + names[0]
        data = get(url)
        expected_sha1 = get(url + ".sha1").decode().split()[0]
        if hashlib.sha1(data).hexdigest() != expected_sha1:  # noqa: S324 — the repository publishes sha1
            raise SystemExit(f"Qt repository: sha1 mismatch for {names[0]}")
        result.append((url, hashlib.sha256(data).hexdigest()))
    return result


def _replace_source(text: str, url_pattern: str, url: str, sha256: str) -> str:
    pattern = re.compile(rf"(url: )\S*{url_pattern}\S*(\n\s+sha256: )[0-9a-f]{{64}}")
    text, count = pattern.subn(lambda m: f"{m.group(1)}{url}{m.group(2)}{sha256}", text)
    if count != 1:
        raise SystemExit(f"manifest: expected one source matching {url_pattern}, found {count}")
    return text


def update(text: str, get: Fetch, version: str) -> str:
    for name in WHEELS:
        url, sha256 = wheel(get, name, version)
        text = _replace_source(text, rf"/{name.replace('-', '_')}-[0-9.]+-cp", url, sha256)
    for part, (url, sha256) in zip(QT_PARTS, qt_archives(get, version), strict=True):
        text = _replace_source(text, rf"-0-\d+{part}-Linux-", url, sha256)
    return text


def main(argv: list[str], get: Fetch = fetch, today: dt.date | None = None) -> int:
    if argv not in (["sprawdz"], ["aktualizuj"]):
        print(__doc__, file=sys.stderr)
        return 2
    text = MANIFEST.read_text(encoding="utf-8")
    current = bundled_version(text)
    newest = newest_version(get, *ui_range(), today or dt.date.today())
    print(f"PySide6/Qt w paczce: {current}, najnowsze: {newest}")
    if _version_key(newest) <= _version_key(current):
        return 0
    if argv == ["aktualizuj"]:
        MANIFEST.write_text(update(text, get, newest), encoding="utf-8")
        print(f"Manifest przestawiony na {newest}.")
    return EXIT_NEWER


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
