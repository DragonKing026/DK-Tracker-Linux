"""`python -m kimai_tray [--hidden]` — the Flatpak's command (`kimai-tray`) runs the same."""

import sys

from kimai_tray.ui.main import main

if __name__ == "__main__":
    sys.exit(main())
