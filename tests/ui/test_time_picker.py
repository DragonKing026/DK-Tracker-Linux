import pytest

from dk_tracker.ui.time_picker import PLACEHOLDER, TimePicker


@pytest.fixture
def picker(qtbot):
    widget = TimePicker(clearable=True)
    qtbot.addWidget(widget)
    widget.show()
    return widget


def rows(column):
    return [column.item(row).text() for row in range(column.count())]


def test_empty_shows_the_placeholder(picker):
    assert picker.value == ""
    assert picker.text() == PLACEHOLDER


def test_hours_and_every_minute(picker):
    picker.open_list()
    assert rows(picker.popup.hours) == [f"{h:02d}" for h in range(24)]
    assert rows(picker.popup.minutes) == [f"{m:02d}" for m in range(60)]
    picker.popup.hide()


def test_any_minute_from_kimai_is_chosen_on_the_list(picker):
    picker.set_value("16:21")
    picker.open_list()
    assert "21" in rows(picker.popup.minutes)
    assert picker.popup.minutes.currentItem().text() == "21"
    assert picker.popup.hours.currentItem().text() == "16"
    picker.popup.hide()


def test_hour_keeps_the_list_open_minute_closes_it_and_reports_once(picker, qtbot):
    picker.set_value("09:40")
    picker.open_list()
    with qtbot.assertNotEmitted(picker.edited):
        picker.popup.hours.picked.emit(11)
    assert picker.popup.isVisible()
    assert picker.value == "11:40"
    with qtbot.waitSignal(picker.edited) as signal:
        picker.popup.minutes.picked.emit(15)
    assert not picker.popup.isVisible()
    assert signal.args == ["11:15"]


def test_closing_without_a_change_reports_nothing(picker, qtbot):
    picker.set_value("09:40")
    picker.open_list()
    with qtbot.assertNotEmitted(picker.edited):
        picker.popup.hide()


def test_set_value_from_outside_is_not_an_edit(picker, qtbot):
    with qtbot.assertNotEmitted(picker.edited):
        picker.set_value("12:00")
    assert picker.text() == "12:00"


def test_clearable_offers_now(picker, qtbot):
    picker.set_value("17:30")
    picker.open_list()
    assert picker.popup.clear_button.isVisible()
    with qtbot.waitSignal(picker.edited) as signal:
        picker.popup.clear_button.click()
    assert signal.args == [""]
    assert picker.text() == PLACEHOLDER


def test_not_clearable_hides_now(qtbot):
    picker = TimePicker()
    qtbot.addWidget(picker)
    picker.show()
    picker.set_value("08:00")
    picker.open_list()
    assert not picker.popup.clear_button.isVisible()
    picker.popup.hide()
