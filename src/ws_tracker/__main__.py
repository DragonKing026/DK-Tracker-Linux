"""`python -m ws_tracker [--hidden]` — the Flatpak's command (`ws-tracker`) runs the same."""

import sys

from ws_tracker.ui.main import main

if __name__ == "__main__":
    sys.exit(main())
