import tomllib
from pathlib import Path

from packaging.requirements import Requirement

PACKAGES = Path(__file__).resolve().parents[1] / "packages"


def _deps(member: str) -> set[str]:
    data = tomllib.loads((PACKAGES / member / "pyproject.toml").read_text())
    return {Requirement(d).name.lower() for d in data["project"]["dependencies"]}


def test_cli_declara_dependencias_embutidas():
    # ignora dependências entre membros do próprio workspace
    internas = {"dcp-engine", "dcp-application", "dcp-cli"}
    exigidas = (_deps("dcp-engine") | _deps("dcp-application")) - internas
    faltando = exigidas - _deps("dcp-cli")
    assert not faltando, f"Declare em dcp-cli: {sorted(faltando)}"