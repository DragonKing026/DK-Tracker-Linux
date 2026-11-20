"""The Qt guard (flatpak/straznik.py) on canned PyPI and Qt repository answers — no network."""

import datetime as dt
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("straznik", ROOT / "flatpak" / "straznik.py")
straznik = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(straznik)

TODAY = dt.date(2026, 11, 20)
QT_DIR = straznik.QT_REPO.format(v="6114")


def _release(day: str, yanked: bool = False) -> list[dict]:
    return [{"upload_time": f"{day}T12:00:00", "yanked": yanked}]


def _wheel_files(name: str, version: str) -> list[dict]:
    stem = name.replace("-", "_")
    return [
        {
            "filename": f"{stem}-{version}-cp310-abi3-manylinux_{glibc}_x86_64.whl",
            "url": f"https://files.example/{stem}-{version}-cp310-abi3-manylinux_{glibc}_x86_64.whl",
            "digests": {"sha256": hashlib.sha256(f"{name}{glibc}".encode()).hexdigest()},
        }
        for glibc in ("2_39", "2_34")
    ] + [{"filename": f"{stem}-{version}-cp310-abi3-win_amd64.whl", "url": "x", "digests": {"sha256": "0"}}]


def fake_fetch(releases: dict) -> callable:
    archives = {part: f"{part} bytes".encode() for part in straznik.QT_PARTS}
    names = {
        part: f"6.11.4-0-202612010000{part}-Linux-RHEL_9_6-GCC-Linux-RHEL_9_6-X86_64.7z" for part in archives
    }
    pages = {
        straznik.PYPI.format(name="pyside6-essentials"): json.dumps({"releases": releases}).encode(),
        QT_DIR: "".join(f'<a href="{n}">{n}</a><a href="{n}.sha1">' for n in names.values()).encode(),
    }
    for name in straznik.WHEELS:
        url = straznik.PYPI.format(name=name).replace("/json", "/6.11.4/json")
        pages[url] = json.dumps({"urls": _wheel_files(name, "6.11.4")}).encode()
    for part, name in names.items():
        pages[QT_DIR + name] = archives[part]
        pages[QT_DIR + name + ".sha1"] = hashlib.sha1(archives[part]).hexdigest().encode() + b"\n"  # noqa: S324
    return pages.__getitem__


def test_manifest_pins_one_version():
    assert straznik.bundled_version(straznik.MANIFEST.read_text(encoding="utf-8")) == "6.11.3"


def test_range_comes_from_pyproject():
    assert straznik.ui_range() == ("6.11", "6.12")


def test_newest_skips_out_of_range_yanked_and_too_fresh_releases():
    releases = {
        "6.11.3": _release("2026-10-26"),
        "6.11.4": _release("2026-11-10"),
        "6.11.5": _release("2026-11-18"),  # 2 days old: cooldown
        "6.11.9": _release("2026-11-01", yanked=True),
        "6.12.0": _release("2026-11-01"),  # outside <6.12
        "6.11.4rc1": _release("2026-11-01"),
    }
    assert straznik.newest_version(fake_fetch(releases), "6.11", "6.12", TODAY) == "6.11.4"


def test_update_moves_wheels_and_qt_headers_together():
    text = straznik.MANIFEST.read_text(encoding="utf-8")
    updated = straznik.update(text, fake_fetch({}), "6.11.4")
    assert "6.11.3" not in updated
    assert "shiboken6-6.11.4-cp310-abi3-manylinux_2_34_x86_64.whl" in updated  # the lowest glibc
    assert hashlib.sha256(b"qtbase bytes").hexdigest() in updated
    assert updated.count("6.11.4-0-202612010000") == 3


def test_update_refuses_a_qt_archive_with_a_wrong_checksum():
    get = fake_fetch({})

    def tampered(url: str) -> bytes:
        return (
            b"other bytes" if url.endswith("qtbase-Linux-RHEL_9_6-GCC-Linux-RHEL_9_6-X86_64.7z") else get(url)
        )

    with pytest.raises(SystemExit, match="sha1 mismatch"):
        straznik.update(straznik.MANIFEST.read_text(encoding="utf-8"), tampered, "6.11.4")


def test_check_exits_10_only_when_a_newer_release_exists(capsys):
    newer = fake_fetch({"6.11.4": _release("2026-11-01")})
    assert straznik.main(["sprawdz"], newer, TODAY) == straznik.EXIT_NEWER
    same = fake_fetch({"6.11.3": _release("2026-10-26")})
    assert straznik.main(["sprawdz"], same, TODAY) == 0
    assert "w paczce: 6.11.3" in capsys.readouterr().out
    assert straznik.main(["cokolwiek"]) == 2
