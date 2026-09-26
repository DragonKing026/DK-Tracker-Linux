"""The package and its metadata agree with each other (Plan 4): version, licence, ids, commands.

A Flatpak mistake here shows up only after a release — a wrong Exec or version in the store —
so the files are checked together on every test run.
"""

import tomllib
import xml.etree.ElementTree as ET
from pathlib import Path

import ws_tracker_tray

ROOT = Path(__file__).resolve().parents[1]
APP_ID = "pl.websystems.WsTrackerTray"
PYPROJECT = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
LANG = "{http://www.w3.org/XML/1998/namespace}lang"


def metainfo() -> ET.Element:
    return ET.parse(ROOT / "data" / f"{APP_ID}.metainfo.xml").getroot()


def desktop_entry() -> dict[str, str]:
    lines = (ROOT / "data" / f"{APP_ID}.desktop").read_text(encoding="utf-8").splitlines()
    return dict(line.split("=", 1) for line in lines if "=" in line)


def test_version_is_the_same_everywhere():
    assert PYPROJECT["version"] == ws_tracker_tray.__version__ == "0.9.0"


def test_licence_is_agpl():
    assert PYPROJECT["license"] == "AGPL-3.0-or-later"
    licence = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert licence.lstrip().startswith("GNU AFFERO GENERAL PUBLIC LICENSE")


# -- Task 2: MetaInfo and the desktop entry ----------------------------------------


def test_metainfo_release_and_licence_match_the_package():
    root = metainfo()
    assert root.find("releases/release").get("version") == ws_tracker_tray.__version__
    assert root.findtext("project_license") == PYPROJECT["license"]


def test_metainfo_names_the_app_in_both_languages():
    root = metainfo()
    assert root.findtext("id") == APP_ID
    assert root.findtext("name") == "WS Tracker Tray"
    summaries = {s.get(LANG, "en"): s.text for s in root.findall("summary")}
    assert set(summaries) == {"en", "pl"}
    assert root.find("launchable").text == f"{APP_ID}.desktop"


def test_screenshot_points_to_a_file_in_this_repository():
    image = metainfo().findtext("screenshots/screenshot/image")
    prefix = "https://raw.githubusercontent.com/DragonKing026/Kimai-App--Linux-/main/"
    assert image.startswith(prefix)
    assert (ROOT / image.removeprefix(prefix)).is_file()


def test_desktop_entry_starts_the_installed_command():
    entry = desktop_entry()
    assert entry["Exec"] == "ws-tracker-tray"
    assert "ws-tracker-tray" in PYPROJECT["scripts"]
    assert entry["Icon"] == APP_ID
    assert entry["Name"] == "WS Tracker Tray"
