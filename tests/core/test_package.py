import re

import ws_tracker_tray


def test_package_has_version():
    assert re.fullmatch(r"\d+\.\d+\.\d+", ws_tracker_tray.__version__)
