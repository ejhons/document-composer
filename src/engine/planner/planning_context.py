from dataclasses import dataclass

from engine.backend.adapters.registry import AdapterRegistry
from engine.frontend.directives.registry import DirectiveRegistry
from engine.frontend.inspectors.registry import StaticInspectorRegistry
from engine.planner.resources.base import ResourceResolver

@dataclass
class PlanningContext:
    '''
    Planning context keeping every registry neccessary for planning step.
    In this step, resources, directives and components are solved making 
    RecipeGraph.
    '''
    adapter_registry: AdapterRegistry
    resource_resolver: ResourceResolver
    directive_registry: DirectiveRegistry
    inspector_registry: StaticInspectorRegistry