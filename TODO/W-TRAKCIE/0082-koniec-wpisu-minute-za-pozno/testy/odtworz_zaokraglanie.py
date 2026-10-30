"""Repro 0082 on the local test Kimai: how the server rounds the end of a stopped entry.

    eval "$(tests/kimai/kimai-testowe.sh env)"
    .venv/bin/python TODO/W-TRAKCIE/0082-koniec-wpisu-minute-za-pozno/testy/odtworz_zaokraglanie.py

Account `jan` (UTC), so wall-clock times are sent in UTC. Each scenario waits for second 20-40 of a
minute, where "rounded up" and "rounded down" give different minutes.
"""

import os
import time
from datetime import UTC, datetime, timedelta

import httpx

STAMP = "%Y-%m-%dT%H:%M:%S"
client = httpx.Client(
    base_url=os.environ["KIMAI_TEST_URL"],
    headers={"Authorization": f"Bearer {os.environ['KIMAI_TEST_USER_TOKEN']}"},
    timeout=10,
)


def call(method: str, path: str, **kwargs) -> dict:
    response = client.request(method, path, **kwargs)
    if response.status_code >= 400:
        return {"status": response.status_code, "body": response.text[:300]}
    return response.json()


def stamp(moment: datetime) -> str:
    return moment.strftime(STAMP)


def mid_minute() -> None:
    while not 20 <= datetime.now(UTC).second <= 40:
        time.sleep(0.2)


def start(project: int, activity: int, begin: datetime) -> dict:
    body = {"project": project, "activity": activity, "description": "test 0082", "begin": stamp(begin)}
    return call("POST", "/api/timesheets", json=body)


def show(label: str, entry: dict) -> None:
    if "status" in entry:
        print(f"  {label}: HTTP {entry['status']} {entry['body']}")
        return
    print(f"  {label}: begin={entry.get('begin')} end={entry.get('end')} duration={entry.get('duration')}")


def main() -> None:
    for entry in call("GET", "/api/timesheets/active"):
        call("PATCH", f"/api/timesheets/{entry['id']}/stop")
    project = call("GET", "/api/projects")[0]["id"]
    activity = next(a["id"] for a in call("GET", "/api/activities") if a.get("project") in (None, project))
    print("config", call("GET", "/api/config/timesheet"))

    print("1. today: start (now - 1 s), /stop, start again right after")
    mid_minute()
    a = start(project, activity, datetime.now(UTC) - timedelta(seconds=1))
    time.sleep(3)
    print("  stop at", stamp(datetime.now(UTC)))
    a = call("PATCH", f"/api/timesheets/{a['id']}/stop")
    b = start(project, activity, datetime.now(UTC) - timedelta(seconds=1))
    show("A", a)
    show("B running", b)
    b = call("PATCH", f"/api/timesheets/{b['id']}/stop")
    show("B stopped", b)

    print("2. PATCH end = now with seconds (rounded too?)")
    mid_minute()
    a = start(project, activity, datetime.now(UTC) - timedelta(minutes=5))
    end = datetime.now(UTC) - timedelta(seconds=1)
    print("  end sent", stamp(end))
    show("A", call("PATCH", f"/api/timesheets/{a['id']}", json={"end": stamp(end)}))

    print("3. fix: PATCH end = (now - 1 s) floored to the minute, then start (now - 1 s)")
    mid_minute()
    a = start(project, activity, datetime.now(UTC) - timedelta(minutes=5))
    end = (datetime.now(UTC) - timedelta(seconds=1)).replace(second=0, microsecond=0)
    a = call("PATCH", f"/api/timesheets/{a['id']}", json={"end": stamp(end)})
    b = start(project, activity, datetime.now(UTC) - timedelta(seconds=1))
    b = call("PATCH", f"/api/timesheets/{b['id']}/stop")
    show("A", a)
    show("B", b)

    print("4. floored end before the begin (an entry within one minute)")
    mid_minute()
    a = start(project, activity, datetime.now(UTC) - timedelta(seconds=1))
    end = datetime.now(UTC).replace(second=0, microsecond=0)
    print("  end sent", stamp(end))
    show("A", call("PATCH", f"/api/timesheets/{a['id']}", json={"end": stamp(end)}))
    for entry in call("GET", "/api/timesheets/active"):
        call("PATCH", f"/api/timesheets/{entry['id']}/stop")

    print("5. start while another runs (hard limit 1: does Kimai stop the old one, and where?)")
    mid_minute()
    a = start(project, activity, datetime.now(UTC) - timedelta(minutes=5))
    b = start(project, activity, datetime.now(UTC) - timedelta(seconds=1))
    show("A", call("GET", f"/api/timesheets/{a['id']}"))
    show("B", b)
    for entry in call("GET", "/api/timesheets/active"):
        call("PATCH", f"/api/timesheets/{entry['id']}/stop")


if __name__ == "__main__":
    main()
