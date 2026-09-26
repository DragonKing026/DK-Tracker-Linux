"""Safety checks of the release scripts in flatpak/ (the signing key must match the one users trust)."""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_KEY = "dk-tracker-repo.gpg"

pytestmark = pytest.mark.skipif(
    shutil.which("gpg") is None or shutil.which("ostree") is None, reason="needs gpg and ostree"
)


def new_key(home: Path, name: str) -> str:
    env = {**os.environ, "GNUPGHOME": str(home)}
    subprocess.run(
        [
            "gpg",
            "--batch",
            "--pinentry-mode",
            "loopback",
            "--passphrase",
            "",
            "--quick-gen-key",
            name,
            "ed25519",
            "sign",
            "never",
        ],
        env=env,
        check=True,
        capture_output=True,
    )
    out = subprocess.run(
        ["gpg", "--list-keys", "--with-colons", name], env=env, check=True, capture_output=True, text=True
    ).stdout
    return next(line.split(":")[9] for line in out.splitlines() if line.startswith("fpr"))


@pytest.fixture
def scripts(tmp_path) -> Path:
    target = tmp_path / "flatpak"
    target.mkdir()
    for name in ("publikuj.sh", "pages.py", "klucz-gpg.sh"):
        shutil.copy2(ROOT / "flatpak" / name, target / name)
    return target


def test_publish_refuses_a_key_other_than_the_committed_one(tmp_path, scripts):
    home = tmp_path / "gnupg"
    home.mkdir(mode=0o700)
    trusted = new_key(home, "Trusted <a@example.com>")
    other = new_key(home, "Other <b@example.com>")
    env = {**os.environ, "GNUPGHOME": str(home)}
    exported = subprocess.run(["gpg", "--export", trusted], env=env, check=True, capture_output=True).stdout
    (scripts / PUBLIC_KEY).write_bytes(exported)

    result = subprocess.run(
        [scripts / "publikuj.sh", tmp_path / "repo", tmp_path / "site", "http://127.0.0.1", other, str(home)],
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert trusted in result.stderr and other in result.stderr
    assert not (tmp_path / "site").exists()


def test_key_script_does_not_replace_the_committed_public_key(tmp_path, scripts):
    (scripts / PUBLIC_KEY).write_bytes(b"the key users already trust")
    home = tmp_path / "home"
    home.mkdir()

    result = subprocess.run(
        [scripts / "klucz-gpg.sh"], env={**os.environ, "HOME": str(home)}, capture_output=True, text=True
    )

    assert result.returncode != 0
    assert (scripts / PUBLIC_KEY).read_bytes() == b"the key users already trust"
    assert list(home.iterdir()) == []


def test_publish_stops_when_the_repository_has_no_app(tmp_path, scripts):
    """An empty `ostree refs` would otherwise publish a repository nobody can install from."""
    home = tmp_path / "gnupg"
    home.mkdir(mode=0o700)
    key = new_key(home, "Trusted <a@example.com>")
    env = {**os.environ, "GNUPGHOME": str(home)}
    exported = subprocess.run(["gpg", "--export", key], env=env, check=True, capture_output=True).stdout
    (scripts / PUBLIC_KEY).write_bytes(exported)
    subprocess.run(["ostree", "init", "--mode=archive-z2", f"--repo={tmp_path / 'repo'}"], check=True)

    result = subprocess.run(
        [scripts / "publikuj.sh", tmp_path / "repo", tmp_path / "site", "http://127.0.0.1", key, str(home)],
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "io.github.dragonking026.DK-Tracker-Linux" in result.stderr
    assert not (tmp_path / "site").exists()
