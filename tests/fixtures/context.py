import pytest
from engine.compilation.adapters.registry import AdapterRegistry
from engine.frontend.directives.implementations.include_directive import IncludeDirectiveHandler
from engine.frontend.directives.registry import DirectiveRegistry
from engine.solving.inspection.implementations.markdown_inspector import MarkdownInspector
from engine.solving.inspection.registry import StaticInspectorRegistry
from engine.solving.solving_context import SolvingContext
from engine.planning.loaders.resource_resolver import LocalResourceResolver


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