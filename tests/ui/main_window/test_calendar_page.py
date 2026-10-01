"""Plan 7: `app.calendarPage` — the days shown, the blocks QML draws, new and moved entries."""

from dataclasses import replace
from datetime import UTC, date, datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from dk_tracker.core.i18n import Translator
from dk_tracker.ui.main_window.calendar_page import CalendarPage

from ...core.fakes import make_entry

WARSAW = ZoneInfo("Europe/Warsaw")
PL = Translator("pl")
NOW = datetime(2026, 9, 25, 16, 0, tzinfo=UTC)  # Friday 18:00 in Warsaw
TODAY = date(2026, 9, 25)


def entry(entry_id, day, hour, minutes, **extra):
    begin = datetime(day.year, day.month, day.day, hour, tzinfo=WARSAW).astimezone(UTC)
    return replace(make_entry(entry_id, begin, begin + timedelta(minutes=minutes)), **extra)


@pytest.fixture
def page(qapp):
    made = CalendarPage()
    made.configure(today=TODAY, first_weekday=0, t=PL, now=NOW, tz=WARSAW)
    return made


def deliver(page, entries):
    first, last = page.days[0], page.days[-1]
    page.set_entries(first, last, entries, tz=WARSAW, now=NOW)


def test_it_starts_on_this_week_of_seven_days_and_asks_for_it(page, qtbot):
    with qtbot.waitSignal(page.loadRequested) as asked:
        page.request()
    assert asked.args == [date(2026, 9, 21), date(2026, 9, 27)]
    data = page.data
    assert (data["mode"], data["workweek"], data["label"], data["loading"]) == (
        "week",
        False,
        "21 – 27 wrz 2026",
        True,
    )
    assert [day["label"] for day in data["days"]][:2] == ["pon. 21", "wt. 22"]
    assert data["days"][4]["today"] is True
    assert data["now"] == 18 * 60


def test_blocks_carry_what_a_block_shows(page):
    page.request()
    deliver(page, [entry(1, date(2026, 9, 22), 9, 90, description="Formularz rezerwacji")])
    [block] = page.data["blocks"]
    assert (block["id"], block["day"], block["start"], block["end"]) == (1, 1, 540, 630)
    assert (block["description"], block["project"], block["color"], block["hours"], block["time"]) == (
        "Formularz rezerwacji", "Moduł rezerwacji · Programowanie", "#008000", "09:00 – 10:30", "1:30",
    )  # fmt: skip
    assert (block["running"], block["exported"], block["movable"]) == (False, False, True)
    assert page.data["days"][1]["total"] == "1:30"
    assert page.data["loaded"] is True


def test_five_days_and_one_day(page, qtbot):
    page.setWorkweek(True)
    assert [day["date"] for day in page.data["days"]] == [f"2026-09-{d}" for d in range(21, 26)]
    with qtbot.waitSignal(page.loadRequested) as asked:
        page.setMode("day")
    assert asked.args == [TODAY, TODAY]
    page.step(-1)
    assert page.data["days"][0]["date"] == "2026-09-24"


def test_an_answer_for_other_days_is_dropped(page):
    page.request()
    page.step(1)
    page.set_entries(
        date(2026, 9, 21), date(2026, 9, 27), [entry(1, date(2026, 9, 22), 9, 60)], tz=WARSAW, now=NOW
    )
    assert page.data["blocks"] == []


def test_a_new_entry_from_a_dragged_span(page, qtbot):
    with qtbot.waitSignal(page.addRequested) as asked:
        page.create(2, 540, 1440, "Formularz rezerwacji", 1, 2, True)
    assert asked.args[0] == {
        "day": date(2026, 9, 23), "begin": "09:00", "end": "24:00", "description": "Formularz rezerwacji",
        "project_id": 1, "activity_id": 2, "billable": True,
    }  # fmt: skip


def test_a_moved_block_stands_in_its_new_place_at_once(page, qtbot):
    page.request()
    deliver(page, [entry(1, date(2026, 9, 22), 9, 60)])
    with qtbot.waitSignal(page.moveRequested) as asked:
        page.move(1, 3, 600, 690)
    assert asked.args == [1, date(2026, 9, 24), 600, 690]
    [block] = page.data["blocks"]
    assert (block["day"], block["start"], block["end"]) == (3, 600, 690)


def test_a_block_keeps_its_seconds_and_a_dragged_edge_leaves_the_other_ones(page, qtbot):
    page.request()
    begin = datetime(2026, 9, 22, 9, 0, 40, tzinfo=WARSAW).astimezone(UTC)
    deliver(page, [make_entry(1, begin, begin + timedelta(minutes=30, seconds=5))])
    [block] = page.data["blocks"]
    assert (block["start"], block["end"]) == pytest.approx((540 + 40 / 60, 570 + 45 / 60))
    assert (block["hours"], block["time"]) == ("09:00 – 09:30", "0:30")
    with qtbot.waitSignal(page.moveRequested) as asked:
        page.move(1, 1, block["start"], 600)  # only the end dragged, to 10:00
    assert asked.args == [1, date(2026, 9, 22), 540, 600]
    moved = page.entry(1)
    assert (moved.begin, moved.duration) == (begin, 59 * 60 + 20)  # 9:00:40 stays


def test_running_exported_and_past_midnight_blocks_do_not_move(page, qtbot):
    page.request()
    running = make_entry(2, NOW - timedelta(hours=1))
    deliver(page, [entry(1, TODAY, 9, 60, exported=True), running, entry(3, date(2026, 9, 21), 23, 120)])
    movable = {(block["id"], block["day"]): block["movable"] for block in page.data["blocks"]}
    assert movable == {(1, 4): False, (2, 4): False, (3, 0): False, (3, 1): False}
    with qtbot.assertNotEmitted(page.moveRequested):
        page.move(1, 4, 600, 660)


def test_a_refresh_waits_while_a_block_is_dragged(page):
    page.request()
    deliver(page, [entry(1, date(2026, 9, 22), 9, 60)])
    page.setDragging(True)
    deliver(page, [entry(1, date(2026, 9, 22), 9, 60), entry(2, date(2026, 9, 22), 12, 60)])
    assert len(page.data["blocks"]) == 1
    page.setDragging(False)
    assert len(page.data["blocks"]) == 2


def test_a_deleted_block_hides_until_undone(page):
    page.request()
    deliver(page, [entry(1, date(2026, 9, 22), 9, 60)])
    assert page.entry(1).id == 1
    page.hide_entry(1)
    assert page.data["blocks"] == []
    page.show_entry(1)
    assert len(page.data["blocks"]) == 1


def test_the_now_line_moves_each_minute_and_only_then(page, qtbot):
    page.request()
    deliver(page, [])
    with qtbot.assertNotEmitted(page.dataChanged):
        page.tick(NOW + timedelta(seconds=30))
    with qtbot.waitSignal(page.dataChanged):
        page.tick(NOW + timedelta(minutes=1))
    assert page.data["now"] == 18 * 60 + 1
