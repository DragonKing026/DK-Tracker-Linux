"""Real session-bus tests (marker `desktop`): `.venv/bin/pytest -m desktop`.

They touch the user's desktop: a test item in the wallet (removed at the end), a notification
(withdrawn) and a background request with autostart=False (no autostart entry is created).
"""

import os

import pytest

from kimai_tray.core.i18n import Translator
from kimai_tray.core.notification_policy import Notification, render
from kimai_tray.desktop.autostart import BackgroundPortal
from kimai_tray.desktop.bus import SessionBus
from kimai_tray.desktop.notifications import PortalNotifier
from kimai_tray.desktop.secrets import SecretServiceStore

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
    store = SecretServiceStore(bus, application="pl.websystems.KimaiTray.TEST")
    try:
        store.set(URL, "test-token-123")
        assert store.get(URL) == "test-token-123"
    finally:
        store.delete(URL)
    assert store.get(URL) is None


def test_notification_can_be_shown_and_withdrawn(bus):
    notifier = PortalNotifier(bus)
    note = render(Notification("kimai-tray-test", "notifConnectionRestored"), Translator("pl"))
    notifier.show(note)
    notifier.withdraw(note.id)


def test_background_request_without_autostart(bus):
    result = BackgroundPortal(bus).request(autostart=False, reason="Kimai Tray — test")
    assert result.autostart is False
    assert isinstance(BackgroundPortal(bus).set_status("Kimai Tray — test"), bool)
