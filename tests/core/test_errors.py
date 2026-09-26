import httpx

from ws_tracker_tray.core.errors import ApiError, ErrorKind, TrackerError, describe, read_error

# Payloads captured from Kimai 2.67.0 (TODO/…/0002…/testy/wynik-probe-*.txt).
EXTRA_FIELDS = {
    "code": 400,
    "message": "Validation Failed",
    "errors": {
        "errors": ["This form should not contain extra fields."],
        "children": {"begin": {}, "end": {}, "project": {}, "activity": {}, "description": {}},
    },
}
STOP_BEFORE_START = {
    "code": "400",
    "message": "There was a problem saving.",
    "errors": {
        "children": {
            "end_date": {"errors": ["The end date must not be earlier than the start date."]},
            "duration": {"errors": ["Duration cannot be negative."]},
        }
    },
}


def fake_t(key, **params):
    return key + (repr(sorted(params.items())) if params else "")


def test_401_with_empty_body_is_auth():
    error = ApiError.from_response(httpx.Response(401, content=b""))
    assert (error.kind, error.status) == (ErrorKind.AUTH, 401)


def test_403_is_forbidden_not_a_bad_token():
    # Kimai 2.65: 403 for editing an exported or someone else's entry; a bad token is 401.
    error = ApiError.from_response(httpx.Response(403, json={"code": 403, "message": "Forbidden"}))
    assert (error.kind, error.status) == (ErrorKind.FORBIDDEN, 403)


def test_400_collects_top_level_form_errors():
    error = ApiError.from_response(httpx.Response(400, json=EXTRA_FIELDS))
    assert error.kind is ErrorKind.REJECTED
    assert error.message == "This form should not contain extra fields."


def test_400_collects_nested_field_errors():
    message = read_error(httpx.Response(400, json=STOP_BEFORE_START))
    assert message == "The end date must not be earlier than the start date. Duration cannot be negative."


def test_non_json_error_body_is_cut_to_200_chars():
    assert read_error(httpx.Response(500, text="<html>" + "x" * 500)) == ("<html>" + "x" * 500)[:200]


def test_404_is_not_found_with_message():
    error = ApiError.from_response(httpx.Response(404, json={"code": 404, "message": "Not Found"}))
    assert (error.kind, error.message) == (ErrorKind.NOT_FOUND, "Not Found")


def test_500_is_server():
    assert ApiError.from_response(httpx.Response(500, json={"message": "boom"})).kind is ErrorKind.SERVER


def test_transport_timeout():
    assert ApiError.from_transport(httpx.ReadTimeout("slow")).kind is ErrorKind.TIMEOUT


def test_transport_certificate_problem_is_tls():
    error = httpx.ConnectError("[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed")
    assert ApiError.from_transport(error).kind is ErrorKind.TLS


def test_transport_other_is_connection():
    assert (
        ApiError.from_transport(httpx.ConnectError("Name or service not known")).kind is ErrorKind.CONNECTION
    )


def test_describe_maps_every_kind():
    assert describe(ApiError(ErrorKind.CONNECTION, 0), fake_t) == "errConnection"
    assert describe(ApiError(ErrorKind.TIMEOUT, 0), fake_t) == "errConnection"
    assert describe(ApiError(ErrorKind.TLS, 0), fake_t) == "errTls"
    assert describe(ApiError(ErrorKind.AUTH, 401), fake_t) == "errAuth"
    assert describe(ApiError(ErrorKind.REJECTED, 400, "bad"), fake_t) == "errRejected[('msg', 'bad')]"
    assert describe(ApiError(ErrorKind.REJECTED, 400, ""), fake_t) == "errServer[('code', 400)]"
    assert describe(ApiError(ErrorKind.SERVER, 502), fake_t) == "errServer[('code', 502)]"


def test_describe_tracker_error_and_other_exceptions():
    assert describe(TrackerError("errDescShort", chars=15), fake_t) == "errDescShort[('chars', 15)]"
    assert describe(ValueError("boom"), fake_t) == "boom"


def test_api_error_str_never_contains_headers():
    error = ApiError.from_response(httpx.Response(401, request=httpx.Request("GET", "https://k.test")))
    assert "Bearer" not in str(error)


def test_describe_bad_response():
    assert describe(ApiError(ErrorKind.BAD_RESPONSE, 200), fake_t) == "errUnexpected"


def test_describe_forbidden():
    assert describe(ApiError(ErrorKind.FORBIDDEN, 403, "Forbidden"), fake_t) == "errForbidden"


def redirect(location, url):
    return httpx.Response(301, headers={"Location": location}, request=httpx.Request("GET", url))


def test_redirect_suggests_the_kimai_base_address():
    error = ApiError.from_response(redirect("https://k.test/api/users/me", "http://k.test/api/users/me"))
    assert (error.kind, error.status, error.location) == (ErrorKind.REDIRECT, 301, "https://k.test")


def test_redirect_keeps_a_subpath_and_resolves_relative_locations():
    moved = redirect("https://firma.test/kimai/api/version", "http://firma.test/kimai/api/version")
    assert ApiError.from_response(moved).location == "https://firma.test/kimai"
    relative = redirect("/nowy/api/version", "https://firma.test/stary/api/version")
    assert ApiError.from_response(relative).location == "https://firma.test/nowy"


def test_redirect_without_location_is_a_server_error():
    response = httpx.Response(302, request=httpx.Request("GET", "http://k.test/api/version"))
    assert ApiError.from_response(response).kind is ErrorKind.SERVER


def test_describe_redirect_names_the_new_address():
    error = ApiError(ErrorKind.REDIRECT, 301, location="https://k.test")
    assert describe(error, fake_t) == "errRedirect[('url', 'https://k.test')]"
