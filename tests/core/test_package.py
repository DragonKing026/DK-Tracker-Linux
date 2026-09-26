import re

import dk_tracker


def test_package_has_version():
    assert re.fullmatch(r"\d+\.\d+\.\d+", dk_tracker.__version__)
