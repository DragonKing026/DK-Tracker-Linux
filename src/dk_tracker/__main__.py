"""`python -m dk_tracker [--hidden]` — the Flatpak's command (`dk-tracker`) runs the same."""

import sys

from dk_tracker.ui.main import main

if __name__ == "__main__":
    sys.exit(main())
