#!/usr/bin/env bash
# Local Kimai for tests: start, seed accounts/tokens/data, print connection details, stop.
#
#   tests/kimai/kimai-testowe.sh up       # start + seed (idempotent), prints env exports
#   tests/kimai/kimai-testowe.sh env      # print env exports for a running instance
#   tests/kimai/kimai-testowe.sh down     # stop and delete everything (volumes too)
#
# Tokens are inserted straight into kimai2_access_token: Kimai has no console command
# for API tokens but stores them in plain text (checked on 2.67.0). If a future Kimai
# changes that, "up" fails loudly on the token check instead of running tests blind.
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE=(docker compose -f "$DIR/docker-compose.yml")
PORT="${KIMAI_TEST_PORT:-8001}"
URL="http://127.0.0.1:${PORT}"

ADMIN_TOKEN="kimai-tray-test-admin-token-000000000001"
USER_TOKEN="kimai-tray-test-user-token-0000000000002"
LEAD_TOKEN="kimai-tray-test-lead-token-0000000000003"

console() { "${COMPOSE[@]}" exec -T kimai /opt/kimai/bin/console "$@"; }
sql() { "${COMPOSE[@]}" exec -T sqldb mysql -ukimai -pkimai kimai -N -e "$1" 2>/dev/null; }
api() { # api TOKEN METHOD PATH [JSON]
  curl -sf -X "$2" -H "Authorization: Bearer $1" -H "Accept: application/json" \
    ${4:+-H "Content-Type: application/json" -d "$4"} "${URL}$3"
}

wait_ready() {
  for _ in $(seq 1 60); do
    [[ "$(curl -s -o /dev/null -w '%{http_code}' "${URL}/en/login")" == 200 ]] && return 0
    sleep 3
  done
  echo "Kimai did not answer on ${URL} within 3 minutes" >&2
  "${COMPOSE[@]}" logs --tail 50 kimai >&2
  exit 1
}

ensure_user() { # login email role password
  if ! console kimai:user:list | grep -qw "$1"; then
    console kimai:user:create "$1" "$2" "$3" "$4" >/dev/null
  fi
}

set_timezone() { # login zone — Kimai reads the account zone from kimai2_user_preferences
  sql "UPDATE kimai2_user_preferences SET value = '$2' WHERE name = 'timezone'
       AND user_id = (SELECT id FROM kimai2_users WHERE username = '$1');"
}

ensure_token() { # login token
  sql "INSERT INTO kimai2_access_token (user_id, token, name)
       SELECT id, '$2', 'kimai-tray-tests' FROM kimai2_users WHERE username = '$1'
       AND NOT EXISTS (SELECT 1 FROM kimai2_access_token WHERE token = '$2');"
  if ! api "$2" GET /api/users/me >/dev/null; then
    echo "Token for '$1' is rejected — did Kimai change how API tokens are stored?" >&2
    exit 1
  fi
}

# Project colours must come from Kimai's fixed palette (theme.color_choices), e.g. Green #008000.
seed_data() {
  if [[ "$(api "$ADMIN_TOKEN" GET /api/customers)" != "[]" ]]; then
    return 0
  fi
  local c1 c2
  c1=$(api "$ADMIN_TOKEN" POST /api/customers '{"name":"Hotel Morski","country":"PL","currency":"PLN","timezone":"Europe/Warsaw","visible":true,"billable":true}' | python3 -c 'import json,sys;print(json.load(sys.stdin)["id"])')
  c2=$(api "$ADMIN_TOKEN" POST /api/customers '{"name":"Sprawy wewnętrzne","country":"PL","currency":"PLN","timezone":"Europe/Warsaw","visible":true,"billable":false}' | python3 -c 'import json,sys;print(json.load(sys.stdin)["id"])')
  api "$ADMIN_TOKEN" POST /api/projects "{\"name\":\"Moduł rezerwacji\",\"customer\":$c1,\"visible\":true,\"billable\":true,\"globalActivities\":true,\"color\":\"#008000\"}" >/dev/null
  api "$ADMIN_TOKEN" POST /api/projects "{\"name\":\"Integracja z KSeF\",\"customer\":$c1,\"visible\":true,\"billable\":true,\"globalActivities\":true,\"color\":\"#008080\"}" >/dev/null
  api "$ADMIN_TOKEN" POST /api/projects "{\"name\":\"Administracja\",\"customer\":$c2,\"visible\":true,\"billable\":true,\"globalActivities\":true,\"color\":\"#808080\"}" >/dev/null
  api "$ADMIN_TOKEN" POST /api/activities '{"name":"Programowanie","visible":true,"billable":true}' >/dev/null
  api "$ADMIN_TOKEN" POST /api/activities '{"name":"Spotkanie","visible":true,"billable":true}' >/dev/null
  api "$ADMIN_TOKEN" POST /api/activities '{"name":"Szkolenie wewnętrzne","visible":true,"billable":false}' >/dev/null
}

print_env() {
  cat <<ENV
export KIMAI_TEST_URL=${URL}
export KIMAI_TEST_ADMIN_TOKEN=${ADMIN_TOKEN}   # admin, ROLE_SUPER_ADMIN
export KIMAI_TEST_USER_TOKEN=${USER_TOKEN}    # jan, ROLE_USER (no billable permission)
export KIMAI_TEST_LEAD_TOKEN=${LEAD_TOKEN}    # kierownik, ROLE_TEAMLEAD (billable allowed, zone of this computer)
ENV
}

case "${1:-}" in
  up)
    "${COMPOSE[@]}" up -d --wait sqldb >/dev/null
    "${COMPOSE[@]}" up -d kimai >/dev/null
    wait_ready
    ensure_user jan jan@kimai.test ROLE_USER jan12345
    ensure_user kierownik kierownik@kimai.test ROLE_TEAMLEAD kier12345
    ensure_token admin "$ADMIN_TOKEN"
    ensure_token jan "$USER_TOKEN"
    ensure_token kierownik "$LEAD_TOKEN"
    # jan stays in UTC (contract tests check the account-zone logic against it);
    # kierownik gets this computer's zone, for manual tests without the timezone warning.
    set_timezone kierownik "${LOCAL_TZ:-$(timedatectl show -p Timezone --value 2>/dev/null || echo Europe/Warsaw)}"
    seed_data
    echo "Kimai $(api "$ADMIN_TOKEN" GET /api/version | python3 -c 'import json,sys;print(json.load(sys.stdin)["version"])') ready at ${URL}" >&2
    print_env
    ;;
  env) print_env ;;
  down) "${COMPOSE[@]}" down -v ;;
  *) sed -n '2,8p' "$0"; exit 2 ;;
esac
