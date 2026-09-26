import re

import ws_tracker


def test_package_has_version():
    assert re.fullmatch(r"\d+\.\d+\.\d+", ws_tracker.__version__)
