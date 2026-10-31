"""Coverage-guided fuzzing (Atheris/libFuzzer) of the pure functions that parse and format user text.

Run from the repository root, with the dev environment of requirements-ci.txt (Linux x86-64):

    python fuzz/fuzz_core.py -max_total_time=60

A crash is any exception other than the ones the function documents (`ValueError` from `at_wall_clock`) or a
broken invariant; libFuzzer saves the input as `crash-*`. CI runs a short pass in testy.yml.
"""

import sys
from datetime import UTC, datetime

import atheris

with atheris.instrument_imports():
    from dk_tracker.core.grouping import sort_key
    from dk_tracker.core.timefmt import at_wall_clock, badge_label, clock, short_duration, weekday_index
    from dk_tracker.core.validation import check_description

DAY = datetime(2026, 9, 25, 12, tzinfo=UTC)


def fuzz_one(data: bytes) -> None:
    """One input: the bytes drive every function once."""
    provider = atheris.FuzzedDataProvider(data)
    seconds = provider.ConsumeFloat()
    if seconds == seconds and abs(seconds) < 1e15:  # NaN and huge values are not what the UI passes
        assert clock(seconds).count(":") == 2
        assert short_duration(seconds).count(":") == 1
        assert badge_label(seconds)

    text = provider.ConsumeUnicode(provider.ConsumeIntInRange(0, 64))
    tz = UTC
    try:
        moment = at_wall_clock(DAY, text, tz)
    except ValueError:
        pass
    else:
        assert moment.date() == DAY.date()

    result = check_description(text, provider.ConsumeIntInRange(-2, 40))
    assert result.ok or result.reason in {"short", "generic"}
    assert isinstance(sort_key(text), str)
    assert 0 <= weekday_index(text) <= 6


def main() -> None:
    atheris.Setup(sys.argv, fuzz_one)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
