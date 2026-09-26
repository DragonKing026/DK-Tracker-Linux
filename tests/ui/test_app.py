from datetime import timedelta

import pytest

from kimai_tray.core.errors import ApiError, ErrorKind
from kimai_tray.core.settings import Memory, Settings
from kimai_tray.desktop.autostart import BackgroundResult
from kimai_tray.desktop.notifications import NotificationAction
from kimai_tray.desktop.secrets import SecretsLocked
from kimai_tray.ui.app import Controller

from ..core.fakes import NOW, FakeClient, make_entry

URL = "https://kimai.test"


class FakeDesktop:
    def __init__(self, token="secret-token", fail=None):
        self.tokens = {URL: token} if token else {}
        self.fail = fail
        self.notified = []
        self.withdrawn = []
        self.background = []

    def get_token(self, url):
        if self.fail:
            raise self.fail
        return self.tokens.get(url)

    def set_token(self, url, token):
        self.tokens[url] = token

    def notify(self, rendered):
        self.notified.append(rendered)

    def withdraw(self, notification_id):
        self.withdrawn.append(notification_id)

    def request_background(self, *, autostart, reason):
        self.background.append(autostart)
        return BackgroundResult(True, autostart)

    def set_status(self, message):
        return False

    def close(self):
        pass


class Harness:
    def __init__(self, qtbot, *, settings=None, desktop=None, client=None, tray=True):
        self.client = client or FakeClient()
        self.desktop = desktop or FakeDesktop()
        self.saved_settings = []
        self.saved_memory = []
        self.clients = []

        def factory(url, token):
            self.clients.append((url, token))
            return self.client

        self.controller = Controller(
            settings=settings if settings is not None else Settings(url=URL, language="pl"),
            memory=Memory(),
            desktop=self.desktop,
            client_factory=factory,
            save_settings=self.saved_settings.append,
            save_memory=self.saved_memory.append,
            now=lambda: self.client.now,
            tray_available=tray,
            window_mode="frameless" if tray else "window",
            listen_for_clicks=False,
        )
        qtbot.addWidget(self.controller.popup)
        self.qtbot = qtbot

    @property
    def state(self):
        return self.controller.state

    def start(self):
        self.controller.start(hidden=True)
        return self

    def settle(self):
        self.qtbot.waitUntil(self.controller.idle, timeout=3000)


@pytest.fixture
def harness(qtbot):
    made = []

    def make(**kwargs):
        made.append(Harness(qtbot, **kwargs).start())
        made[-1].settle()
        return made[-1]

    yield make
    for item in made:
        item.controller.shutdown()


def test_without_an_address_the_app_asks_for_settings(harness):
    h = harness(settings=Settings())
    assert h.state.configured is False
    assert h.controller.tray.status.kind == "unconfigured"
    assert h.clients == []


def test_token_from_the_wallet_configures_the_tracker(harness):
    h = harness()
    assert h.clients == [(URL, "secret-token")]
    assert h.state.configured is True
    assert h.state.snapshot.user.username == "jan"


def test_locked_wallet_is_reported(harness):
    h = harness(desktop=FakeDesktop(fail=SecretsLocked("dismissed")))
    assert h.state.configured is False
    assert h.state.secrets_problem == "secretsLocked"


def test_start_from_the_window(harness):
    h = harness()
    h.controller.popup.form.startRequested.emit(
        {"project_id": 1, "activity_id": 1, "description": "Walidacja dat przyjazdu", "billable": None}
    )
    h.settle()
    assert h.state.snapshot.current.description == "Walidacja dat przyjazdu"
    assert h.controller.tray.status.kind == "running"


def test_rule_errors_are_shown_in_the_window(harness):
    h = harness()
    h.controller.popup.form.startRequested.emit(
        {"project_id": None, "activity_id": 1, "description": "Walidacja dat przyjazdu", "billable": None}
    )
    h.settle()
    assert h.controller.popup.error.text() == "Wybierz projekt."


def test_stop_from_the_menu_is_confirmed(harness):
    client = FakeClient()
    client.add(make_entry(7, NOW - timedelta(minutes=30)))
    h = harness(client=client)
    h.controller.tray.stopRequested.emit()
    h.settle()
    assert h.state.snapshot.current is None
    assert [n.title for n in h.desktop.notified] == ["Stop: 0:30 — Moduł rezerwacji"]


def test_long_timer_notification_after_a_refresh(harness):
    client = FakeClient()
    client.add(make_entry(7, NOW - timedelta(hours=9)))
    h = harness(client=client)
    assert h.desktop.notified[0].id == "long-timer-7"
    assert h.desktop.notified[0].buttons == (("Zatrzymaj", "stop"), ("Działa dalej", "keep"))


def test_stop_clicked_in_a_notification_stops_that_entry(harness):
    client = FakeClient()
    client.add(make_entry(7, NOW - timedelta(hours=9)))
    h = harness(client=client)
    h.controller.on_notification(NotificationAction("long-timer-8", "stop", 8))  # another entry: ignored
    h.settle()
    assert h.state.snapshot.current is not None
    h.controller.on_notification(NotificationAction("long-timer-7", "stop", 7))
    h.settle()
    assert h.state.snapshot.current is None


