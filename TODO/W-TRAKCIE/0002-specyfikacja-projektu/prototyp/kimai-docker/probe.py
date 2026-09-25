"""Spike: verify Kimai API behaviours the app relies on, against the throwaway container."""
import datetime as dt
import json
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:8001"
ADMIN, USER = "test-admin-token-0123456789", "test-user-token-0123456789"


def call(token, method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": f"Bearer {token}", "Accept": "application/json",
                                          **({"Content-Type": "application/json"} if body is not None else {})})
    try:
        with urllib.request.urlopen(req) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw else None), dict(r.headers)
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return e.code, json.loads(raw), dict(e.headers)
        except ValueError:
            return e.code, raw[:200], dict(e.headers)


from zoneinfo import ZoneInfo

# Kimai reads a submitted wall-clock time in the *Kimai user's* timezone, so every
# time we send must be computed there, not in the timezone of this machine.
USER_TZ = ZoneInfo(call(USER, "GET", "/api/users/me")[1]["timezone"])


def kimai_time(delta=dt.timedelta(0)):
    return (dt.datetime.now(USER_TZ) + delta).strftime("%Y-%m-%dT%H:%M:%S")


def now_local():
    return kimai_time(-dt.timedelta(seconds=1))


s, customers, _ = call(ADMIN, "GET", "/api/customers")
if not customers:
    s, c1, _ = call(ADMIN, "POST", "/api/customers", {"name": "Hotel Morski", "country": "PL", "currency": "PLN", "timezone": "Europe/Warsaw", "visible": True, "billable": True})
    s, c2, _ = call(ADMIN, "POST", "/api/customers", {"name": "Sprawy wewnętrzne", "country": "PL", "currency": "PLN", "timezone": "Europe/Warsaw", "visible": True, "billable": False})
    call(ADMIN, "POST", "/api/projects", {"name": "Moduł rezerwacji", "customer": c1["id"], "visible": True, "billable": True, "globalActivities": True})
    call(ADMIN, "POST", "/api/projects", {"name": "Administracja", "customer": c2["id"], "visible": True, "billable": True, "globalActivities": True})
    call(ADMIN, "POST", "/api/activities", {"name": "Programowanie", "visible": True, "billable": True})
s, projects, _ = call(USER, "GET", "/api/projects?visible=1&ignoreDates=1")
p1 = next(p for p in projects if p["name"] == "Moduł rezerwacji")
p2 = next(p for p in projects if p["name"] == "Administracja")
s, acts, _ = call(USER, "GET", "/api/activities?visible=1&globals=true")
a1 = acts[0]
print("user projects", [p["name"] for p in projects], "activities", [a["name"] for a in acts])
print("user timezone:", USER_TZ)
# clean slate: entries left from a run with wrong times get a sane begin, then stop
for a in call(USER, "GET", "/api/timesheets/active")[1]:
    call(USER, "PATCH", f"/api/timesheets/{a['id']}", {"begin": kimai_time(-dt.timedelta(hours=1))})
    print("cleanup stop", call(USER, "PATCH", f"/api/timesheets/{a['id']}/stop")[0])

print("\n== start with billable as ROLE_USER")
s, body, _ = call(USER, "POST", "/api/timesheets", {"begin": now_local(), "project": p1["id"], "activity": a1["id"], "description": "Test billable", "billable": False})
print(s, body)
if s == 200:
    call(USER, "PATCH", f"/api/timesheets/{body['id']}/stop")

print("\n== start without billable (begin 10 min ago)")
ago = kimai_time(-dt.timedelta(minutes=10))
s, e1, _ = call(USER, "POST", "/api/timesheets", {"begin": ago, "project": p1["id"], "activity": a1["id"], "description": "Formularz rezerwacji"})
print(s, {k: e1.get(k) for k in ("id", "begin", "end", "billable")} if s == 200 else e1)

s, active, _ = call(USER, "GET", "/api/timesheets/active")
print("active", s, [(a["id"], a["begin"]) for a in active])

print("\n== second start while running (default limit 1)")
s, e2, _ = call(USER, "POST", "/api/timesheets", {"begin": now_local(), "project": p2["id"], "activity": a1["id"], "description": "Drugi wpis"})
print(s, e2.get("id") if s == 200 else e2)

s, active, _ = call(USER, "GET", "/api/timesheets/active")
print("active after 2nd start", [(a["id"]) for a in active])
s, first, _ = call(USER, "GET", f"/api/timesheets/{e1['id']}")
print("first entry end after auto-stop:", first.get("end"))

print("\n== stop running")
running_id = call(USER, "GET", "/api/timesheets/active")[1][0]["id"]
s, stopped, _ = call(USER, "PATCH", f"/api/timesheets/{running_id}/stop")
print(s, stopped.get("end") if s == 200 else stopped)

print("\n== stop already-stopped entry")
s, body, _ = call(USER, "PATCH", f"/api/timesheets/{running_id}/stop")
print(s, body)

print("\n== begin in the future")
fut = kimai_time(dt.timedelta(hours=2))
s, body, _ = call(USER, "POST", "/api/timesheets", {"begin": fut, "project": p1["id"], "activity": a1["id"], "description": "Przyszłość"})
print(s, body)

print("\n== pagination: page past the end")
s, body, h = call(USER, "GET", "/api/timesheets?size=1&page=1")
print("page1", s, {k: v for k, v in h.items() if k.lower().startswith("x-")})
s, body, h = call(USER, "GET", "/api/timesheets?size=1&page=99")
print("page99", s, body if s != 200 else len(body))

print("\n== latest with full=true: fields present")
s, body, _ = call(USER, "GET", "/api/timesheets?size=5&orderBy=begin&order=DESC&full=true")
e = body[0]
print(s, sorted(e.keys()))
print("project keys:", sorted(e["project"].keys()))
print("user.language:", e.get("user", {}).get("language") if isinstance(e.get("user"), dict) else e.get("user"))

print("\n== bad token")
s, body, _ = call("nope", "GET", "/api/timesheets/active")
print(s, body)
