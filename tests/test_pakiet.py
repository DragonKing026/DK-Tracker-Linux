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


# -- Task 3: the Flatpak manifest --------------------------------------------------


def manifest() -> dict:
    import yaml

    return yaml.safe_load((ROOT / "flatpak" / f"{APP_ID}.yml").read_text(encoding="utf-8"))


def test_manifest_builds_on_the_kde_runtime_with_pyside():
    data = manifest()
    assert data["id"] == APP_ID
    assert (data["runtime"], data["runtime-version"]) == ("org.kde.Platform", "6.11")
    assert (data["base"], data["base-version"]) == ("io.qt.PySide.BaseApp", "6.11")


def test_permissions_are_exactly_those_of_the_specification():
    """Spec, section 8 — nothing more (no home directory, no session bus at large)."""
    assert set(manifest()["finish-args"]) == {
        "--share=network",
        "--share=ipc",
        "--socket=wayland",
        "--socket=fallback-x11",
        "--device=dri",
        "--talk-name=org.kde.StatusNotifierWatcher",
        "--talk-name=org.freedesktop.secrets",
    }


def test_autostart_runs_the_command_the_manifest_installs():
    from ws_tracker_tray.ui.desktop_bridge import AUTOSTART_COMMAND

    assert manifest()["command"] == AUTOSTART_COMMAND[0] == "ws-tracker-tray"


def test_bundled_python_libraries_satisfy_pyproject():
    import re

    import yaml
    from packaging.requirements import Requirement

    deps = yaml.safe_load((ROOT / "flatpak" / "python3-deps.yaml").read_text(encoding="utf-8"))
    wheels = {
        m.group(1).lower(): m.group(2)
        for module in deps["modules"]
        for source in module["sources"]
        if (m := re.search(r"/([A-Za-z0-9_]+)-([0-9][^-]*)-py3-none-any\.whl$", source["url"]))
    }
    for requirement in map(Requirement, PYPROJECT["dependencies"]):
        assert requirement.name in wheels, requirement.name
        version = wheels[requirement.name]
        assert requirement.specifier.contains(version), (requirement, version)
    assert "python3-deps.yaml" in manifest()["modules"]


def test_build_does_not_copy_the_virtualenv_or_git():
    app = next(m for m in manifest()["modules"] if isinstance(m, dict) and m["name"] == "ws-tracker-tray")
    skipped = set(app["sources"][0]["skip"])
    assert {".venv", ".git"} <= skipped


# -- Task 6: GitHub Actions and the signing key ------------------------------------


def workflow(name: str) -> dict:
    import yaml

    return yaml.safe_load((ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8"))


def test_release_builds_in_the_same_container_as_the_local_script():
    import re

    script = (ROOT / "flatpak" / "buduj.sh").read_text(encoding="utf-8")
    local_image = re.search(r"^IMAGE=(\S+)$", script, re.M).group(1)
    job = workflow("wydanie.yml")["jobs"]["flatpak"]
    assert job["container"]["image"] == local_image
    builder = next(step for step in job["steps"] if "flatpak-builder" in step.get("uses", ""))
    assert builder["with"]["manifest-path"] == f"flatpak/{APP_ID}.yml"


def test_release_runs_only_for_version_tags():
    triggers = workflow("wydanie.yml")[True]  # YAML 1.1 reads the key "on" as True
    assert triggers == {"push": {"tags": ["v*"]}}


# -- Final review of Plan 4: release order, gates and permissions -------------------


def test_release_waits_for_the_tests():
    jobs = workflow("wydanie.yml")["jobs"]
    assert jobs["testy"]["uses"] == "./.github/workflows/testy.yml"
    assert "testy" in jobs["flatpak"]["needs"]
    assert "workflow_call" in workflow("testy.yml")[True]


def test_release_is_created_only_after_the_repository_is_on_pages():
    """A release pointing at a .flatpakref that is not online yet would install nothing."""
    jobs = workflow("wydanie.yml")["jobs"]
    assert jobs["pages"]["needs"] == "flatpak"
    assert jobs["wydanie"]["needs"] == "pages"
    assert not any("action-gh-release" in step.get("uses", "") for step in jobs["flatpak"]["steps"])


def test_only_the_jobs_that_need_them_get_write_permissions():
    data = workflow("wydanie.yml")
    assert data["permissions"] == {"contents": "read"}
    jobs = data["jobs"]
    assert jobs["pages"]["permissions"] == {"pages": "write", "id-token": "write"}
    assert jobs["wydanie"]["permissions"] == {"contents": "write"}
    assert "permissions" not in jobs["flatpak"]  # the job holding the GPG key keeps read-only access


def test_build_does_not_copy_what_the_ci_action_leaves_in_the_checkout():
    app = next(m for m in manifest()["modules"] if isinstance(m, dict) and m["name"] == "ws-tracker-tray")
    assert {"flatpak_app", "repo", "site", "dist"} <= set(app["sources"][0]["skip"])
