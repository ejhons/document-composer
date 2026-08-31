from dataclasses import dataclass

from dcp_engine.compilation.adapters.registry import AdapterRegistry
from dcp_engine.language.directives.registry import DirectiveRegistry
from dcp_engine.planning.loaders.base import ResourceResolver
from dcp_engine.solving.inspection.registry import StaticInspectorRegistry

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