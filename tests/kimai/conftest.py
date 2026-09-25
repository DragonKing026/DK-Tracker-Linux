"""Contract tests against a local Kimai in Docker (marker `kimai`, not run by default).

    .venv/bin/pytest -m kimai

Uses a running instance when KIMAI_TEST_URL is set (eval "$(tests/kimai/kimai-testowe.sh env)"),
otherwise starts one and stops it afterwards unless KIMAI_TEST_KEEP=1.
"""

import os
import re
import subprocess
from pathlib import Path

import pytest

from kimai_tray.core.kimai_client import KimaiClient
from kimai_tray.core.settings import Memory, Settings
from kimai_tray.core.tracker import Tracker

SCRIPT = Path(__file__).resolve().parent / "kimai-testowe.sh"


@pytest.fixture(scope="session")
def kimai_env():
    if os.environ.get("KIMAI_TEST_URL"):
        yield {key: value for key, value in os.environ.items() if key.startswith("KIMAI_TEST_")}
        return
    output = subprocess.run([str(SCRIPT), "up"], check=True, capture_output=True, text=True).stdout
    yield dict(re.findall(r"export (KIMAI_TEST_\w+)=(\S+)", output))
    if os.environ.get("KIMAI_TEST_KEEP") != "1":
        subprocess.run([str(SCRIPT), "down"], check=True, capture_output=True)


def _stop_everything(client: KimaiClient) -> None:
    for entry in client.active():
        client.stop(entry.id)


def _tracker(env, token_key):
    client = KimaiClient(env["KIMAI_TEST_URL"], env[token_key])
    _stop_everything(client)
    tracker = Tracker(client, Settings(url=env["KIMAI_TEST_URL"]), Memory())
    tracker.load_catalog()
    yield tracker
    _stop_everything(client)
    client.close()


@pytest.fixture
def user_tracker(kimai_env):
    yield from _tracker(kimai_env, "KIMAI_TEST_USER_TOKEN")


@pytest.fixture
def lead_tracker(kimai_env):
    yield from _tracker(kimai_env, "KIMAI_TEST_LEAD_TOKEN")
