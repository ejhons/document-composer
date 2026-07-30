from dataclasses import dataclass

from engine.compilation.adapters.registry import AdapterRegistry
from engine.frontend.directives.registry import DirectiveRegistry
from engine.frontend.inspection.registry import StaticInspectorRegistry
from engine.planning.loaders.base import ResourceResolver

@dataclass
class SolvingContext:
    '''
    Planning context keeping every registry neccessary for planning step.
    In this step, resources, directives and components are solved making 
    RecipeGraph.
    '''
    adapter_registry: AdapterRegistry
    resource_resolver: ResourceResolver
    directive_registry: DirectiveRegistry
    inspector_registry: StaticInspectorRegistry