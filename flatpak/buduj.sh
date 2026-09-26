#!/usr/bin/env bash
# Build the Flatpak in the same container GitHub Actions uses, then check it and (optionally) install it.
#
#   flatpak/buduj.sh              → dist/pl.websystems.WsTrackerTray-<version>.flatpak (+ OSTree repo in the cache)
#   flatpak/buduj.sh --zainstaluj → the same, then `flatpak install --user --bundle` on this computer
#
# Why a container: Fedora 44's Flatpak 1.18.2 cannot build with a `base:` app (flatpak#6818, ADR-0006);
# the flathub-infra image carries Flatpak 1.18.1 and the KDE 6.11 SDK, plus appstreamcli and the linter.
# Downloads (runtime, PySide base) and build state are cached in ~/.cache/ws-tracker-tray-flatpak.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APP=pl.websystems.WsTrackerTray
IMAGE=ghcr.io/flathub-infra/flatpak-github-actions:kde-6.11
CACHE="${XDG_CACHE_HOME:-$HOME/.cache}/ws-tracker-tray-flatpak"
VERSION="$(sed -n 's/^version = "\(.*\)"/\1/p' "$ROOT/pyproject.toml")"
BUNDLE="$APP-$VERSION.flatpak"
# Findings that only matter for Flathub, not for our own repository on GitHub Pages:
# the websystems.pl certificate (from the app id) and screenshots mirrored into the OSTree repo or Flathub media.
ALLOWED_LINT="appid-url-not-reachable appstream-screenshots-not-mirrored-in-ostree appstream-missing-screenshots appstream-external-screenshot-url"

mkdir -p "$CACHE" "$ROOT/dist"
docker run --rm --privileged \
  -v "$ROOT":/src:ro -v "$CACHE":/work -v "$ROOT/dist":/dist \
  -e HOME=/work/home -e APP="$APP" -e BUNDLE="$BUNDLE" -e ALLOWED_LINT="$ALLOWED_LINT" \
  "$IMAGE" bash -euo pipefail -c '
    rm -rf /tmp/src && mkdir /tmp/src
    tar -C /src --exclude=.venv --exclude=.git --exclude=dist -cf - . | tar -C /tmp/src -xf -
    appstreamcli validate --no-net "/tmp/src/data/$APP.metainfo.xml"
    desktop-file-validate "/tmp/src/data/$APP.desktop"
    flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
    flatpak-builder --user --install-deps-from=flathub --force-clean --disable-rofiles-fuse \
      --state-dir=/work/state --repo=/work/repo /work/build "/tmp/src/flatpak/$APP.yml" > /work/build.log 2>&1 \
      || { tail -40 /work/build.log; exit 1; }
    flatpak build-bundle --runtime-repo=https://flathub.org/repo/flathub.flatpakrepo /work/repo "/dist/$BUNDLE" "$APP"
    for target in "manifest /tmp/src/flatpak/$APP.yml" "repo /work/repo"; do
      set -- $target
      flatpak-builder-lint "$1" "$2" > /work/lint.json || true
      python3 - "$1" <<PY
import json, os, sys
found = set(json.load(open("/work/lint.json")).get("errors", []))
unexpected = found - set(os.environ["ALLOWED_LINT"].split())
print(f"lint {sys.argv[1]}: " + (", ".join(sorted(unexpected)) or "OK"))
sys.exit(1 if unexpected else 0)
PY
    done
    chmod -R a+rwX /work /dist
  '
echo "Paczka: $ROOT/dist/$BUNDLE"
if [[ "${1:-}" == "--zainstaluj" ]]; then
  flatpak install --user -y --noninteractive --bundle "$ROOT/dist/$BUNDLE"
fi
