"""Plan 6: the summaries — periods, averages, the norm, the bars and the breakdown (spec 0.10, section 6)."""

from dataclasses import replace
from datetime import UTC, date, datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from dk_tracker.core.i18n import Translator
from dk_tracker.core.summary import (
    MAX_RANGE_DAYS,
    Span,
    nice_scale,
    present,
    range_span,
    shifted,
    span_for,
    span_label,
    summarize,
)

from .fakes import make_entry

WARSAW = ZoneInfo("Europe/Warsaw")
PL = Translator("pl")
EN = Translator("en")
NOW = datetime(2026, 9, 25, 16, 0, tzinfo=UTC)  # Friday 18:00 in Warsaw
HOUR = 3600
NORM = 8 * HOUR
MONDAY, SUNDAY = 0, 6


def entry(entry_id, day, hour, hours, *, project=1, customer=10, activity=1, billable=True, running=False):
    begin = datetime(day.year, day.month, day.day, hour, tzinfo=WARSAW).astimezone(UTC)
    end = None if running else begin + timedelta(hours=hours)
    names = {1: "Moduł rezerwacji", 2: "Administracja", 3: "Strona"}
    return replace(
        make_entry(entry_id, begin, end, billable=billable, project_id=project, activity_id=activity),
        project_name=names[project],
        project_color={1: "#008000", 2: "#808080", 3: "#0000ff"}[project],
        activity_name={1: "Programowanie", 2: "Spotkanie"}[activity],
        activity_color={1: "#111111", 2: "#222222"}[activity],
        customer_id=customer,
        customer_name={10: "Hotel Morski", 20: "Sprawy wewnętrzne"}[customer],
        customer_color={10: "#aa0000", 20: "#00aa00"}[customer],
    )


def week(day=date(2026, 9, 25)):
    return span_for("week", day, MONDAY)


# -- periods ---------------------------------------------------------------------------


def test_a_week_starts_on_the_accounts_first_weekday():
    assert span_for("week", date(2026, 9, 25), MONDAY) == Span("week", date(2026, 9, 21), date(2026, 9, 27))
    assert span_for("week", date(2026, 9, 25), SUNDAY) == Span("week", date(2026, 9, 20), date(2026, 9, 26))


def test_a_month_and_a_year_are_the_calendar_ones():
    assert span_for("month", date(2026, 2, 14), MONDAY) == Span("month", date(2026, 2, 1), date(2026, 2, 28))
    assert span_for("year", date(2026, 2, 14), MONDAY) == Span("year", date(2026, 1, 1), date(2026, 12, 31))


def test_the_arrows_move_by_one_period():
    assert shifted(week(), -1, MONDAY) == Span("week", date(2026, 9, 14), date(2026, 9, 20))
    month = span_for("month", date(2026, 1, 31), MONDAY)
    assert shifted(month, -1, MONDAY) == Span("month", date(2025, 12, 1), date(2025, 12, 31))
    assert shifted(month, 1, MONDAY) == Span("month", date(2026, 2, 1), date(2026, 2, 28))
    assert shifted(span_for("year", date(2026, 5, 1), MONDAY), 1, MONDAY).first == date(2027, 1, 1)


def test_a_range_moves_by_its_own_length():
    ten_days = range_span(date(2026, 9, 1), date(2026, 9, 10))
    assert shifted(ten_days, 1, MONDAY) == Span("range", date(2026, 9, 11), date(2026, 9, 20))


def test_a_range_typed_backwards_is_turned_round_and_capped_at_a_year():
    assert range_span(date(2026, 9, 10), date(2026, 9, 1)) == Span(
        "range", date(2026, 9, 1), date(2026, 9, 10)
    )
    long = range_span(date(2024, 1, 1), date(2026, 1, 1))
    assert long.days == MAX_RANGE_DAYS
    assert long.first == date(2024, 1, 1)


def test_period_labels():
    today = date(2026, 9, 25)
    assert span_label(week(), today, PL) == "21 – 27 wrz 2026"
    assert span_label(week(date(2026, 10, 1)), today, PL) == "28 wrz – 4 paź 2026"
    assert span_label(week(date(2026, 1, 1)), today, PL) == "29 gru 2025 – 4 sty 2026"
    assert span_label(span_for("month", today, MONDAY), today, PL) == "wrzesień 2026"
    assert span_label(span_for("month", today, MONDAY), today, EN) == "September 2026"
    assert span_label(span_for("year", today, MONDAY), today, PL) == "2026"


