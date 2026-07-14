from dataclasses import dataclass

from engine.frontend.directives.registry import DirectiveRegistry
from engine.frontend.inspectors.registry import StaticInspectorRegistry
from engine.planner.resources.resource_resolver import LocalResourceResolver

@dataclass
class PlanningContext:
    '''
    Planning context keeping every registry neccessary for planning step.
    In this step, resources, directives and components are solved making 
    RecipeGraph.
    '''
    resource_resolver: LocalResourceResolver
    directive_registry: DirectiveRegistry
    inspector_registry: StaticInspectorRegistry