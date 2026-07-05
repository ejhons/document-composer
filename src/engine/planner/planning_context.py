from dataclasses import dataclass

from engine.frontend.directives.registry import DirectiveRegistry
from engine.frontend.inspectors.registry import StaticInspectorRegistry
from engine.planner.resources.resource_resolver import LocalResourceResolver

@dataclass
class PlanningContext:
    resource_resolver: LocalResourceResolver
    directive_registry: DirectiveRegistry
    inspector_registry: StaticInspectorRegistry