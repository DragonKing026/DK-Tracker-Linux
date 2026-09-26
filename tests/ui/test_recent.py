from dataclasses import replace
from datetime import UTC, datetime
from zoneinfo import ZoneInfo

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QLabel

from dk_tracker.core.i18n import Translator
from dk_tracker.core.tracker import Snapshot
from dk_tracker.ui.recent import RecentList

from ..core.fakes import NOW, make_entry

WARSAW = ZoneInfo("Europe/Warsaw")
TODAY_A = make_entry(5, datetime(2026, 9, 25, 13, 15, tzinfo=UTC), datetime(2026, 9, 25, 15, 5, tzinfo=UTC))
TODAY_B = make_entry(
    4,
    datetime(2026, 9, 25, 7, 0, tzinfo=UTC),
    datetime(2026, 9, 25, 8, 0, tzinfo=UTC),
    description="",
    billable=False,
)
YESTERDAY = make_entry(3, datetime(2026, 9, 24, 9, 0, tzinfo=UTC), datetime(2026, 9, 24, 9, 30, tzinfo=UTC))
SNAPSHOT = Snapshot(recent=(TODAY_A, TODAY_B, YESTERDAY))


def texts(widget, name):
    return [label.text() for label in widget.findChildren(QLabel, name)]


def make(qtbot, snapshot=SNAPSHOT, t=None):
    recent = RecentList()
    qtbot.addWidget(recent)
    recent.render(snapshot, WARSAW, NOW, t or Translator("pl"))
    return recent


def test_days_have_labels_and_sums(qtbot):
    recent = make(qtbot)
    assert texts(recent, "recentDayName") == ["DZIŚ", "WCZORAJ"]
    assert texts(recent, "recentDaySum") == ["2:50", "0:30"]


def test_rows_show_the_entry(qtbot):
    recent = make(qtbot)
    assert texts(recent, "entryDesc")[0] == "Formularz rezerwacji pokoi"
    assert texts(recent, "entryDescEmpty") == ["(bez opisu)"]
    assert texts(recent, "entryDuration") == ["1:50", "1:00", "0:30"]
    assert texts(recent, "entrySpan")[0] == "15:15-17:05"
    assert texts(recent, "entryMeta")[0] == "Moduł rezerwacji - Programowanie"


def test_resume_emits_the_entry(qtbot):
    recent = make(qtbot)
    with qtbot.waitSignal(recent.resumeRequested) as signal:
        recent.rows[0].resume.click()
    assert signal.args == [TODAY_A]


def test_billable_click_is_optimistic_until_the_next_render(qtbot):
    recent = make(qtbot)
    button = recent.rows[1].billable
    with qtbot.waitSignal(recent.billableRequested) as signal:
        button.click()
    assert signal.args == [4, True]
    assert not button.isEnabled()  # pending
    recent.render(SNAPSHOT, WARSAW, NOW, Translator("pl"))  # e.g. Kimai refused: back to the truth
    assert recent.rows[1].billable.isEnabled()
    assert recent.rows[1].billable.property("on") == "false"


def test_billable_is_locked_without_permission_or_after_export(qtbot):
    exported = replace(TODAY_A, exported=True)
    recent = make(qtbot, Snapshot(recent=(exported, TODAY_B)))
    assert not recent.rows[0].billable.isEnabled()
    assert recent.rows[1].billable.isEnabled()
    recent = make(qtbot, Snapshot(recent=(TODAY_A,), billable_allowed=False))
    assert not recent.rows[0].billable.isEnabled()


def test_empty_list(qtbot):
    recent = make(qtbot, Snapshot())
    assert not recent.empty.isHidden()
    assert recent.rows == []


def test_english(qtbot):
    recent = make(qtbot, t=Translator("en"))
    assert texts(recent, "recentDayName") == ["TODAY", "YESTERDAY"]
    assert recent.head.text() == "RECENT ENTRIES"


def test_dot_and_buttons_are_centred_in_the_row(qtbot):
    recent = make(qtbot)
    recent.resize(460, 400)
    recent.show()
    qtbot.waitExposed(recent)
    row = recent.rows[0]
    centre = row.height() / 2
    for widget in (row.marker, row.billable, row.resume):
        middle = widget.geometry().center().y()
        assert abs(middle - centre) <= 2, (widget.objectName(), middle, centre)


