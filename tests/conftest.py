# tests/conftest.py
from pathlib import Path

from build.lib.engine.execution.engine import Engine
from engine.compilation.adapters.registry import AdapterRegistry
from engine.compilation.compilers.registry import CompilerRegistry
from engine.runtime.workspace import Workspace
from engine.frontend.directives.registry import DirectiveRegistry
from engine.solving.inspection.pipeline import InspectionPipeline
from engine.solving.inspection.registry import StaticInspectorRegistry
from engine.frontend.parser import MarkdownParser
from engine.frontend.syntax.expressions.parser import ExpressionParser
from engine.solving.solving_context import SolvingContext
from engine.solving.resolution.dependency_resolver import DependencyResolver
from engine.solving.resolution.resolution_collector import PendingCollector
from engine.solving.resolution.runtime_resolver import RuntimeResolver
from engine.planning.loaders.resource_resolver import LocalResourceResolver
from engine.runtime.context import EngineContext

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
def engine_context():
    return EngineContext(resource_resolver=LocalResourceResolver())

@pytest.fixture
def temp_workspace(tmp_path: Path) -> Path:
    """
    Cria um workspace temporário para cada teste.
    """
    return tmp_path

@pytest.fixture
def temp_workspace_object(temp_workspace) -> Path:
    """
    Cria um workspace temporário para cada teste.
    """
    return Workspace(root=temp_workspace)


@pytest.fixture
def markdown_file(temp_workspace: Path):
    def _factory(name: str, content: str):

        path = temp_workspace / name
        path.write_text(content, encoding="utf8")

        return path

    return _factory

@pytest.fixture
def engine():
    engine = Engine(
        inspection_pipeline=InspectionPipeline(),
        plan_context=SolvingContext(
            resource_resolver = LocalResourceResolver(),
            directive_registry=DirectiveRegistry(),
            inspector_registry=StaticInspectorRegistry()
        ),
        runtime=RuntimeResolver(),
        dependency=DependencyResolver(
            markdown_parser=MarkdownParser(
                expression_parser=ExpressionParser()
            )
        ),
        pending=PendingCollector(),
        compiler_registry=CompilerRegistry(),
        adapter_registry=AdapterRegistry(),
        bootstrap=True # Inicializa Adapter e Compiler Resgitries
    )

# pytest_plugins = [
#     "tests.fixtures.auth_fixtures",
#     "tests.fixtures.db_fixtures",
#     "tests.fixtures.markdown_fixtures",  # Exemplo de arquivo seu
# ]
