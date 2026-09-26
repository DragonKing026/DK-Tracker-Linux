"""Real session-bus tests (marker `desktop`): `.venv/bin/pytest -m desktop`.

They touch the user's desktop: a test item in the wallet (removed at the end), a notification
(withdrawn) and a background request with autostart=False (no autostart entry is created).
"""

import os

import pytest

from ws_tracker.core.i18n import Translator
from ws_tracker.core.notification_policy import Notification, render
from ws_tracker.desktop.autostart import BackgroundPortal
from ws_tracker.desktop.bus import SessionBus
from ws_tracker.desktop.notifications import PortalNotifier
from ws_tracker.desktop.secrets import SecretServiceStore

pytestmark = pytest.mark.desktop
URL = "https://kimai.test.invalid"


@pytest.fixture
def bus():
    if not os.environ.get("DBUS_SESSION_BUS_ADDRESS"):
        pytest.skip("no session bus")
    connection = SessionBus()
    yield connection
    connection.close()


def test_secret_round_trip(bus):
    store = SecretServiceStore(bus, application="io.github.dragonking026.WS-Tracker-Linux.TEST")
    try:
        store.set(URL, "test-token-123")
        assert store.get(URL) == "test-token-123"
    finally:
        store.delete(URL)
    assert store.get(URL) is None


def test_notification_can_be_shown_and_withdrawn(bus):
    notifier = PortalNotifier(bus)
    note = render(Notification("ws-tracker-test", "notifConnectionRestored"), Translator("pl"))
    notifier.show(note)
    notifier.withdraw(note.id)


def test_background_request_without_autostart(bus):
    result = BackgroundPortal(bus).request(autostart=False, reason="WS Tracker — test")
    assert result.autostart is False
    assert isinstance(BackgroundPortal(bus).set_status("WS Tracker — test"), bool)
