import pytest
from engine.frontend.directives.implementations.include_directive import IncludeDirectiveHandler
from engine.frontend.directives.registry import DirectiveRegistry
from engine.frontend.inspectors.implementations.inspector import MarkdownInspector
from engine.frontend.inspectors.registry import StaticInspectorRegistry
from engine.planner.planning_context import PlanningContext
from engine.planner.resources.resource_resolver import LocalResourceResolver


@pytest.fixture
def planning_context():
    resource_resolver=LocalResourceResolver()
    directive_registry=DirectiveRegistry()
    inspector_registry=StaticInspectorRegistry()
    

    inspector_registry.register(
        "md",
        MarkdownInspector()
    )
    directive_registry.register(
        IncludeDirectiveHandler()
    )

    return PlanningContext(
        resource_resolver=resource_resolver,
        directive_registry=directive_registry,
        inspector_registry=inspector_registry
    )