# -- numbers ---------------------------------------------------------------------------


def test_totals_billable_and_days_with_entries():
    entries = [
        entry(1, date(2026, 9, 21), 8, 6),
        entry(2, date(2026, 9, 21), 15, 2, billable=False),
        entry(3, date(2026, 9, 23), 8, 7),
    ]
    summary = summarize(entries, week(), WARSAW, now=NOW, norm=NORM, first_weekday=MONDAY)
    assert summary.total == 15 * HOUR
    assert summary.billable == 13 * HOUR
    assert (summary.days_with, summary.work_days) == (2, 5)
    assert summary.avg_day == 3 * HOUR  # ÷ working days until today (Monday–Friday), not ÷ days with entries


def test_the_running_entry_counts_until_now_on_the_day_it_began():
    running = entry(1, date(2026, 9, 25), 16, 0, running=True)  # 16:00 → 18:00 Warsaw now
    summary = summarize([running], week(), WARSAW, now=NOW, norm=NORM, first_weekday=MONDAY)
    assert summary.total == 2 * HOUR
    assert summary.buckets[4].seconds == 2 * HOUR


def test_an_entry_past_midnight_counts_on_the_day_it_began():
    late = entry(1, date(2026, 9, 21), 22, 4)
    summary = summarize([late], week(), WARSAW, now=NOW, norm=NORM, first_weekday=MONDAY)
    assert [bucket.seconds for bucket in summary.buckets][:2] == [4 * HOUR, 0]


def test_entries_outside_the_period_are_left_out():
    outside = entry(1, date(2026, 9, 20), 10, 1)
    summary = summarize([outside], week(), WARSAW, now=NOW, norm=NORM, first_weekday=MONDAY)
    assert summary.total == 0


def test_the_average_is_per_working_day_so_a_saturday_catches_up():
    """Live test of 0.10.3: one average — hours ÷ working days (Monday–Friday). Work on a Saturday
    raises it; counting days with entries would have lowered it."""
    last_week = shifted(week(), -1, MONDAY)  # 14–20 September, all past
    entries = [entry(i, date(2026, 9, 14 + i), 8, 7) for i in range(5)] + [entry(9, date(2026, 9, 19), 8, 5)]
    summary = summarize(entries, last_week, WARSAW, now=NOW, norm=NORM, first_weekday=MONDAY)
    assert summary.work_days == 5
    assert summary.avg_day == 8 * HOUR  # 40 h ÷ 5, not ÷ 6 days with entries


def test_working_days_of_the_current_period_count_until_today():
    summary = summarize([entry(1, date(2026, 9, 1), 8, 19)], span_for("month", date(2026, 9, 1), 0), WARSAW,
                        now=NOW, norm=NORM, first_weekday=0)  # fmt: skip
    assert summary.work_days == 19  # 1–25 September, today included; the rest of the month is to come
    future = summarize([], shifted(week(), 1, MONDAY), WARSAW, now=NOW, norm=NORM, first_weekday=MONDAY)
    assert (future.work_days, future.avg_day) == (0, 0)


def test_a_weekend_only_period_averages_by_its_days_with_entries():
    weekend = range_span(date(2026, 9, 19), date(2026, 9, 20))
    summary = summarize(
        [entry(1, date(2026, 9, 19), 8, 4)], weekend, WARSAW, now=NOW, norm=NORM, first_weekday=0
    )
    assert (summary.work_days, summary.avg_day) == (0, 4 * HOUR)


# -- bars ------------------------------------------------------------------------------


