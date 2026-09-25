from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from kimai_tray.core.errors import ApiError, ErrorKind
from kimai_tray.core.settings import Memory, Settings
from kimai_tray.core.tracker import Snapshot, Totals, Tracker, all_entries_url, live_totals

from .fakes import NOW, FakeClient, make_entry

WAW = ZoneInfo("Europe/Warsaw")


def make_tracker(client=None, memory=None, local_tz=WAW):
    client = client or FakeClient()
    saved = []
    tracker = Tracker(
        client,
        Settings(url="https://kimai.test"),
        memory or Memory(),
        save_memory=saved.append,
        now=lambda: client.now,
        local_now=lambda: client.now.astimezone(local_tz),
    )
    return tracker, client, saved


def test_refresh_active_idle():
    tracker, _, _ = make_tracker()
    snapshot = tracker.refresh_active()
    assert snapshot.running == ()
    assert snapshot.user.username == "jan"
    assert (snapshot.error, snapshot.failures) == (None, 0)


def test_refresh_active_orders_running_newest_first():
    tracker, client, _ = make_tracker()
    older = client.add(make_entry(1, NOW - timedelta(hours=2)))
    newer = client.add(make_entry(2, NOW - timedelta(minutes=5)))
    snapshot = tracker.refresh_active()
    assert snapshot.running == (newer, older)
    assert snapshot.current == newer


def test_refresh_failures_are_counted_and_keep_last_data():
    tracker, client, _ = make_tracker()
    running = client.add(make_entry(1, NOW - timedelta(minutes=5)))
    tracker.refresh_active()
    client.fail["active"] = [ApiError(ErrorKind.CONNECTION, 0), ApiError(ErrorKind.CONNECTION, 0)]
    assert tracker.refresh_active().failures == 1
    snapshot = tracker.refresh_active()
    assert (snapshot.failures, snapshot.error.kind, snapshot.running) == (2, ErrorKind.CONNECTION, (running,))
    snapshot = tracker.refresh_active()
    assert (snapshot.failures, snapshot.error) == (0, None)


def test_refresh_full_splits_running_recent_and_totals():
    tracker, client, _ = make_tracker()
    today = client.add(make_entry(1, NOW - timedelta(hours=3), NOW - timedelta(hours=2)))
    yesterday = client.add(make_entry(2, NOW - timedelta(days=1, hours=3), NOW - timedelta(days=1, hours=1)))
    running = client.add(make_entry(3, NOW - timedelta(minutes=30)))
    snapshot = tracker.refresh_full()
    assert snapshot.running == (running,)
    assert snapshot.recent == (today, yesterday)
    assert snapshot.totals == Totals(today=3600, week=3 * 3600)


def test_totals_window_is_the_kimai_week_in_account_zone():
    tracker, client, _ = make_tracker()
    tracker.refresh_full()
    assert ("range", "2026-09-21T00:00:00", "2026-09-25T23:59:59") in client.calls


def test_totals_failure_does_not_fail_the_refresh():
    tracker, client, _ = make_tracker()
    client.fail["range"] = [ApiError(ErrorKind.SERVER, 500)]
    snapshot = tracker.refresh_full()
    assert (snapshot.totals, snapshot.error) == (None, None)


def test_timezone_mismatch_flag():
    assert make_tracker(FakeClient("UTC"))[0].refresh_active().timezone_mismatch is True
    assert make_tracker(FakeClient("Europe/Warsaw"))[0].refresh_active().timezone_mismatch is False
    assert make_tracker(FakeClient("Europe/Berlin"))[0].refresh_active().timezone_mismatch is False


def test_unknown_kimai_timezone_falls_back_and_flags_mismatch():
    tracker, _, _ = make_tracker(FakeClient("Mars/Olympus"))
    snapshot = tracker.refresh_full()
    assert snapshot.timezone_mismatch is True
    assert tracker.kimai_tz().utcoffset(NOW) == timedelta(hours=2)  # the system zone (Warsaw, CEST)


def test_kimai_locale_is_remembered_from_entries():
    tracker, client, saved = make_tracker()
    client.add(make_entry(1, NOW - timedelta(hours=3), NOW - timedelta(hours=2), language="pl"))
    tracker.refresh_full()
    assert tracker.memory.kimai_locale == "pl"
    assert saved[-1].kimai_locale == "pl"


def test_load_catalog_marks_non_billable_customers():
    tracker, client, _ = make_tracker()
    snapshot = tracker.load_catalog()
    assert [p.name for p in snapshot.projects] == ["Moduł rezerwacji", "Administracja"]
    assert snapshot.non_billable_customers == frozenset({20})
    client.fail["customers"] = [ApiError(ErrorKind.AUTH, 403)]
    assert tracker.load_catalog().non_billable_customers == frozenset()


