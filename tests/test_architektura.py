"""Layer rules from ADR-0004: core is plain Python, desktop never touches Qt."""

import ast
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "src" / "kimai_tray"
FORBIDDEN = {
    "core": {"PySide6", "jeepney"},
    "desktop": {"PySide6"},
}


def imported_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            roots.add(node.module.split(".")[0])
    return roots


@pytest.mark.parametrize("layer", sorted(FORBIDDEN))
def test_layer_does_not_import_forbidden_packages(layer):
    offenders = [
        f"{path.relative_to(SRC)} imports {sorted(imported_roots(path) & FORBIDDEN[layer])}"
        for path in sorted((SRC / layer).rglob("*.py"))
        if imported_roots(path) & FORBIDDEN[layer]
    ]
    assert offenders == []


@pytest.mark.parametrize("layer", ["core", "desktop"])
def test_lower_layers_never_import_the_ui(layer):
    offenders = []
    for path in sorted((SRC / layer).rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                if module.startswith("kimai_tray.ui") or (node.level >= 2 and module.split(".")[0] == "ui"):
                    offenders.append(str(path.relative_to(SRC)))
    assert offenders == []
