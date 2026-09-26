#!/usr/bin/env bash
# Development install on the host: .desktop entry + icon in ~/.local/share, launching this
# checkout with the system Python (PySide6 from Fedora — layer-shell works there).
# The desktop entry gives the app its name and icon in notifications and the task bar.
#   scripts/instaluj-dev.sh          install
#   scripts/instaluj-dev.sh --usun   remove
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APP=io.github.dragonking026.WS-Tracker-Linux
APPS="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
ICONS="${XDG_DATA_HOME:-$HOME/.local/share}/icons/hicolor/512x512/apps"

if [[ "${1:-}" == "--usun" ]]; then
    rm -f "$APPS/$APP.desktop" "$ICONS/$APP.png"
    echo "Usunięto $APP.desktop i ikonę."
    exit 0
fi

mkdir -p "$APPS" "$ICONS"
install -m 644 "$ROOT/src/ws_tracker/ui/assets/ws-tracker.png" "$ICONS/$APP.png"
sed "s|^Exec=.*|Exec=env PYTHONPATH=\"$ROOT/src\" /usr/bin/python3 -m ws_tracker|" \
    "$ROOT/data/$APP.desktop" > "$APPS/$APP.desktop"
command -v update-desktop-database >/dev/null && update-desktop-database -q "$APPS" || true
echo "Zainstalowano $APPS/$APP.desktop (Exec: python3 -m ws_tracker z $ROOT/src)."
