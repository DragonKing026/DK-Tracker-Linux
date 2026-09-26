import json

import httpx
import pytest

from ws_tracker_tray.core.errors import ApiError, ErrorKind
from ws_tracker_tray.core.kimai_client import KimaiClient

ENTRY = {
    "id": 8,
    "begin": "2026-09-25T16:04:00+0000",
    "end": None,
    "description": "x" * 20,
    "project": 1,
    "activity": 1,
}


class Recorder:
    """MockTransport handler that records requests and answers from a routing function."""

    def __init__(self, route):
        self.route = route
        self.requests: list[httpx.Request] = []

    def __call__(self, request):
        self.requests.append(request)
        return self.route(request)

    @property
    def last(self):
        return self.requests[-1]


def client_for(route, url="https://kimai.test"):
    recorder = Recorder(route)
    return KimaiClient(url, "secret-token", transport=httpx.MockTransport(recorder)), recorder


def test_sends_bearer_and_accept_headers():
    client, rec = client_for(
        lambda r: httpx.Response(200, json={"id": 1, "username": "jan", "timezone": "UTC"})
    )
    assert client.me().username == "jan"
    assert rec.last.headers["Authorization"] == "Bearer secret-token"
    assert rec.last.headers["Accept"] == "application/json"
    assert rec.last.url.path == "/api/users/me"


def test_base_url_with_subpath_and_trailing_slash():
    client, rec = client_for(
        lambda r: httpx.Response(200, json={"version": "2.67.0"}), url="https://firma.test/kimai/"
    )
    assert client.version() == "2.67.0"
    assert str(rec.last.url) == "https://firma.test/kimai/api/version"


def test_catalog_queries():
    client, rec = client_for(lambda r: httpx.Response(200, json=[]))
    client.projects()
    assert rec.last.url.path == "/api/projects"
    assert dict(rec.last.url.params) == {"visible": "1", "ignoreDates": "1"}
    client.customers()
    assert dict(rec.last.url.params) == {"visible": "1"}
    client.activities()
    assert dict(rec.last.url.params) == {"visible": "1", "globals": "true"}
    client.activities(4)
    assert dict(rec.last.url.params) == {"visible": "1", "globals": "true", "project": "4"}


def test_latest_query_and_parsing():
    client, rec = client_for(lambda r: httpx.Response(200, json=[ENTRY]))
    entries = client.latest(5)
    assert dict(rec.last.url.params) == {"size": "5", "orderBy": "begin", "order": "DESC", "full": "true"}
    assert entries[0].id == 8


def test_active():
    client, rec = client_for(lambda r: httpx.Response(200, json=[ENTRY]))
    assert [e.id for e in client.active()] == [8]
    assert rec.last.url.path == "/api/timesheets/active"


def test_range_follows_total_pages_header():
    def route(request):
        page = int(request.url.params["page"])
        body = [dict(ENTRY, id=page * 10 + i) for i in range(2 if page == 1 else 1)]
        return httpx.Response(200, json=body, headers={"X-Total-Pages": "2"})

    client, rec = client_for(route)
    entries = client.range("2026-09-21T00:00:00", "2026-09-25T23:59:59")
    assert [e.id for e in entries] == [10, 11, 20]
    assert len(rec.requests) == 2
    assert rec.requests[0].url.params["begin"] == "2026-09-21T00:00:00"
    assert rec.requests[0].url.params["size"] == "500"


def test_range_treats_404_after_first_page_as_end():
    def route(request):
        if request.url.params["page"] == "1":
            return httpx.Response(200, json=[ENTRY], headers={"X-Total-Pages": "3"})
        return httpx.Response(404, json={"code": 404, "message": "Not Found"})

    client, _ = client_for(route)
    assert len(client.range("a", "b")) == 1


def test_range_404_on_first_page_is_an_error():
    client, _ = client_for(lambda r: httpx.Response(404, json={"message": "Not Found"}))
    with pytest.raises(ApiError) as caught:
        client.range("a", "b")
    assert caught.value.kind is ErrorKind.NOT_FOUND


