import pytest

from dcp_engine.compilation.adapters.registry import AdapterRegistry
from dcp_engine.language.directives.implementations.include_directive import IncludeDirectiveHandler
from dcp_engine.language.directives.registry import DirectiveRegistry
from dcp_engine.planning.loaders.resource_resolver import LocalResourceResolver
from dcp_engine.solving.inspection.implementations.markdown_inspector import MarkdownInspector
from dcp_engine.solving.inspection.registry import StaticInspectorRegistry
from dcp_engine.solving.solving_context import SolvingContext


@pytest.fixture
def planning_context():
    resource_resolver=LocalResourceResolver()
    adapter_registry = AdapterRegistry()
    directive_registry=DirectiveRegistry()
    inspector_registry=StaticInspectorRegistry()
    

    inspector_registry.register(
        "md",
        MarkdownInspector()
    )
    directive_registry.register(
        IncludeDirectiveHandler()
    )

    return SolvingContext(
        adapter_registry=adapter_registry,
        resource_resolver=resource_resolver,
        directive_registry=directive_registry,
        inspector_registry=inspector_registry
    )