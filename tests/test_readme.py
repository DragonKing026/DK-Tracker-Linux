"""README.md (VS Code, Obsidian) and .github/README.md (the GitHub page) tell the same story.

The GitHub copy has no front matter (GitHub would render it as a table) and its links start
with ../ because it lives in .github/ — apart from that the two must not drift apart.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return re.sub(r"\A---\n.*?\n---\n\n?", "", text, count=1, flags=re.S)


def test_both_readmes_have_the_same_content():
    github = body(ROOT / ".github" / "README.md").replace("](../", "](")
    assert body(ROOT / "README.md") == github


def test_only_the_repository_readme_has_front_matter():
    assert (ROOT / "README.md").read_text(encoding="utf-8").startswith("---\n")
    assert not (ROOT / ".github" / "README.md").read_text(encoding="utf-8").startswith("---")
