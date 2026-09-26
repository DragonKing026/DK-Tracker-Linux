from ws_tracker.core.billable import default_billable, is_billable_rejected, project_billable
from ws_tracker.core.errors import ApiError, ErrorKind
from ws_tracker.core.models import Activity, Project

BILLED = Project(1, "Rezerwacje", 10, "Hotel", None, True)
UNBILLED_PROJECT = Project(2, "Wewnętrzny", 10, "Hotel", None, False)
UNBILLED_CUSTOMER = Project(3, "Administracja", 20, "Sprawy wewnętrzne", None, True)
CODING = Activity(1, "Programowanie", True, None)
TRAINING = Activity(2, "Szkolenie", False, None)


def test_project_billable_combines_project_and_customer():
    assert project_billable(BILLED, frozenset({20})) is True
    assert project_billable(UNBILLED_PROJECT, frozenset()) is False
    assert project_billable(UNBILLED_CUSTOMER, frozenset({20})) is False


def test_default_billable_mirrors_kimai():
    assert default_billable(BILLED, CODING, frozenset()) is True
    assert default_billable(BILLED, TRAINING, frozenset()) is False
    assert default_billable(UNBILLED_CUSTOMER, CODING, frozenset({20})) is False
    assert default_billable(None, None, frozenset()) is True


def test_is_billable_rejected_only_for_extra_fields_400():
    rejected = ApiError(ErrorKind.REJECTED, 400, "This form should not contain extra fields.")
    assert is_billable_rejected(rejected) is True
    assert is_billable_rejected(ApiError(ErrorKind.REJECTED, 400, "Duration cannot be negative.")) is False
    assert is_billable_rejected(ApiError(ErrorKind.AUTH, 401)) is False
    assert is_billable_rejected(ValueError("extra fields")) is False
