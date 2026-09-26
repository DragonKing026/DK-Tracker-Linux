"""The package and its metadata agree with each other (Plan 4): version, licence, ids, commands.

A Flatpak mistake here shows up only after a release — a wrong Exec or version in the store —
so the files are checked together on every test run.
"""

import tomllib
import xml.etree.ElementTree as ET
from pathlib import Path

import kimai_tray

ROOT = Path(__file__).resolve().parents[1]
APP_ID = "pl.websystems.KimaiTray"
PYPROJECT = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
LANG = "{http://www.w3.org/XML/1998/namespace}lang"


def metainfo() -> ET.Element:
    return ET.parse(ROOT / "data" / f"{APP_ID}.metainfo.xml").getroot()


def desktop_entry() -> dict[str, str]:
    lines = (ROOT / "data" / f"{APP_ID}.desktop").read_text(encoding="utf-8").splitlines()
    return dict(line.split("=", 1) for line in lines if "=" in line)


def test_version_is_the_same_everywhere():
    assert PYPROJECT["version"] == kimai_tray.__version__ == "0.9.0"


def test_licence_is_agpl():
    assert PYPROJECT["license"] == "AGPL-3.0-or-later"
    licence = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert licence.lstrip().startswith("GNU AFFERO GENERAL PUBLIC LICENSE")
