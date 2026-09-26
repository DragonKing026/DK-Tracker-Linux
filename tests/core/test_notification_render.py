from ws_tracker_tray.core.i18n import Translator
from ws_tracker_tray.core.notification_policy import Notification, entry_id_from, render


def test_render_long_timer_in_polish():
    note = Notification(
        "long-timer-7",
        "notifLongTimerTitle",
        "notifLongTimerBody",
        {"time": "8:00", "project": "Moduł rezerwacji", "description": "Formularz"},
        ("stop", "keep"),
        entry_id=7,
    )
    rendered = render(note, Translator("pl"))
    assert rendered.id == "long-timer-7"
    assert rendered.title == "Timer działa od 8:00"
    assert rendered.body == "Moduł rezerwacji — Formularz"
    assert rendered.buttons == (("Zatrzymaj", "stop"), ("Działa dalej", "keep"))


def test_render_without_body_and_buttons_in_english():
    rendered = render(Notification("connection", "notifConnectionRestored"), Translator("en"))
    assert (rendered.title, rendered.body, rendered.buttons) == ("Connection to Kimai restored", "", ())


def test_entry_id_from_notification_id():
    assert entry_id_from("long-timer-123") == 123
    assert entry_id_from("connection") is None
    assert entry_id_from("long-timer-abc") is None


def test_entry_id_from_ignores_non_ascii_digits():
    assert entry_id_from("long-timer-²") is None
    assert entry_id_from("long-timer-٣") is None


def test_our_notification_ids_are_recognised():
    from ws_tracker_tray.core.notification_policy import is_ours

    assert is_ours("action.1790374275")
    assert is_ours("connection.12")
    assert is_ours("long-timer-7.1790374275")
    assert not is_ours("action")  # we always add a number
    assert not is_ours("org.kde.kdeconnect.3")
    assert not is_ours("settings-reminder.5")
    assert not is_ours("long-timer-x.5")
