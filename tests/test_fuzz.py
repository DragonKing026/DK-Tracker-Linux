"""The Atheris harness in fuzz/ keeps working (CI also runs it as a fuzzer for half a minute)."""

import pytest

pytest.importorskip("atheris")  # Linux x86-64 wheels only; requirements-ci.txt has it


def test_fuzz_target_accepts_arbitrary_bytes():
    from fuzz import fuzz_core

    for data in (b"", b"\x00" * 64, bytes(range(256)), b"12:30 poprawki #4"):
        fuzz_core.fuzz_one(data)
