from dataclasses import replace
from datetime import UTC, datetime
from zoneinfo import ZoneInfo

from PySide6.QtWidgets import QLabel

from ws_tracker_tray.core.i18n import Translator
from ws_tracker_tray.core.tracker import Snapshot
from ws_tracker_tray.ui.recent import RecentList

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
