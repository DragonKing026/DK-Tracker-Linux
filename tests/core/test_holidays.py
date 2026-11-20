"""Task 0088: public holidays — parsing Nager.Date, the file, the service (no network: MockTransport)."""

from datetime import UTC, date, datetime

import httpx
import pytest

from dk_tracker.core.errors import ApiError, ErrorKind
from dk_tracker.core.holiday_countries import CODES, COUNTRIES
from dk_tracker.core.holidays import (
    Holiday,
    HolidayData,
    HolidayService,
    describe_error,
    load_holidays,
    merge_days,
    parse_year,
    save_holidays,
)
from dk_tracker.core.i18n import Translator
from dk_tracker.core.settings import Settings, holidays_path, state_path

NOW = datetime(2026, 11, 20, 11, 30, tzinfo=UTC)


def item(day, local, name, *, is_global=True, types=("Public",)):
    return {
        "date": day, "localName": local, "name": name, "countryCode": "PL", "fixed": True,
        "global": is_global, "counties": None, "launchYear": None, "types": list(types),
    }  # fmt: skip


YEAR = [
    item("2026-01-01", "Nowy Rok", "New Year's Day"),
    item("2026-01-06", "Trzech Króli", "Epiphany", is_global=False),  # regional: left out
    item("2026-03-29", "Dzień zmiany czasu", "Clocks change", types=("Optional",)),  # not a day off
    item("2026-11-11", "Narodowe Święto Niepodległości", "Independence Day"),
]


def service(tmp_path, route):
    seen: list[httpx.Request] = []

    def handler(request):
        seen.append(request)
        return route(request)

    return HolidayService(tmp_path / "holidays.json", transport=httpx.MockTransport(handler)), seen


# -- the list of countries ---------------------------------------------------------------


def test_the_snapshot_of_countries_is_whole_and_sane():
    assert len(COUNTRIES) == 204 and len(CODES) == 204
    assert dict(COUNTRIES)["PL"] == "Poland"
    assert all(len(code) == 2 and code.isupper() and name for code, name in COUNTRIES)


# -- parsing -----------------------------------------------------------------------------


def test_only_nationwide_public_holidays_are_kept():
    found = parse_year(YEAR)
    assert [h.day for h in found] == [date(2026, 1, 1), date(2026, 11, 11)]
    assert found[1].local_name == "Narodowe Święto Niepodległości" and found[1].name == "Independence Day"


@pytest.mark.parametrize("payload", [{"a": 1}, "x", [{"date": "2026-01-01"}], [{**YEAR[0], "date": "01.01"}]])
def test_a_wrong_shape_is_a_bad_response(payload):
    with pytest.raises(ApiError) as caught:
        parse_year(payload)
    assert caught.value.kind is ErrorKind.BAD_RESPONSE


def test_two_holidays_of_one_day_are_joined():
    day = date(2026, 4, 5)
    merged = merge_days(
        [
            Holiday(date(2026, 5, 1), "Święto Pracy", "Labour Day"),
            Holiday(day, "Wielkanoc", "Easter"),
            Holiday(day, "Niedziela", "Sunday"),
            Holiday(day, "Wielkanoc", "Easter"),
        ]  # fmt: skip
    )
    assert [h.day for h in merged] == [day, date(2026, 5, 1)]
    assert merged[0].local_name == "Wielkanoc · Niedziela" and merged[0].name == "Easter · Sunday"


def test_the_name_follows_the_interface_language():
    holiday = Holiday(date(2026, 1, 1), "Nowy Rok", "New Year's Day")
    assert holiday.shown("en") == "New Year's Day" and holiday.shown("pl") == "Nowy Rok"
    assert Holiday(date(2026, 1, 1), "", "X").shown("pl") == "X"  # a missing local name


def test_names_of_another_country_count_for_nothing():
    data = HolidayData("PL", "2026-11-20 12:30", (Holiday(date(2026, 1, 1), "Nowy Rok", "New Year's Day"),))
    assert data.names("pl") == {date(2026, 1, 1): "Nowy Rok"}
    assert data.names("en", "PL") == {date(2026, 1, 1): "New Year's Day"}
    assert data.names("pl", "DE") == {} and data.names("pl", "") == {}


# -- the file ----------------------------------------------------------------------------


