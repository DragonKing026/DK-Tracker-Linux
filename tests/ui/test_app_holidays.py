"""Task 0088: the controller and the public holidays — fetching on a saved country and on ↻, keeping the
data on a failure, "none" deleting it, the pages told, the status under the field. No network."""

from datetime import date

import httpx
import pytest

from dk_tracker.core.holidays import Holiday, HolidayData, HolidayService, save_holidays
from dk_tracker.core.settings import Settings

from .test_app import URL, harness  # noqa: F401 - the fixture

DAY = date(2026, 11, 11)


class Nager:
    """A fake date.nager.at: every year has Independence Day, until `fail` is set."""

    def __init__(self):
        self.requests: list[str] = []
        self.fail: httpx.Response | None = None

    def __call__(self, request):
        self.requests.append(request.url.path)
        if self.fail is not None:
            return self.fail
        year, country = request.url.path.split("/")[-2:]
        name = {"PL": ("Narodowe Święto Niepodległości", "Independence Day")}.get(country, ("Święto", "Day"))
        return httpx.Response(
            200,
            json=[
                {
                    "date": f"{year}-11-11",
                    "localName": name[0],
                    "name": name[1],
                    "global": True,
                    "types": ["Public"],
                }  # fmt: skip
            ],
        )


@pytest.fixture
def nager():
    return Nager()


@pytest.fixture
def made(harness, nager, tmp_path):  # noqa: F811
    path = tmp_path / "holidays.json"

    def make(country="", saved=None):
        if saved is not None:
            save_holidays(saved, path)
        service = HolidayService(path, transport=httpx.MockTransport(nager))
        return harness(settings=Settings(url=URL, language="pl", holiday_country=country), holidays=service)

    make.path = path
    return make


def saved_form(h, country, token=None):
    h.controller.save_settings(Settings(url=URL, language="pl", holiday_country=country), token)
    h.settle()


def status(h):
    return h.controller.settings_form.form["holidayStatus"]


def calendar_names(h):
    return [day["holiday"] for day in h.controller.main_bridge.calendar.data["days"]]


def test_without_a_country_nothing_is_fetched_and_the_start_is_as_before(made, nager):
    h = made()
    assert nager.requests == [] and status(h) == ""
    assert h.controller.main_bridge.summary._holidays == HolidayData()


def test_a_saved_country_is_fetched_once_for_three_years_and_kept(made, nager):
    h = made()
    saved_form(h, "PL")
    assert nager.requests == [f"/api/v3/PublicHolidays/{y}/PL" for y in (2025, 2026, 2027)]
    kept = made.path.read_text(encoding="utf-8")
    assert '"country": "PL"' in kept and "Narodowe Święto Niepodległości" in kept
    assert (
        status(h).startswith("Zsynchronizowano 20")
        and h.controller.settings_form.form["holidayBusy"] is False
    )
    assert h.controller._holidays.names("pl", "PL")[DAY] == "Narodowe Święto Niepodległości"
    saved_form(h, "PL")  # the same country again: the save alone fetches nothing
    assert len(nager.requests) == 3


def test_the_button_fetches_again_and_replaces_the_data(made, nager):
    old = HolidayData("PL", "2025-01-01 08:00", (Holiday(date(2025, 5, 3), "Stare", "Old"),))
    h = made("PL", saved=old)
    assert nager.requests == [] and status(h) == ""  # a start fetches nothing
    h.controller.open_settings()
    assert status(h) == "Zsynchronizowano 2025-01-01 08:00"
    h.controller.settings_form.syncHolidays()
    h.settle()
    assert len(nager.requests) == 3
    assert date(2025, 5, 3) not in h.controller._holidays.names("pl")  # overwritten, no history
    assert DAY in h.controller._holidays.names("pl")


def test_a_failure_keeps_the_saved_data_and_says_why(made, nager):
    old = HolidayData("PL", "2025-01-01 08:00", (Holiday(date(2025, 5, 3), "Stare", "Old"),))
    h = made("PL", saved=old)
    nager.fail = httpx.Response(503)
    h.controller.settings_form.syncHolidays()
    h.settle()
    assert status(h) == "Nie udało się pobrać świąt: serwis zwrócił błąd 503"
    assert h.controller.settings_form.form["holidayOk"] is False
    assert h.controller._holidays == old and '"Stare"' in made.path.read_text(encoding="utf-8")
    nager.fail = None
    h.controller.settings_form.syncHolidays()
    h.settle()
    assert status(h).startswith("Zsynchronizowano 20")  # the error goes with the next success


def test_a_new_country_that_fails_leaves_the_old_data_unused(made, nager):
    old = HolidayData("PL", "2025-01-01 08:00", (Holiday(DAY, "Stare", "Old"),))
    h = made("PL", saved=old)
    h.controller.main_bridge.calendar.set_holidays(h.controller._holidays, "PL")
    nager.fail = httpx.Response(404)
    saved_form(h, "DE")
    assert status(h) == "Nie udało się pobrać świąt: serwis nie zna tego kraju"
    assert '"country": "PL"' in made.path.read_text(encoding="utf-8")  # the file is untouched
    assert h.controller.main_bridge.summary._holiday_country == "DE"  # and the pages ignore PL's days
    assert h.controller.main_bridge.summary._holidays.names("pl", "DE") == {}


def test_none_deletes_the_holidays_and_fetches_nothing(made, nager):
    h = made()
    saved_form(h, "PL")
    nager.requests.clear()
    saved_form(h, "")
    assert nager.requests == [] and not made.path.exists()
    assert h.controller._holidays == HolidayData() and status(h) == ""
    assert h.controller.main_bridge.calendar._holiday_country == ""


def test_the_pages_are_told_without_a_restart(made):
    h = made()
    bridge = h.controller.main_bridge
    saved_form(h, "PL")
    assert bridge.calendar._holidays.country == "PL" and bridge.summary._holidays.country == "PL"
    assert bridge.calendar._holiday_country == "PL"


def test_a_start_with_a_saved_country_marks_its_holidays_from_the_file(made, nager):
    held = HolidayData("PL", "2026-11-01 08:00", (Holiday(DAY, "Święto", "Day"),))
    h = made("PL", saved=held)
    assert nager.requests == []
    assert h.controller.main_bridge.calendar._holidays == held


def test_the_status_follows_the_interface_language(made):
    h = made()
    saved_form(h, "PL")
    h.controller.save_settings(Settings(url=URL, language="en", holiday_country="PL"), None)
    h.settle()
    assert status(h).startswith("Synchronized 20")


def test_an_answer_for_a_country_given_up_is_dropped(made, nager):
    h = made()
    h.controller.save_settings(Settings(url=URL, language="pl", holiday_country="PL"), None)
    h.controller.save_settings(Settings(url=URL, language="pl", holiday_country=""), None)
    h.settle()
    h.qtbot.waitUntil(lambda: not h.controller.holiday_worker.busy, timeout=3000)
    assert h.controller._holidays == HolidayData() and not made.path.exists()
