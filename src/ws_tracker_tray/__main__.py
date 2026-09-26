"""`python -m ws_tracker_tray [--hidden]` — the Flatpak's command (`ws-tracker-tray`) runs the same."""

import sys

from ws_tracker_tray.ui.main import main

if __name__ == "__main__":
    sys.exit(main())
