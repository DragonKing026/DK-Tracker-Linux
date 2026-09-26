"""Files of the Flatpak repository published on GitHub Pages (flatpak/pages.py)."""

import base64
import configparser
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("pages", ROOT / "flatpak" / "pages.py")
pages = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pages)

URL = "https://dragonking026.github.io/DK-Tracker-Linux"
KEY = b"\x99\x01\x0dfake public key bytes"


def parse(text: str, section: str) -> dict[str, str]:
    parser = configparser.ConfigParser(interpolation=None)
    parser.optionxform = str
    parser.read_string(text)
    return dict(parser[section])


def test_repo_file_lets_flatpak_add_the_remote():
    data = parse(pages.flatpakrepo(URL, KEY), "Flatpak Repo")
    assert data["Url"] == f"{URL}/repo/"
    assert data["Title"] == "DK Tracker"
    assert base64.b64decode(data["GPGKey"]) == KEY
    assert "RuntimeRepo" not in data  # a .flatpakref key only (flatpak command reference)


def test_ref_file_installs_the_app_from_that_remote():
    data = parse(pages.flatpakref(URL, KEY), "Flatpak Ref")
    assert (data["Name"], data["Branch"], data["IsRuntime"]) == (
        "io.github.dragonking026.DK-Tracker-Linux",
        "master",
        "false",
    )
    assert data["Url"] == f"{URL}/repo/"
    assert data["SuggestRemoteName"] == "dk-tracker"
    assert base64.b64decode(data["GPGKey"]) == KEY


def test_site_writes_both_files_and_an_index(tmp_path):
    key = tmp_path / "key.gpg"
    key.write_bytes(KEY)
    pages.write_site(tmp_path / "site", URL + "/", key)
    names = sorted(path.name for path in (tmp_path / "site").iterdir())
    assert names == [
        "dk-tracker.flatpakrepo",
        "index.html",
        "io.github.dragonking026.DK-Tracker-Linux.flatpakref",
    ]
    index = (tmp_path / "site" / "index.html").read_text(encoding="utf-8")
    assert f"flatpak install --user {URL}/io.github.dragonking026.DK-Tracker-Linux.flatpakref" in index