def test_start_omits_untouched_billable():
    client, rec = client_for(lambda r: httpx.Response(200, json=ENTRY))
    client.start(project_id=1, activity_id=2, description="d" * 20, begin="2026-09-25T18:04:02")
    assert json.loads(rec.last.content) == {
        "begin": "2026-09-25T18:04:02",
        "project": 1,
        "activity": 2,
        "description": "d" * 20,
    }
    client.start(project_id=1, activity_id=2, description="d" * 20, begin="b", billable=False)
    assert json.loads(rec.last.content)["billable"] is False


def test_stop_and_update():
    client, rec = client_for(lambda r: httpx.Response(200, json=ENTRY))
    client.stop(8)
    assert (rec.last.method, rec.last.url.path) == ("PATCH", "/api/timesheets/8/stop")
    client.update(8, {"description": "nowy opis zadania"})
    assert (rec.last.method, rec.last.url.path) == ("PATCH", "/api/timesheets/8")
    assert json.loads(rec.last.content) == {"description": "nowy opis zadania"}


def test_http_errors_become_api_errors():
    client, _ = client_for(lambda r: httpx.Response(401))
    with pytest.raises(ApiError) as caught:
        client.active()
    assert caught.value.kind is ErrorKind.AUTH


def test_transport_errors_become_api_errors():
    def route(request):
        raise httpx.ConnectError("Name or service not known")

    client, _ = client_for(route)
    with pytest.raises(ApiError) as caught:
        client.active()
    assert caught.value.kind is ErrorKind.CONNECTION


def test_token_is_stripped_of_pasted_whitespace():
    client, rec = client_for(lambda r: httpx.Response(200, json={"version": "2.67.0"}))
    client = KimaiClient("https://kimai.test", "  secret-token\n", transport=httpx.MockTransport(rec))
    client.version()
    assert rec.last.headers["Authorization"] == "Bearer secret-token"


def test_token_never_appears_in_transport_errors():
    token = "abc\ndef-secret"

    def route(request):  # what h11 raises for an illegal header value
        raise httpx.LocalProtocolError(f"Illegal header value b'Bearer {token}'")

    client = KimaiClient("https://kimai.test", token, transport=httpx.MockTransport(route))
    with pytest.raises(ApiError) as caught:
        client.active()
    assert caught.value.kind is ErrorKind.AUTH
    assert "def-secret" not in str(caught.value)
    assert "def-secret" not in caught.value.message


def test_non_json_200_is_a_bad_response_error():
    client, _ = client_for(lambda r: httpx.Response(200, text="<html>Hotel Wi-Fi login</html>"))
    with pytest.raises(ApiError) as caught:
        client.active()
    assert caught.value.kind is ErrorKind.BAD_RESPONSE


def test_wrong_shape_200_is_a_bad_response_error():
    client, _ = client_for(lambda r: httpx.Response(200, json={"message": "x"}))
    with pytest.raises(ApiError) as caught:
        client.me()
    assert caught.value.kind is ErrorKind.BAD_RESPONSE
    with pytest.raises(ApiError) as caught:
        client.active()
    assert caught.value.kind is ErrorKind.BAD_RESPONSE


def test_client_does_not_follow_redirects_but_reports_them():
    moved = lambda r: httpx.Response(301, headers={"Location": "https://kimai.test/api/users/me"})  # noqa: E731
    client, rec = client_for(moved, url="http://kimai.test")
    with pytest.raises(ApiError) as caught:
        client.me()
    assert (caught.value.kind, caught.value.location) == (ErrorKind.REDIRECT, "https://kimai.test")
    assert len(rec.requests) == 1  # the token is not sent a second time


def test_search_asks_kimai_for_the_term_newest_first():
    client, rec = client_for(lambda r: httpx.Response(200, json=[ENTRY]))
    entries = client.search("rezerwacja pokoi")
    assert dict(rec.last.url.params) == {
        "term": "rezerwacja pokoi",
        "size": "50",
        "orderBy": "begin",
        "order": "DESC",
        "full": "true",
    }
    assert entries[0].id == 8
