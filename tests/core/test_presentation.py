from dataclasses import replace
from datetime import UTC, date, datetime, timedelta
from zoneinfo import ZoneInfo

from ws_tracker_tray.core.errors import ApiError, ErrorKind
from ws_tracker_tray.core.i18n import Translator
from ws_tracker_tray.core.presentation import day_label, display_zone, entry_row, tray_status
from ws_tracker_tray.core.tracker import Snapshot, Totals

from .fakes import NOW, FakeClient, make_entry

WARSAW = ZoneInfo("Europe/Warsaw")
PL = Translator("pl")
USER = FakeClient().user


def running(minutes, **kwargs):
    return make_entry(7, NOW - timedelta(minutes=minutes), **kwargs)


def test_unconfigured_has_no_label():
    status = tray_status(Snapshot(), False, NOW, PL)
    assert (status.kind, status.label) == ("unconfigured", "")
    assert status.tooltip == "WS Tracker Tray\nAplikacja nie jest jeszcze skonfigurowana."


def test_idle_shows_today_total_in_the_tooltip():
    status = tray_status(Snapshot(user=USER, totals=Totals(today=27120, week=0)), True, NOW, PL)
    assert (status.kind, status.label) == ("idle", "")
    assert status.tooltip == "WS Tracker Tray\nNic nie jest mierzone\nDziś 7:32"


def test_running_label_switches_format_at_an_hour():
    assert tray_status(Snapshot(user=USER, running=(running(47),)), True, NOW, PL).label == "47m"
    status = tray_status(Snapshot(user=USER, running=(running(82),)), True, NOW, PL)
    assert (status.kind, status.label) == ("running", "1:22")
    assert status.tooltip == "WS Tracker Tray — 1:22:00\nModuł rezerwacji — Formularz rezerwacji pokoi"


def test_running_without_description_or_project():
    entry = replace(running(5, description=""), project_name=None)
    assert tray_status(Snapshot(user=USER, running=(entry,)), True, NOW, PL).tooltip.endswith("\n(bez opisu)")


def test_several_running_entries_are_counted():
    entries = (running(10), make_entry(8, NOW - timedelta(minutes=90)))
    tooltip = tray_status(Snapshot(user=USER, running=entries), True, NOW, PL).tooltip
    assert tooltip.endswith("\ni jeszcze trwające: 1")


def test_error_wins_over_a_running_entry():
    error = ApiError(ErrorKind.CONNECTION, 0, "down")
    status = tray_status(Snapshot(user=USER, running=(running(5),), error=error), True, NOW, PL)
    assert (status.kind, status.label) == ("error", "!")
    assert status.tooltip == "WS Tracker Tray\nBrak połączenia z Kimai."


def test_display_zone_prefers_the_kimai_account():
    assert display_zone(Snapshot(user=USER), datetime.now(UTC)) == WARSAW
    assert display_zone(Snapshot(), datetime(2026, 1, 1, tzinfo=UTC)) == UTC


def test_day_labels():
    today = date(2026, 9, 25)  # Friday
    assert day_label(today, today, PL) == "Dziś"
    assert day_label(date(2026, 9, 24), today, PL) == "Wczoraj"
    assert day_label(date(2026, 9, 22), today, PL) == "wt., 22 wrz"
    assert day_label(date(2026, 9, 22), today, Translator("en")) == "Tue, 22 Sep"


def test_entry_row_texts():
    entry = make_entry(
        5,
        datetime(2026, 9, 25, 13, 15, tzinfo=UTC),
        datetime(2026, 9, 25, 15, 5, tzinfo=UTC),
        description="Kalendarz\ndostępności",
    )
    row = entry_row(entry, WARSAW, PL)
    assert row.description == "Kalendarz dostępności"
    assert row.empty is False
    assert row.meta == "Moduł rezerwacji - Programowanie"
    assert (row.duration, row.span) == ("1:50", "15:15-17:05")


def test_entry_row_without_description():
    entry = make_entry(5, NOW - timedelta(hours=1), NOW, description="  ")
    row = entry_row(entry, WARSAW, PL)
    assert (row.description, row.empty) == ("(bez opisu)", True)
