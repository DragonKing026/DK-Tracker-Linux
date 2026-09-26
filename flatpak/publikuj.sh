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

# Users trust only the committed public key; signing with any other key would break every install and update.
GPG_HOME=()
[[ -n "$HOMEDIR" ]] && GPG_HOME=(--homedir "$HOMEDIR")
TRUSTED="$(gpg "${GPG_HOME[@]}" --show-keys --with-colons "$HERE/ws-tracker-tray-repo.gpg" | awk -F: '/^fpr/ {print $10; exit}')"
SIGNING="$(gpg "${GPG_HOME[@]}" --list-keys --with-colons "$KEY" | awk -F: '/^fpr/ {print $10; exit}')"
if [[ -z "$TRUSTED" || "$TRUSTED" != "$SIGNING" ]]; then
  echo "Klucz podpisujący ${SIGNING:-$KEY} to nie klucz z flatpak/ws-tracker-tray-repo.gpg (${TRUSTED:-brak})." >&2
  exit 1
fi

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
