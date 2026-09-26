#!/usr/bin/env bash
# Turn a built OSTree repo into the site GitHub Pages serves: signed repo + .flatpakrepo/.flatpakref.
#
#   flatpak/publikuj.sh <repo> <site-dir> <base-url> <gpg-key-id> [gpg-homedir]
#
# Runs inside the flathub-infra container (GitHub Actions: wydanie.yml; locally for a dry run).
# The app commit is signed (again — idempotent) and the summary too, so `flatpak` on people's
# computers verifies everything with the public key in flatpak/ws-tracker-tray-repo.gpg.
set -euo pipefail
REPO="$1"; SITE="$2"; URL="$3"; KEY="$4"; HOMEDIR="${5:-}"
APP=pl.websystems.WsTrackerTray
HERE="$(cd "$(dirname "$0")" && pwd)"
GPG=(--gpg-sign="$KEY")
[[ -n "$HOMEDIR" ]] && GPG+=(--gpg-homedir="$HOMEDIR")

# Every ref of the app — the app itself and its .Locale/.Debug extensions — must carry a signature.
for ref in $(ostree --repo="$REPO" refs | grep -F "$APP"); do
  kind="${ref%%/*}"; rest="${ref#*/}"; id="${rest%%/*}"; branch="${ref##*/}"
  if [[ "$kind" == runtime ]]; then
    flatpak build-sign "${GPG[@]}" --runtime "$REPO" "$id" "$branch"
  else
    flatpak build-sign "${GPG[@]}" "$REPO" "$id" "$branch"
  fi
done
flatpak build-update-repo "${GPG[@]}" --generate-static-deltas --prune "$REPO"
mkdir -p "$SITE"
rm -rf "$SITE/repo"
cp -a "$REPO" "$SITE/repo"
python3 "$HERE/pages.py" "$SITE" "$URL" "$HERE/ws-tracker-tray-repo.gpg"
echo "Strona repozytorium: $SITE ($URL)"
