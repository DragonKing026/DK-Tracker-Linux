"""Files of the Flatpak repository published on GitHub Pages (flatpak/pages.py)."""

import base64
import configparser
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("pages", ROOT / "flatpak" / "pages.py")
pages = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pages)

URL = "https://dragonking026.github.io/Kimai-App--Linux-"
KEY = b"\x99\x01\x0dfake public key bytes"


def parse(text: str, section: str) -> dict[str, str]:
    parser = configparser.ConfigParser(interpolation=None)
    parser.optionxform = str
    parser.read_string(text)
    return dict(parser[section])


def test_repo_file_lets_flatpak_add_the_remote():
    data = parse(pages.flatpakrepo(URL, KEY), "Flatpak Repo")
    assert data["Url"] == f"{URL}/repo/"
    assert data["Title"] == "WS Tracker Tray"
    assert base64.b64decode(data["GPGKey"]) == KEY
    assert "RuntimeRepo" not in data  # a .flatpakref key only (flatpak command reference)


def test_ref_file_installs_the_app_from_that_remote():
    data = parse(pages.flatpakref(URL, KEY), "Flatpak Ref")
    assert (data["Name"], data["Branch"], data["IsRuntime"]) == (
        "pl.websystems.WsTrackerTray",
        "master",
        "false",
    )
    assert data["Url"] == f"{URL}/repo/"
    assert data["SuggestRemoteName"] == "ws-tracker-tray"
    assert base64.b64decode(data["GPGKey"]) == KEY


def test_site_writes_both_files_and_an_index(tmp_path):
    key = tmp_path / "key.gpg"
    key.write_bytes(KEY)
    pages.write_site(tmp_path / "site", URL + "/", key)
    names = sorted(path.name for path in (tmp_path / "site").iterdir())
    assert names == ["index.html", "pl.websystems.WsTrackerTray.flatpakref", "ws-tracker-tray.flatpakrepo"]
    index = (tmp_path / "site" / "index.html").read_text(encoding="utf-8")
    assert f"flatpak install --user {URL}/pl.websystems.WsTrackerTray.flatpakref" in index
