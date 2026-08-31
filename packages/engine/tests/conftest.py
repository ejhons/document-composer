# tests/conftest.py

import importlib

import pytest
from pathlib import Path

from dcp_engine.compilation.adapters.registry import AdapterRegistry
from dcp_engine.compilation.compilers.registry import CompilerRegistry
from dcp_engine.language.directives.registry import DirectiveRegistry
from dcp_engine.language.parser import MarkdownParser
from dcp_engine.language.syntax.expressions.parser import ExpressionParser
from dcp_engine.planning.loaders.resource_resolver import LocalResourceResolver
from dcp_engine.planning.resolution.dependency_resolver import DependencyResolver
from dcp_engine.planning.resolution.runtime_resolver import RuntimeResolver
from dcp_engine.runtime.context import EngineContext
from dcp_engine.runtime.engine import Engine
from dcp_engine.runtime.workspace import Workspace
from dcp_engine.solving.inspection.pipeline import InspectionPipeline
from dcp_engine.solving.inspection.registry import StaticInspectorRegistry
from dcp_engine.solving.resolution.resolution_collector import PendingCollector
from dcp_engine.solving.solving_context import SolvingContext

# # Encontra todos os arquivos .py dentro de tests/fixtures/ (ignorando __init__.py)
# fixtures_dir = Path(__file__).parent / "fixtures"
# # print(fixtures_dir)
# plugins = [
#     f"tests.fixtures.{p.stem}"
#     for p in fixtures_dir.glob("*.py")
#     if p.stem != "__init__"
# ]

# pytest_plugins = plugins
fixtures_dir = Path(__file__).parent / "fixtures"

for p in fixtures_dir.glob("*.py"):
    if p.stem == "__init__":
        continue
    
    # Cria uma especificação de módulo a partir do caminho do arquivo
    spec = importlib.util.spec_from_file_location(p.stem, p)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Injeta as fixtures diretamente no namespace do conftest atual
    globals().update({
        name: getattr(module, name) 
        for name in dir(module) 
        if not name.startswith("_")
    })

    
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
    return engine

# pytest_plugins = [
#     "tests.fixtures.auth_fixtures",
#     "tests.fixtures.db_fixtures",
#     "tests.fixtures.markdown_fixtures",  # Exemplo de arquivo seu
# ]
