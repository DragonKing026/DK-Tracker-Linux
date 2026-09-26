import logging
import subprocess
import sys
import uuid

from PySide6.QtCore import QCoreApplication

from ws_tracker_tray.ui.main import QtTranslations, SingleInstance, parse_args, setup_logging


def test_hidden_flag():
    assert parse_args(["--hidden"]).hidden is True
    assert parse_args([]).hidden is False


def test_second_instance_asks_the_first_to_show_its_window(qtbot):
    name = f"ws-tracker-tray-test-{uuid.uuid4().hex[:8]}"
    first = SingleInstance(name)
    assert first.claim() is True
    second = SingleInstance(name)
    with qtbot.waitSignal(first.showRequested, timeout=3000):
        assert second.claim() is False
    first.release()


def test_a_stale_server_name_is_taken_over(qtbot):
    name = f"ws-tracker-tray-test-{uuid.uuid4().hex[:8]}"
    crashed = SingleInstance(name)
    crashed.claim()
    crashed.server.close()  # the socket file of a crashed instance stays; nobody answers
    assert SingleInstance(name).claim() is True


def test_log_file_rotates_and_says_where_it_is(tmp_path):
    path = setup_logging(tmp_path / "state", level=logging.INFO)
    logging.getLogger("ws_tracker_tray.test").info("hello")
    for handler in logging.getLogger().handlers:
        handler.flush()
    assert path == tmp_path / "state" / "ws-tracker-tray.log"
    assert "hello" in path.read_text(encoding="utf-8")
    logging.getLogger().handlers.clear()


def test_qt_standard_texts_follow_the_language(qapp):
    translations = QtTranslations()
    translations.switch("pl")
    assert QCoreApplication.translate("QPlatformTheme", "Cancel") == "Anuluj"
    translations.switch("en")
    assert QCoreApplication.translate("QPlatformTheme", "Cancel") == "Cancel"


def test_module_runs_and_shows_help():
    result = subprocess.run(
        [sys.executable, "-m", "ws_tracker_tray", "--help"], capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0
    assert "--hidden" in result.stdout


def test_when_the_socket_cannot_be_opened_the_app_still_starts(qtbot, caplog):
    instance = SingleInstance("/nonexistent-dir/ws-tracker-tray-test")  # listen() fails here
    with caplog.at_level("WARNING", logger="ws_tracker_tray.ui.main"):
        assert instance.claim() is True
    assert "single instance" in caplog.text
