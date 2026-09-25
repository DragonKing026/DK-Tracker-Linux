"""Billable rules (F-09), mirroring how Kimai derives the flag."""

from __future__ import annotations

from .errors import ApiError, ErrorKind
from .models import Activity, Project


def project_billable(project: Project, non_billable_customers: frozenset[int]) -> bool:
    """A non-billable customer makes every project underneath it non-billable."""
    return project.billable and project.customer_id not in non_billable_customers


def default_billable(
    project: Project | None, activity: Activity | None, non_billable_customers: frozenset[int]
) -> bool:
    """Billable unless the customer, project or activity says otherwise."""
    if project is not None and not project_billable(project, non_billable_customers):
        return False
    return activity is None or activity.billable


def is_billable_rejected(error: BaseException) -> bool:
    """Kimai offers `billable` only to accounts holding edit_billable_own_timesheet (teamlead
    and above by default). For everyone else the whole request fails with a 400 "This form
    should not contain extra fields." — and `billable` is the only optional field we send.
    """
    return (
        isinstance(error, ApiError)
        and error.kind is ErrorKind.REJECTED
        and "extra fields" in error.message.lower()
    )
