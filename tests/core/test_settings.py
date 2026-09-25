import json

from kimai_tray.core.settings import Memory, Settings, config_path, load_json, save_json, state_path


def test_missing_file_gives_defaults(tmp_path):
    assert load_json(Settings, tmp_path / "nope.json") == Settings()


def test_round_trip(tmp_path):
    path = tmp_path / "sub" / "settings.json"
    save_json(Settings(url="https://k.test", language="pl"), path)
    assert load_json(Settings, path) == Settings(url="https://k.test", language="pl")
    assert not (tmp_path / "sub" / "settings.tmp").exists()


def test_corrupt_file_gives_defaults(tmp_path):
    path = tmp_path / "state.json"
    path.write_text("{not json", encoding="utf-8")
    assert load_json(Memory, path) == Memory()


def test_unknown_keys_are_ignored(tmp_path):
    path = tmp_path / "state.json"
    path.write_text(json.dumps({"last_project": 3, "from_the_future": True}), encoding="utf-8")
    assert load_json(Memory, path) == Memory(last_project=3)


def test_normalized_cleans_input():
    settings = Settings(
        url="  https://k.test/kimai//  ", min_description=-3, long_timer_hours=-1
    ).normalized()
    assert settings.url == "https://k.test/kimai"
    assert (settings.min_description, settings.long_timer_hours) == (0, 0.0)


def test_http_warning():
    assert Settings(url="http://k.test").warnings() == ["warnHttp"]
    assert Settings(url="https://k.test").warnings() == []


def test_paths_follow_xdg(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "cfg"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    assert config_path() == tmp_path / "cfg" / "kimai-tray" / "settings.json"
    assert state_path() == tmp_path / "state" / "kimai-tray" / "state.json"


def test_settings_file_never_contains_a_token(tmp_path):
    path = tmp_path / "settings.json"
    save_json(Settings(url="https://k.test"), path)
    assert "token" not in path.read_text(encoding="utf-8").lower()