def test_a_week_has_a_bar_a_day_split_by_project():
    entries = [
        entry(1, date(2026, 9, 21), 8, 2, project=1),
        entry(2, date(2026, 9, 21), 11, 1, project=2),
        entry(3, date(2026, 9, 22), 8, 3, project=2),
    ]
    summary = summarize(entries, week(), WARSAW, now=NOW, norm=NORM, first_weekday=MONDAY)
    assert summary.unit == "day"
    assert len(summary.buckets) == 7
    monday = summary.buckets[0]
    assert monday.seconds == 3 * HOUR
    # The same stacking order in every bar: the biggest project of the period at the bottom.
    assert [(part.key, part.seconds) for part in monday.parts] == [("p2", HOUR), ("p1", 2 * HOUR)]
    view = present(summary, PL, group="project", today=date(2026, 9, 25))
    assert [(part["seconds"], part["below"]) for part in view["bars"][0]["parts"]] == [
        (HOUR, 0),
        (2 * HOUR, HOUR),
    ]
    assert all(bucket.norm == NORM for bucket in summary.buckets)


def test_a_year_has_a_bar_a_month_with_the_norm_times_its_working_days():
    entries = [
        entry(1, date(2026, 3, 2), 8, 8),
        entry(2, date(2026, 3, 3), 8, 6),
        entry(3, date(2026, 5, 4), 8, 1),
    ]
    summary = summarize(
        entries, span_for("year", date(2026, 1, 1), 0), WARSAW, now=NOW, norm=NORM, first_weekday=0
    )
    assert summary.unit == "month"
    assert len(summary.buckets) == 12
    march = summary.buckets[2]
    assert (march.seconds, march.days_with, march.norm) == (14 * HOUR, 2, 22 * NORM)
    assert summary.buckets[0].norm == 22 * NORM  # January, no entries: still 22 working days
    assert summary.buckets[9].norm == 0  # October is still to come


def test_a_long_range_has_monthly_bars_a_short_one_daily():
    short = range_span(date(2026, 8, 1), date(2026, 9, 30))  # 61 days
    long = range_span(date(2026, 7, 15), date(2026, 9, 30))
    assert summarize([], short, WARSAW, now=NOW, norm=NORM, first_weekday=0).unit == "day"
    months = summarize([], long, WARSAW, now=NOW, norm=NORM, first_weekday=0)
    assert months.unit == "month"
    assert [(b.first, b.last) for b in months.buckets][0] == (date(2026, 7, 15), date(2026, 7, 31))


# -- breakdown -------------------------------------------------------------------------


def test_the_breakdown_by_project_customer_and_activity():
    entries = [
        entry(1, date(2026, 9, 21), 8, 3, project=1, customer=10, activity=1),
        entry(2, date(2026, 9, 21), 12, 1, project=2, customer=20, activity=2, billable=False),
        entry(3, date(2026, 9, 22), 8, 2, project=3, customer=10, activity=2),
    ]
    summary = summarize(entries, week(), WARSAW, now=NOW, norm=NORM, first_weekday=MONDAY)
    projects = summary.shares["project"]
    assert [(s.name, s.detail, s.color, s.seconds) for s in projects] == [
        ("Moduł rezerwacji", "Hotel Morski", "#008000", 3 * HOUR),
        ("Strona", "Hotel Morski", "#0000ff", 2 * HOUR),
        ("Administracja", "Sprawy wewnętrzne", "#808080", HOUR),
    ]
    customers = summary.shares["customer"]
    assert [(s.name, s.color, s.seconds, s.billable) for s in customers] == [
        ("Hotel Morski", "#aa0000", 5 * HOUR, 5 * HOUR),
        ("Sprawy wewnętrzne", "#00aa00", HOUR, 0),
    ]
    assert [(s.name, s.seconds) for s in summary.shares["activity"]] == [  # a tie: alphabetical
        ("Programowanie", 3 * HOUR),
        ("Spotkanie", 3 * HOUR),
    ]


# -- the axis --------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("highest", "top", "step"),
    [
        (0, HOUR, HOUR),
        (20 * 60, 30 * 60, 15 * 60),
        (7.5 * HOUR, 8 * HOUR, 2 * HOUR),
        (9 * HOUR, 9 * HOUR, 3 * HOUR),
        (170 * HOUR, 200 * HOUR, 50 * HOUR),
    ],
)
def test_the_axis_has_round_steps_and_at_most_four_of_them(highest, top, step):
    assert nice_scale(highest) == (top, step)


# -- texts for the view ---------------------------------------------------------------