def test_the_file_round_trips_and_leaves_no_temporary_one(tmp_path):
    data = HolidayData("PL", "2026-11-20 12:30", (Holiday(date(2026, 11, 11), "Święto", "Day"),))
    path = tmp_path / "state" / "holidays.json"
    save_holidays(data, path)
    assert load_holidays(path) == data
    assert [p.name for p in path.parent.iterdir()] == ["holidays.json"]


@pytest.mark.parametrize(
    "text", ["", "{", "[]", '{"country": "PL"}', '{"country":"PL","synced":"","holidays":[{}]}']
)
def test_a_missing_or_broken_file_means_no_holidays(tmp_path, text):
    path = tmp_path / "holidays.json"
    assert load_holidays(path) == HolidayData()
    path.write_text(text, encoding="utf-8")
    assert load_holidays(path) == HolidayData()


def test_the_file_lies_next_to_the_state(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    assert holidays_path() == state_path().parent / "holidays.json"


def test_the_country_setting_is_cleaned_and_must_be_known():
    assert Settings().holiday_country == ""
    assert Settings(holiday_country=" pl ").normalized().holiday_country == "PL"
    assert Settings(holiday_country="ZZ").normalized().holiday_country == ""


# -- the service -------------------------------------------------------------------------


def test_sync_fetches_three_years_and_overwrites_the_file(tmp_path):
    def route(request):
        year = request.url.path.split("/")[-2]
        return httpx.Response(
            200, json=[item(f"{year}-11-11", "Święto", "Day")] + YEAR[:1] * (year == "2026")
        )

    holidays, seen = service(tmp_path, route)
    (tmp_path / "holidays.json").write_text("old", encoding="utf-8")
    data = holidays.sync("PL", NOW)
    assert [r.url.path for r in seen] == [f"/api/v3/PublicHolidays/{y}/PL" for y in (2025, 2026, 2027)]
    assert all(r.url.host == "date.nager.at" and "Authorization" not in r.headers for r in seen)
    assert [h.day for h in data.holidays] == [
        date(2025, 11, 11), date(2026, 1, 1), date(2026, 11, 11), date(2027, 11, 11),
    ]  # fmt: skip
    assert data.country == "PL" and data.synced == NOW.astimezone().strftime("%Y-%m-%d %H:%M")
    assert holidays.load() == data


@pytest.mark.parametrize(
    "answer",
    [
        httpx.Response(404),
        httpx.Response(500),
        httpx.Response(200, text="<html>"),
        httpx.Response(200, json={}),
    ],
)
def test_a_failed_year_leaves_what_was_saved(tmp_path, answer):
    keep = HolidayData("DE", "2026-01-01 08:00", (Holiday(date(2026, 1, 1), "Neujahr", "New Year"),))
    holidays, _ = service(
        tmp_path, lambda r: httpx.Response(200, json=[]) if "2025" in r.url.path else answer
    )
    save_holidays(keep, tmp_path / "holidays.json")
    with pytest.raises(ApiError):
        holidays.sync("PL", NOW)
    assert holidays.load() == keep


def test_a_dead_network_is_a_connection_error(tmp_path):
    def route(request):
        raise httpx.ConnectError("down")

    holidays, _ = service(tmp_path, route)
    with pytest.raises(ApiError) as caught:
        holidays.sync("PL", NOW)
    assert caught.value.kind is ErrorKind.CONNECTION
    assert not (tmp_path / "holidays.json").exists()


def test_clear_removes_the_file_and_is_harmless_twice(tmp_path):
    holidays, _ = service(tmp_path, lambda r: httpx.Response(200, json=YEAR))
    holidays.sync("PL", NOW)
    holidays.clear()
    holidays.clear()
    assert holidays.load() == HolidayData()


def test_errors_are_described_in_both_languages():
    pl, en = Translator("pl"), Translator("en")
    assert describe_error(ApiError(ErrorKind.TIMEOUT, 0), pl) == "brak połączenia z date.nager.at"
    assert describe_error(ApiError(ErrorKind.NOT_FOUND, 404), en) == "the service does not know this country"
    assert describe_error(ApiError(ErrorKind.BAD_RESPONSE, 200), en) == "unexpected answer from the service"
    assert describe_error(ApiError(ErrorKind.SERVER, 503), pl) == "serwis zwrócił błąd 503"
    assert describe_error(ValueError("x"), pl) == "x"
