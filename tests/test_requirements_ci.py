"""requirements-ci.in repeats every dependency of pyproject.toml (Dependabot compiles only that file)."""

import tomllib
from pathlib import Path

from packaging.requirements import Requirement

ROOT = Path(__file__).resolve().parents[1]


def _ci_inputs() -> dict[str, Requirement]:
    reqs = {}
    for line in (ROOT / "requirements-ci.in").read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            req = Requirement(line)
            reqs[req.name.lower()] = req
    return reqs


def _project_requirements() -> list[Requirement]:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    lines = list(project["dependencies"])
    for extra in ("dev", "ui"):
        lines += project["optional-dependencies"][extra]
    return [Requirement(line) for line in lines]


def test_ci_inputs_match_pyproject() -> None:
    ci = _ci_inputs()
    for req in _project_requirements():
        assert req.name.lower() in ci, f"{req.name} missing from requirements-ci.in"
        assert ci[req.name.lower()].specifier == req.specifier, (
            f"{req.name}: range differs from pyproject.toml"
        )


def test_build_backend_in_ci_inputs() -> None:
    build = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["build-system"]["requires"]
    ci = _ci_inputs()
    for line in build:
        assert Requirement(line).name.lower() in ci
