"""Plan 6: `app.summary` — the chosen period and breakdown, asking for entries, the data QML draws."""

from datetime import UTC, date, datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from dk_tracker.core.i18n import Translator
from dk_tracker.ui.main_window.summary_page import SummaryPage

from ...core.fakes import make_entry

WARSAW = ZoneInfo("Europe/Warsaw")
PL = Translator("pl")
NOW = datetime(2026, 9, 25, 16, 0, tzinfo=UTC)
TODAY = date(2026, 9, 25)


def entry(entry_id, day, hours, **extra):
    begin = datetime(day.year, day.month, day.day, 8, tzinfo=WARSAW).astimezone(UTC)
    return make_entry(entry_id, begin, begin + timedelta(hours=hours), **extra)


@pytest.fixture
def page(qapp):
    made = SummaryPage()
    made.configure(today=TODAY, first_weekday=0, t=PL)
    return made


def deliver(page, entries, norm=8 * 3600):
    first, last = page.span.first, page.span.last
    page.set_entries(first, last, entries, tz=WARSAW, now=NOW, norm=norm)


def test_it_starts_on_this_week_and_asks_for_it(page, qtbot):
    assert (page.span.kind, page.span.first, page.span.last) == ("week", date(2026, 9, 21), date(2026, 9, 27))
    with qtbot.waitSignal(page.loadRequested) as asked:
        page.request()
    assert asked.args == [date(2026, 9, 21), date(2026, 9, 27)]
    assert page.data["loading"] is True
    assert page.data["label"] == "21 – 27 wrz 2026"
    assert page.data["loaded"] is False


def test_entries_fill_the_data(page):
    page.request()
    deliver(page, [entry(1, date(2026, 9, 21), 6)])
    data = page.data
    assert (data["loaded"], data["loading"], data["total"], data["kind"], data["group"]) == (
        True, False, "6:00", "week", "project",
    )  # fmt: skip
    assert len(data["bars"]) == 7


def test_the_arrows_and_the_kind_ask_for_the_new_period(page, qtbot):
    with qtbot.waitSignal(page.loadRequested) as asked:
        page.step(-1)
    assert asked.args == [date(2026, 9, 14), date(2026, 9, 20)]
    assert page.data["isToday"] is False
    with qtbot.waitSignal(page.loadRequested) as asked:
        page.setPeriod("month")
    assert asked.args == [
        date(2026, 9, 1),
        date(2026, 9, 30),
    ]  # the month of the day shown, not of the week before
    with qtbot.waitSignal(page.loadRequested) as asked:
        page.today()
    assert asked.args == [date(2026, 9, 1), date(2026, 9, 30)]
    assert page.data["isToday"] is True


def test_a_range_from_two_days(page, qtbot):
    with qtbot.waitSignal(page.loadRequested) as asked:
        page.setRange("2026-09-10", "2026-09-01")
    assert asked.args == [date(2026, 9, 1), date(2026, 9, 10)]
    assert (page.data["kind"], page.data["first"], page.data["last"]) == ("range", "2026-09-01", "2026-09-10")


def test_a_half_typed_day_is_ignored(page, qtbot):
    with qtbot.assertNotEmitted(page.loadRequested):
        page.setRange("2026-13-01", "2026-09-01")


def test_choosing_range_starts_from_the_period_shown(page, qtbot):
    page.setPeriod("month")
    with qtbot.waitSignal(page.loadRequested) as asked:
        page.setPeriod("range")
    assert asked.args == [date(2026, 9, 1), date(2026, 9, 30)]


def test_an_answer_for_an_older_period_is_dropped(page):
    page.request()
    old_first, old_last = page.span.first, page.span.last
    page.step(-1)
    page.set_entries(old_first, old_last, [entry(1, date(2026, 9, 21), 6)], tz=WARSAW, now=NOW, norm=0)
    assert page.data["loaded"] is False
    assert page.data["loading"] is True


def test_the_breakdown_changes_without_asking_kimai(page, qtbot):
    page.request()
    deliver(page, [entry(1, date(2026, 9, 21), 6)])
    with qtbot.assertNotEmitted(page.loadRequested):
        page.setGroup("activity")
    assert page.data["group"] == "activity"
    assert page.data["shares"][0]["name"] == "Programowanie"
    page.setGroup("nonsense")
    assert page.data["group"] == "activity"


def test_the_numbers_stay_while_the_next_period_loads(page):
    page.request()
    deliver(page, [entry(1, date(2026, 9, 21), 6)])
    page.request()  # the minute's refresh
    assert (page.data["loading"], page.data["loaded"], page.data["total"]) == (True, True, "6:00")


def test_a_failed_load_stops_the_loading(page):
    page.request()
    page.set_loading(False)
    assert page.data["loading"] is False


def test_the_language_changes_the_texts(page):
    page.request()
    deliver(page, [entry(1, date(2026, 9, 21), 6)])
    page.retranslate(Translator("en"))
    assert page.data["label"] == "21 – 27 Sep 2026"
    assert page.data["daysWith"] == "Days with entries: 1"


def test_a_new_week_moves_this_week_along_until_the_user_picks_a_period(page, qtbot):
    page.configure(today=date(2026, 9, 28), first_weekday=0, t=PL)
    assert page.span.first == date(2026, 9, 28)  # left open over the weekend: the new week
    page.step(-1)
    page.configure(today=date(2026, 10, 5), first_weekday=0, t=PL)
    assert page.span.first == date(2026, 9, 21)  # a period the user picked does not jump
    with qtbot.waitSignal(page.loadRequested) as asked:
        page.today()
    assert asked.args == [date(2026, 10, 5), date(2026, 10, 11)]