def test_present_gives_the_view_its_texts():
    entries = [
        entry(1, date(2026, 9, 21), 8, 6),
        entry(2, date(2026, 9, 21), 15, 2, billable=False),
        entry(3, date(2026, 9, 23), 8, 7, project=2, customer=20),
    ]
    summary = summarize(entries, week(), WARSAW, now=NOW, norm=NORM, first_weekday=MONDAY)
    view = present(summary, PL, group="project", today=date(2026, 9, 25))
    assert view["empty"] is False
    assert (view["total"], view["daysWith"]) == ("15:00", "Dni robocze: 5 · z wpisami: 2")
    assert (view["paid"], view["paidPercent"]) == ("13:00", "87 %")
    assert (view["unpaid"], view["unpaidPercent"]) == ("2:00", "13 %")
    assert (view["avgDay"], view["norm"], view["normDiff"]) == ("3:00", "8:00", "−5:00")
    assert "avgWeek" not in view
    assert view["normLine"] == NORM
    bars = view["bars"]
    assert [bar["label"] for bar in bars] == [
        "pon. 21",
        "wt. 22",
        "śr. 23",
        "czw. 24",
        "pt. 25",
        "sob. 26",
        "niedz. 27",
    ]
    assert bars[4]["today"] is True
    assert bars[0]["title"] == "pon., 21 wrz"
    assert bars[0]["total"] == "8:00"
    assert [(part["name"], part["time"], part["color"]) for part in bars[0]["parts"]] == [
        ("Moduł rezerwacji", "8:00", "#008000")
    ]
    assert view["scaleTop"] == 8 * HOUR
    assert [tick["label"] for tick in view["ticks"]] == ["0:00", "2:00", "4:00", "6:00", "8:00"]
    first = view["shares"][0]
    assert (first["name"], first["detail"], first["time"], first["percent"], first["paid"]) == (
        "Moduł rezerwacji", "Hotel Morski", "8:00", "53 %", "6:00",
    )  # fmt: skip


def test_present_without_a_norm_hides_it():
    summary = summarize([entry(1, date(2026, 9, 21), 8, 6)], week(), WARSAW, now=NOW, norm=0, first_weekday=0)
    view = present(summary, EN, group="project", today=date(2026, 9, 25))
    assert (view["norm"], view["normDiff"], view["normLine"]) == ("", "", 0)
    assert view["paidPercent"] == "100%"


def test_present_an_empty_period():
    summary = summarize([], week(), WARSAW, now=NOW, norm=NORM, first_weekday=MONDAY)
    view = present(summary, PL, group="customer", today=date(2026, 9, 25))
    assert view["empty"] is True
    assert (view["total"], view["avgDay"], view["paidPercent"]) == ("0:00", "0:00", "0 %")
    assert view["shares"] == []
    assert view["slices"] == []


def test_the_ring_keeps_eight_slices_and_puts_the_rest_together():
    entries = [
        replace(
            entry(i, date(2026, 9, 21), 8, 1), project_id=i, project_name=f"P{i}", project_color="#123456"
        )
        for i in range(1, 11)
    ]
    summary = summarize(entries, week(), WARSAW, now=NOW, norm=NORM, first_weekday=MONDAY)
    view = present(summary, PL, group="project", today=date(2026, 9, 25))
    assert len(view["shares"]) == 10  # the table has them all
    slices = view["slices"]
    assert len(slices) == 9
    assert slices[-1]["name"] == "Pozostałe"
    assert slices[-1]["fraction"] == pytest.approx(0.2)
    assert sum(item["fraction"] for item in slices) == pytest.approx(1.0)


def test_month_bars_are_labelled_with_the_day_and_a_year_with_months():
    month = summarize([], span_for("month", date(2026, 9, 1), 0), WARSAW, now=NOW, norm=NORM, first_weekday=0)
    labels = [bar["label"] for bar in present(month, PL, group="project", today=date(2026, 9, 25))["bars"]]
    assert labels[:3] == ["1", "2", "3"]
    assert len(labels) == 30
    year = summarize([], span_for("year", date(2026, 9, 1), 0), WARSAW, now=NOW, norm=NORM, first_weekday=0)
    bars = present(year, PL, group="project", today=date(2026, 9, 25))["bars"]
    assert [bar["label"] for bar in bars][:2] == ["sty", "lut"]
    assert bars[8]["title"] == "wrzesień 2026"
    assert bars[8]["today"] is True


