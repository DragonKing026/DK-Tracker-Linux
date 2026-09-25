"""Tests of mdfix.py: `python3 -m pytest .claude/skills/markdownlint -q`."""

import importlib.util
import re
from pathlib import Path

spec = importlib.util.spec_from_file_location("mdfix", Path(__file__).with_name("mdfix.py"))
mdfix = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mdfix)


def same_text(before: str, after: list[str]) -> bool:
    return re.sub(r"\s+", " ", before).strip() == re.sub(r"\s+", " ", " ".join(after)).strip()


def test_punctuation_stays_glued_to_code_and_links():
    line = "- Create: " + "`testy/lista-kontrolna.md`, " * 6 + "[plik](../a.md). **nigdy**"
    wrapped = mdfix.wrap_line(line)
    assert all(len(part) <= 120 for part in wrapped)
    assert "` ," not in " ".join(wrapped)
    assert same_text(line[2:], [w.strip().removeprefix("- ") for w in wrapped])


def test_a_line_never_starts_with_a_marker():
    line = "Tekst " * 18 + "- myślnik 12. numer # hash > cytat"
    for part in mdfix.wrap_line(line)[1:]:
        assert not mdfix.risky(part.split()[0])


def test_list_item_continuation_is_indented():
    wrapped = mdfix.wrap_line("- [ ] " + "słowo " * 30)
    assert wrapped[0].startswith("- [ ] ")
    assert all(part.startswith("      ") for part in wrapped[1:])


def test_long_code_span_may_break():
    line = "  - `Entry(" + ", ".join(f"field_{n}: int" for n in range(20)) + ")`"
    assert all(len(part) <= 120 for part in mdfix.wrap_line(line))


def test_callout_title_is_kept_whole():
    line = "> [!warning] " + "tytuł " * 30
    assert mdfix.wrap_line(line) == [line]


def test_tables_become_compact():
    fixed = mdfix.fix_text("| a | b|\n|---|:---:|\n| `x|y` | z |")
    assert fixed == "| a | b |\n| --- | :---: |\n| `x|y` | z |"


def test_front_matter_and_code_are_untouched():
    text = "---\ntags: [" + "a, " * 60 + "]\n---\n\n```python\n" + "x = 1  # " + "y" * 150 + "\n```"
    assert mdfix.fix_text(text) == text


def test_a_marker_word_moves_with_its_neighbour_instead_of_overflowing():
    line = "x" * 100 + " aaaa bbbb cccc dddd eeee = ffff"
    for part in mdfix.wrap_line(line):
        assert len(part) <= 120
    assert not mdfix.risky(mdfix.wrap_line(line)[-1].split()[0])
