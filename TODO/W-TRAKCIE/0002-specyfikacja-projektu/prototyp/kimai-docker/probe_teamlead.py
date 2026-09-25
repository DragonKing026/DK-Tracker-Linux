"""Spike: billable override works for an account holding edit_billable_own_timesheet (teamlead)."""
import datetime as dt
from zoneinfo import ZoneInfo

src = open("probe.py", encoding="utf-8").read().split("s, customers, _")[0]
ns: dict = {}
exec(src, ns)
call = ns["call"]
LEAD = "test-teamlead-token-0123456789"
tz = ZoneInfo(call(LEAD, "GET", "/api/users/me")[1]["timezone"])
t = lambda d: (dt.datetime.now(tz) + d).strftime("%Y-%m-%dT%H:%M:%S")

for a in call(ns["USER"], "GET", "/api/timesheets/active")[1]:  # leftover future entry of jan
    call(ns["USER"], "PATCH", f"/api/timesheets/{a['id']}", {"begin": t(-dt.timedelta(minutes=30))})
    print("cleanup jan", call(ns["USER"], "PATCH", f"/api/timesheets/{a['id']}/stop")[0])

projects = call(LEAD, "GET", "/api/projects?visible=1&ignoreDates=1")[1]
p1 = next(p for p in projects if p["name"] == "Moduł rezerwacji")
a1 = call(LEAD, "GET", "/api/activities?visible=1&globals=true")[1][0]
s, e, _ = call(LEAD, "POST", "/api/timesheets", {"begin": t(-dt.timedelta(minutes=5)), "project": p1["id"],
                                                  "activity": a1["id"], "description": "Teamlead billable=false", "billable": False})
print("teamlead start billable=false:", s, e.get("billable") if s == 200 else e)
s, e2, _ = call(LEAD, "PATCH", f"/api/timesheets/{e['id']}", {"billable": True})
print("teamlead PATCH billable=true:", s, e2.get("billable") if s == 200 else e2)
print("stop:", call(LEAD, "PATCH", f"/api/timesheets/{e['id']}/stop")[0])