LONG = replace(TODAY_A, id=9, description="Trello: poprawić przepływ rejestracji pacjenta w aplikacji " * 6)


def description_of(row):
    return row.findChild(QLabel, "entryDesc")


def test_long_description_shows_two_and_a_half_lines_from_the_top(qtbot):
    recent = make(qtbot, Snapshot(recent=(LONG,)))
    label = description_of(recent.rows[0])
    assert label.alignment() & Qt.AlignmentFlag.AlignTop  # centred text was clipped at the top as well
    assert label.maximumHeight() == round(label.fontMetrics().lineSpacing() * 2.5)


def test_clicking_a_row_expands_and_collapses_its_description(qtbot):
    recent = make(qtbot, Snapshot(recent=(LONG,)))
    row = recent.rows[0]
    collapsed = description_of(row).maximumHeight()
    QTest.mouseClick(row, Qt.MouseButton.LeftButton)
    assert description_of(recent.rows[0]).maximumHeight() > collapsed * 4
    QTest.mouseClick(recent.rows[0], Qt.MouseButton.LeftButton)
    assert description_of(recent.rows[0]).maximumHeight() == collapsed


def test_an_expanded_row_stays_expanded_after_a_refresh(qtbot):
    recent = make(qtbot, Snapshot(recent=(LONG, YESTERDAY)))
    QTest.mouseClick(recent.rows[0], Qt.MouseButton.LeftButton)
    recent.render(Snapshot(recent=(LONG, YESTERDAY)), WARSAW, NOW, Translator("pl"))
    assert description_of(recent.rows[0]).maximumHeight() > description_of(recent.rows[1]).maximumHeight() * 4


# -- F-33: search in all entries ---------------------------------------------------


def ids(recent):
    return [row.entry.id for row in recent.rows]


def test_search_asks_for_the_term_after_a_pause(qtbot):
    recent = make(qtbot)
    with qtbot.waitSignal(recent.searchRequested, timeout=2000) as signal:
        QTest.keyClicks(recent.search, "rezerwacja")
    assert signal.args == ["rezerwacja"]


def test_one_character_does_not_search(qtbot):
    recent = make(qtbot)
    with qtbot.assertNotEmitted(recent.searchRequested, wait=700):
        QTest.keyClicks(recent.search, "r")


def test_results_replace_the_recent_list_until_the_field_is_cleared(qtbot):
    recent = make(qtbot)
    recent.search.setText("trello")
    recent.show_results("trello", (LONG,), WARSAW, NOW)
    assert ids(recent) == [9]
    assert texts(recent, "recentHead") == ["WYNIKI (1)"]
    recent.render(SNAPSHOT, WARSAW, NOW, Translator("pl"))  # the minute refresh keeps the results
    assert ids(recent) == [9]
    recent.search.clear()
    assert ids(recent) == [5, 4, 3]
    assert texts(recent, "recentHead") == ["OSTATNIE WPISY"]


def test_late_results_for_an_older_term_are_ignored(qtbot):
    recent = make(qtbot)
    recent.search.setText("trello nowe")
    recent.show_results("trello", (LONG,), WARSAW, NOW)
    assert ids(recent) == [5, 4, 3]


def test_no_results_says_so(qtbot):
    recent = make(qtbot)
    recent.search.setText("xyz")
    recent.show_results("xyz", (), WARSAW, NOW)
    assert ids(recent) == []
    assert recent.empty.isVisibleTo(recent)
    assert recent.empty.text() == "Żaden wpis nie ma tego tekstu w opisie."


def test_escape_clears_the_search_first(qtbot):
    recent = make(qtbot)
    recent.search.setText("trello")
    recent.show_results("trello", (LONG,), WARSAW, NOW)
    QTest.keyClick(recent.search, Qt.Key.Key_Escape)
    assert recent.search.text() == ""
    assert ids(recent) == [5, 4, 3]


def test_search_field_speaks_english(qtbot):
    recent = make(qtbot, t=Translator("en"))
    assert recent.search.placeholderText() == "Search all entries…"
