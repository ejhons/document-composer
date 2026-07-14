# tests/conftest.py
from pathlib import Path

# Encontra todos os arquivos .py dentro de tests/fixtures/ (ignorando __init__.py)
fixtures_dir = Path(__file__).parent / "fixtures"
# print(fixtures_dir)
plugins = [
    f"tests.fixtures.{p.stem}"
    for p in fixtures_dir.glob("*.py")
    if p.stem != "__init__"
]

pytest_plugins = plugins


import pytest
from pathlib import Path



@pytest.fixture
def temp_workspace(tmp_path: Path) -> Path:
    """
    Cria um workspace temporário para cada teste.
    """
    return tmp_path


@pytest.fixture
def markdown_file(temp_workspace: Path):
    def _factory(name: str, content: str):

        path = temp_workspace / name
        path.write_text(content, encoding="utf8")

        return path

    return _factory

# pytest_plugins = [
#     "tests.fixtures.auth_fixtures",
#     "tests.fixtures.db_fixtures",
#     "tests.fixtures.markdown_fixtures",  # Exemplo de arquivo seu
# ]
