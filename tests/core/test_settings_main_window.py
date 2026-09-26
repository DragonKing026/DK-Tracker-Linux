"""Plan 5: the tray can be turned off; the main window's size and view are remembered."""

from dk_tracker.core.settings import Memory, Settings, load_json, save_json


def test_tray_is_on_by_default_and_can_be_turned_off(tmp_path):
    assert Settings().show_tray is True
    path = tmp_path / "settings.json"
    save_json(Settings(url="https://kimai.test", show_tray=False), path)
    assert load_json(Settings, path).show_tray is False


def test_main_window_size_and_view_are_remembered(tmp_path):
    memory = Memory()
    assert (memory.main_width, memory.main_height, memory.main_view) == (1000, 700, "entries")
    path = tmp_path / "state.json"
    save_json(Memory(main_width=1200, main_height=800, main_view="entries"), path)
    loaded = load_json(Memory, path)
    assert (loaded.main_width, loaded.main_height) == (1200, 800)


def test_settings_from_an_older_version_get_the_tray_on(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text('{"url": "https://kimai.test"}', encoding="utf-8")
    assert load_json(Settings, path).show_tray is True


def test_the_theme_follows_the_system_unless_chosen():
    """User's choice (live test of 0.10.0): Systemowy / Jasny / Ciemny in the settings."""
    assert Settings().theme == "auto"
    assert Settings(theme="dark").normalized().theme == "dark"
    assert Settings(theme="fioletowy").normalized().theme == "auto"  # an unknown value from an old file
