#!/usr/bin/env bash
# Build a Flatpak manifest inside a Debian trixie container (flatpak 1.16) and produce a .flatpak bundle.
#
# Why: Fedora 44 ships flatpak 1.18.2, whose `build-init --base` fails on SELinux hosts
# (flatpak#6818). The container has no SELinux and an unaffected flatpak.
# The host's runtimes are mounted READ-ONLY and used as local sources — nothing on the host changes
# except the output directory (~/.cache/kimai-tray-flatpak/docker).
#
#   prototyp/flatpak/buduj-w-dockerze.sh <manifest.yml> <app-id>
set -euo pipefail
MANIFEST="$(realpath "$1")"; APP_ID="$2"
WORK="$HOME/.cache/kimai-tray-flatpak/docker"
mkdir -p "$WORK"
SRC_ROOT="$(realpath "$(dirname "$MANIFEST")/..")"

docker run --rm --privileged \
  -v /var/lib/flatpak:/host-system:ro \
  -v "$HOME/.local/share/flatpak":/host-user:ro \
  -v "$SRC_ROOT":/src:ro \
  -v "$WORK":/work \
  -e APP_ID="$APP_ID" -e MANIFEST_REL="$(realpath --relative-to="$SRC_ROOT" "$MANIFEST")" \
  debian:trixie bash -euo pipefail -c '
    apt-get update -qq >/dev/null
    DEBIAN_FRONTEND=noninteractive apt-get install -y -qq flatpak flatpak-builder ostree >/dev/null 2>&1
    flatpak --version
    # Installation repos have no summary file, so copy the needed commits into a local
    # archive repo (cached in /work) and generate one. No network, host repos read-only.
    LOCAL=/work/localrepo
    [ -d "$LOCAL/objects" ] || ostree --repo="$LOCAL" init --mode=archive-z2
    for pair in "/host-system/repo runtime/org.kde.Platform/x86_64/6.11" \
                "/host-user/repo runtime/org.kde.Sdk/x86_64/6.11" \
                "/host-user/repo app/io.qt.PySide.BaseApp/x86_64/6.11"; do
      set -- $pair
      commit=$(ostree --repo="$1" rev-parse "flathub:$2")
      if [ "$(ostree --repo="$LOCAL" rev-parse "$2" 2>/dev/null)" != "$commit" ]; then
        ostree --repo="$LOCAL" pull-local "$1" "$commit"
        ostree --repo="$LOCAL" refs --create="$2" "$commit" --force
      fi
    done
    flatpak build-update-repo "$LOCAL" >/dev/null
    flatpak remote-add --user --no-gpg-verify local "file://$LOCAL"
    flatpak install --user -y --noninteractive --no-related local \
      org.kde.Platform//6.11 org.kde.Sdk//6.11 io.qt.PySide.BaseApp//6.11 >/dev/null
    cp -r /src /tmp/src
    flatpak-builder --user --force-clean --disable-rofiles-fuse --state-dir=/work/state \
      --repo=/work/repo /work/build "/tmp/src/$MANIFEST_REL"
    flatpak build-bundle --runtime-repo=https://flathub.org/repo/flathub.flatpakrepo /work/repo "/work/$APP_ID.flatpak" "$APP_ID"
    chmod -R a+rwX /work
  '
ls -la "$WORK/$APP_ID.flatpak"
