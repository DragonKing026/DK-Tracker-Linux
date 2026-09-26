#!/usr/bin/env bash
# One-off: the key that signs the Flatpak repository on GitHub Pages.
#
#   flatpak/klucz-gpg.sh
#
# Creates the key in a throwaway GnuPG home (your own keyring stays untouched), writes the PUBLIC key
# to flatpak/ws-tracker-tray-repo.gpg (committed — it goes into .flatpakrepo/.flatpakref) and the PRIVATE key
# to ~/ws-tracker-tray-repo-private.asc for the GitHub secret FLATPAK_GPG_PRIVATE_KEY. Then delete that file.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PRIVATE="$HOME/ws-tracker-tray-repo-private.asc"
[[ -e "$PRIVATE" ]] && { echo "$PRIVATE już istnieje — nie nadpisuję." >&2; exit 1; }
# A second key would silently replace the one every installed copy trusts.
[[ -e "$HERE/ws-tracker-tray-repo.gpg" ]] && { echo "$HERE/ws-tracker-tray-repo.gpg już jest — nie tworzę nowego klucza." >&2; exit 1; }
HOMEDIR="$(mktemp -d)"
trap 'rm -rf "$HOMEDIR"' EXIT
export GNUPGHOME="$HOMEDIR"
gpg --batch --pinentry-mode loopback --passphrase '' \
  --quick-gen-key "WS Tracker Tray Flatpak repository <ws-tracker-tray@users.noreply.github.com>" rsa4096 sign never
KEY_ID="$(gpg --list-keys --with-colons | awk -F: '/^fpr/ {print $10; exit}')"
gpg --export "$KEY_ID" > "$HERE/ws-tracker-tray-repo.gpg"
( umask 077; gpg --armor --export-secret-keys "$KEY_ID" > "$PRIVATE" )
echo "Klucz: $KEY_ID"
echo "Publiczny: $HERE/ws-tracker-tray-repo.gpg (do commita)"
echo "Prywatny:  $PRIVATE → gh secret set FLATPAK_GPG_PRIVATE_KEY < \"$PRIVATE\" && shred -u \"$PRIVATE\""