def test_activities_are_sorted_and_default_billable():
    tracker, _, _ = make_tracker()
    tracker.load_catalog()
    activities = tracker.activities(1)
    assert [a.name for a in activities] == ["Programowanie", "Spotkanie"]
    assert tracker.default_billable(1, activities[0]) is True
    assert tracker.default_billable(2, activities[0]) is False  # customer 20 is not billable


def test_live_totals_add_running_time():
    running = make_entry(1, NOW - timedelta(minutes=10))
    snapshot = Snapshot(running=(running,), totals=Totals(today=60, week=120))
    assert live_totals(snapshot, NOW, WAW) == Totals(today=660, week=720)
    assert live_totals(Snapshot(), NOW, WAW) == Totals()


def test_live_totals_count_a_running_entry_on_the_day_it_began():
    # Like Kimai: an entry belongs to the day it started, so stopping it does not move hours.
    since_last_night = make_entry(1, datetime(2026, 9, 24, 22, 0, tzinfo=WAW))  # Thursday
    snapshot = Snapshot(running=(since_last_night,), totals=Totals(today=0, week=100))
    elapsed = int((NOW - since_last_night.begin).total_seconds())
    assert live_totals(snapshot, NOW, WAW) == Totals(today=0, week=100 + elapsed)


def test_live_totals_ignore_a_running_entry_from_last_week():
    since_sunday = make_entry(1, datetime(2026, 9, 20, 23, 0, tzinfo=WAW))
    assert live_totals(Snapshot(running=(since_sunday,)), NOW, WAW) == Totals()


def test_light_refresh_recomputes_totals_when_an_entry_stops_elsewhere():
    tracker, client, _ = make_tracker()
    client.add(make_entry(1, NOW - timedelta(hours=1)))
    assert tracker.refresh_full().totals == Totals()
    ranges = lambda: sum(1 for call in client.calls if call[0] == "range")  # noqa: E731
    tracker.refresh_active()
    assert ranges() == 1  # nothing changed: no extra query
    client.stop(1)  # stopped in the browser add-on or the Kimai panel
    snapshot = tracker.refresh_active()
    assert ranges() == 2
    assert snapshot.running == ()
    assert snapshot.totals == Totals(today=3600, week=3600)


def test_all_entries_url():
    assert all_entries_url("https://k.test/", "pl") == "https://k.test/pl/timesheet/"


def test_initial_snapshot_respects_billable_memory():
    tracker, _, _ = make_tracker(memory=Memory(billable_allowed=False))
    assert tracker.snapshot.billable_allowed is False
    assert tracker.snapshot.user is None


def test_refresh_survives_a_captive_portal_page():
    import httpx

    from kimai_tray.core.kimai_client import KimaiClient

    client = KimaiClient(
        "https://kimai.test", "t", transport=httpx.MockTransport(lambda r: httpx.Response(200, text="<html>"))
    )
    tracker = Tracker(client, Settings(url="https://kimai.test"), Memory(), now=lambda: NOW)
    snapshot = tracker.refresh_active()
    assert (snapshot.error.kind, snapshot.failures) == (ErrorKind.BAD_RESPONSE, 1)
    assert tracker.refresh_full().failures == 2


def test_missing_kimai_timezone_uses_system_zone_and_warns():
    tracker, _, _ = make_tracker(FakeClient(""))
    snapshot = tracker.refresh_full()
    assert (snapshot.timezone_missing, snapshot.timezone_mismatch) == (True, False)
    assert tracker.kimai_tz().utcoffset(NOW) == timedelta(hours=2)
    assert tracker.warnings() == [("warnTimezoneMissing", {"system": "CEST"})]


def test_warnings_for_zone_mismatch_and_for_none():
    utc_account, _, _ = make_tracker(FakeClient("UTC"))
    utc_account.refresh_active()
    assert utc_account.warnings() == [("warnTimezone", {"kimai": "UTC", "system": "CEST"})]
    same, _, _ = make_tracker(FakeClient("Europe/Warsaw"))
    assert same.warnings() == []  # nothing known yet
    same.refresh_active()
    assert same.warnings() == []


def test_week_totals_follow_the_kimai_first_weekday():
    from dataclasses import replace

    client = FakeClient()
    client.user = replace(client.user, first_weekday="sunday")
    tracker, _, _ = make_tracker(client)
    tracker.refresh_full()
    assert ("range", "2026-09-20T00:00:00", "2026-09-25T23:59:59") in client.calls
    since_sunday = make_entry(9, datetime(2026, 9, 20, 23, 0, tzinfo=WAW))
    snapshot = replace(tracker.snapshot, running=(since_sunday,), totals=Totals())
    assert live_totals(snapshot, NOW, WAW).week == int((NOW - since_sunday.begin).total_seconds())