def test_many_daily_bars_are_labelled_once_a_week():
    span = range_span(date(2026, 8, 1), date(2026, 9, 30))
    bars = present(summarize([], span, WARSAW, now=NOW, norm=NORM, first_weekday=0), PL, group="project",
                   today=date(2026, 9, 25))["bars"]  # fmt: skip
    shown = [bar["label"] for bar in bars if bar["label"]]
    assert len(shown) == 9


def test_present_gives_ready_sentences_and_where_each_slice_starts():
    entries = [entry(1, date(2026, 9, 1), 8, 6), entry(2, date(2026, 9, 21), 8, 2, billable=False, project=2)]
    month = span_for("month", date(2026, 9, 1), MONDAY)
    summary = summarize(entries, month, WARSAW, now=NOW, norm=NORM, first_weekday=0)
    view = present(summary, PL, group="project", today=date(2026, 9, 25))
    assert view["unpaidLine"] == "Niepłatne 2:00 · 25 %"
    assert view["normText"] == "Norma 8:00 · −7:34"  # 8 h ÷ 19 working days
    assert [round(item["start"], 2) for item in view["slices"]] == [0.0, 0.75]
    assert view["bars"][0]["normText"] == "Norma 8:00"
    year = present(summarize(entries, span_for("year", date(2026, 9, 1), 0), WARSAW, now=NOW, norm=0,
                             first_weekday=0), PL, group="project", today=date(2026, 9, 25))  # fmt: skip
    assert (year["normText"], year["bars"][8]["normText"]) == ("", "")


# -- what a slice or a table row holds (live test of 0.10.3: as in Toggl) --------------------


def test_each_share_lists_its_entries_by_description_biggest_first():
    entries = [
        replace(entry(1, date(2026, 9, 21), 8, 1), description="Formularz  rezerwacji"),
        replace(
            entry(2, date(2026, 9, 22), 8, 2), description="Formularz rezerwacji"
        ),  # the same, spaced alike
        replace(entry(3, date(2026, 9, 22), 11, 2), description="Kalendarz dostępności"),
        replace(entry(4, date(2026, 9, 23), 8, 1), description=""),
        replace(entry(5, date(2026, 9, 23), 10, 1, project=2), description="Spotkanie zespołu"),
    ]
    summary = summarize(entries, week(), WARSAW, now=NOW, norm=NORM, first_weekday=MONDAY)
    first = summary.shares["project"][0]
    assert first.items == (
        ("Formularz rezerwacji", 3 * HOUR),
        ("Kalendarz dostępności", 2 * HOUR),
        ("", HOUR),
    )
    view = present(summary, PL, group="project", today=date(2026, 9, 25))
    assert view["shares"][0]["entries"] == [
        {"text": "Formularz rezerwacji", "time": "3:00"},
        {"text": "Kalendarz dostępności", "time": "2:00"},
        {"text": "(bez opisu)", "time": "1:00"},
    ]
    assert view["shares"][0]["more"] == ""
    assert view["slices"][0]["index"] == 0  # a slice points at its row of the table


def test_a_long_list_of_entries_is_cut_with_how_many_more():
    entries = [
        replace(entry(i, date(2026, 9, 21), 8, 0.5), description=f"Zadanie numer {i}") for i in range(1, 15)
    ]
    summary = summarize(entries, week(), WARSAW, now=NOW, norm=NORM, first_weekday=MONDAY)
    share = present(summary, PL, group="project", today=date(2026, 9, 25))["shares"][0]
    assert len(share["entries"]) == 10
    assert share["more"] == "+ 4 więcej"


def test_the_others_slice_lists_the_shares_it_holds():
    entries = [
        replace(
            entry(i, date(2026, 9, 21), 8, 11 - i),
            project_id=i,
            project_name=f"P{i}",
            project_color="#123456",
        )
        for i in range(1, 11)
    ]
    summary = summarize(entries, week(), WARSAW, now=NOW, norm=NORM, first_weekday=MONDAY)
    others = present(summary, PL, group="project", today=date(2026, 9, 25))["slices"][-1]
    assert others["index"] == -1
    assert others["entries"] == [{"text": "P9", "time": "2:00"}, {"text": "P10", "time": "1:00"}]
    assert (others["time"], others["percent"]) == ("3:00", "5 %")
