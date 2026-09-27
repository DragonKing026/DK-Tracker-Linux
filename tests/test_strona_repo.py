"""Files of the Flatpak repository published on GitHub Pages (flatpak/pages.py)."""

import base64
import configparser
import importlib.util
import re
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


def test_site_writes_both_files_and_the_project_page(tmp_path):
    key = tmp_path / "key.gpg"
    key.write_bytes(KEY)
    pages.write_site(tmp_path / "site", URL + "/", key)
    names = sorted(path.name for path in (tmp_path / "site").iterdir())
    assert names == [
        "dk-tracker.flatpakrepo",
        "dk-tracker.svg",
        "index.html",
        "io.github.dragonking026.DK-Tracker-Linux.flatpakref",
        "okno-ciemny-motyw.png",
        "okno-glowne-edycja.png",
        "okno-glowne-kalendarz.png",
        "okno-glowne-podsumowania.png",
        "okno-glowne-wpisy.png",
        "strona.css",
        "strona.js",
    ]
    index = (tmp_path / "site" / "index.html").read_text(encoding="utf-8")
    assert f"flatpak install --user {URL}/io.github.dragonking026.DK-Tracker-Linux.flatpakref" in index
    assert "{{" not in index


def test_page_shows_the_newest_release_from_the_metainfo_file(tmp_path):
    metainfo = tmp_path / "app.metainfo.xml"
    metainfo.write_text(
        "<component><releases>"
        '<release version="1.2.3" date="2026-10-01"/><release version="1.2.2" date="2026-09-30"/>'
        "</releases></component>",
        encoding="utf-8",
    )
    version, date = pages.latest_release(metainfo)
    assert (version, date) == ("1.2.3", "2026-10-01")
    index = pages.index_html(URL, version, date)
    assert "wersja 1.2.3 · 2026-10-01" in index and "version 1.2.3 · 2026-10-01" in index


def test_page_links_only_files_the_site_has():
    """Relative links and assets of the page must exist next to it on Pages."""
    index = pages.index_html(URL, "1.0.0", "2026-10-01")
    published = {
        "dk-tracker.flatpakrepo",
        "io.github.dragonking026.DK-Tracker-Linux.flatpakref",
        "strona.css",
        "strona.js",
        "dk-tracker.svg",
        "okno-ciemny-motyw.png",
        "okno-glowne-wpisy.png",
        "okno-glowne-edycja.png",
        "okno-glowne-podsumowania.png",
        "okno-glowne-kalendarz.png",
    }
    local = {ref for ref in re.findall(r'(?:href|src)="([^"#:]+)"', index)}
    assert local and local <= published


def test_page_loads_nothing_from_other_servers():
    """No telemetry: scripts, styles and images come from the site itself."""
    index = pages.index_html(URL, "1.0.0", "2026-10-01")
    assert not re.search(r'<(script|img|link)[^>]+(src|href)="https?://(?!dragonking026\.github\.io)', index)
    assert "http" not in (pages.PAGE / "strona.css").read_text(encoding="utf-8")