def test_saving_settings_stores_the_token_and_switches_language(harness):
    h = harness()
    h.controller.save_settings(Settings(url=URL, language="en", autostart=True), "new-token")
    h.settle()
    assert h.desktop.tokens[URL] == "new-token"
    assert h.saved_settings[-1].language == "en"
    assert h.clients[-1] == (URL, "new-token")
    assert h.controller.tray.quit_action.text() == "Quit"
    assert h.desktop.background == [True]


def test_connection_test_reports_the_user(harness):
    h = harness()
    dialog = h.controller.open_settings()
    dialog.testRequested.emit(URL, "")
    h.settle()
    assert dialog.status.text() == "Połączono jako jan."


def test_open_kimai_uses_the_remembered_locale(harness, monkeypatch):
    opened = []
    monkeypatch.setattr(
        "kimai_tray.ui.app.QDesktopServices.openUrl", lambda url: opened.append(url.toString())
    )
    h = harness()
    h.controller.tray.openKimaiRequested.emit()
    assert opened == ["https://kimai.test/en/timesheet/"]


def test_window_open_before_the_token_arrives_still_gets_projects(qtbot):
    h = Harness(qtbot)
    h.controller.start(hidden=False)  # the window opens at once, the wallet answers later
    h.settle()
    form = h.controller.popup.form
    assert form.project.findData(1) > 0
    assert form.activity.findData(1) > 0
    h.controller.shutdown()


def test_failed_actions_are_logged_without_the_token(harness, caplog):
    h = harness()
    h.client.fail["start"] = [ApiError(ErrorKind.REJECTED, 400, "Overlapping entry")]
    with caplog.at_level("WARNING", logger="kimai_tray.ui.app"):
        h.controller.popup.form.startRequested.emit(
            {"project_id": 1, "activity_id": 1, "description": "Walidacja dat przyjazdu", "billable": None}
        )
        h.settle()
    assert "Overlapping entry" in caplog.text
    assert "secret-token" not in caplog.text


def test_without_a_tray_the_window_explains_it_for_this_session_only(harness):
    h = harness(tray=False)
    assert h.controller.tray is None
    assert h.controller.popup.isVisible()  # no icon to click, so the window opens at start
    h.controller.refresh_active()
    h.settle()
    assert ("hintNoTray", {}) in h.state.warnings
    assert h.saved_memory[-1].tray_hint_shown is True  # the next start stays quiet


def test_a_handled_notification_is_withdrawn(harness):
    client = FakeClient()
    client.add(make_entry(7, NOW - timedelta(hours=9)))
    h = harness(client=client)
    h.controller.on_notification(NotificationAction("long-timer-7", "stop", 7))
    h.settle()
    assert h.desktop.withdrawn == ["long-timer-7"]
    h.controller.on_notification(NotificationAction("long-timer-7", "keep", 7))
    h.settle()
    assert h.desktop.withdrawn == ["long-timer-7", "long-timer-7"]


def test_window_size_chosen_by_the_user_is_remembered(harness):
    from PySide6.QtCore import QSize

    h = harness()
    h.controller.popup.sizeChosen.emit(QSize(540, 700))
    h.settle()
    assert (h.saved_memory[-1].popup_width, h.saved_memory[-1].popup_height) == (540, 700)


def test_remembered_size_is_used_at_start(qtbot):
    from PySide6.QtCore import QSize

    controller = Controller(
        settings=Settings(url=URL),
        memory=Memory(popup_width=520, popup_height=650),
        desktop=FakeDesktop(),
        client_factory=lambda url, token: FakeClient(),
        save_settings=lambda settings: None,
        save_memory=lambda memory: None,
        tray_available=True,
        window_mode="frameless",
        listen_for_clicks=False,
    )
    qtbot.addWidget(controller.popup)
    assert controller.popup.width() == 520  # low while not configured, but as wide as the user left it
    controller.state.update(configured=True)
    assert controller.popup.size() == QSize(520, 650)
    controller.shutdown()


def test_tray_click_toggles_the_window(harness):
    h = harness()
    popup = h.controller.popup
    h.controller.toggle_popup()
    assert popup.isVisible()
    h.controller.toggle_popup()
    assert not popup.isVisible()


def test_click_that_took_the_focus_away_does_not_reopen_the_window(harness):
    h = harness()
    popup = h.controller.popup
    h.controller.show_popup()
    popup.hide_after_focus_loss()  # the click on the panel took the focus first...
    h.controller.toggle_popup()  # ...then the same click reached the icon
    assert not popup.isVisible()


def test_activities_of_a_project_no_longer_chosen_are_ignored(harness):
    h = harness()
    form = h.controller.popup.form
    form.set_catalog(h.state.snapshot.__class__(projects=tuple(h.client.projects_list)), 1)
    form.select_project(2)
    h.settle()
    from kimai_tray.core.models import Activity

    stale = [Activity(99, "Z innego projektu", True, 1)]
    h.controller._apply_activities(1, stale)  # an answer for project 1 arriving after 2 was chosen
    assert form.activity.findData(99) == -1


def test_connection_test_never_sends_the_stored_token_to_another_address(harness):
    h = harness()
    dialog = h.controller.open_settings()
    dialog.testRequested.emit("https://inny.example.com", "")
    h.settle()
    assert ("https://inny.example.com", "secret-token") not in h.clients
    assert dialog.status.text() == "Podaj token API."
