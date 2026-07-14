from engine.common.models.recipe import RecipeManifest
from engine.planner.planning_context import PlanningContext
from engine.planner.graph.graph import RecipeGraph
from engine.planner.graph.component_node import ComponentNode


class RecipeGraphBuilder():
    '''
    Build a graph from REcipe Manifest by Planning Context Definition.
    '''
    def __init__(self, context: PlanningContext):
        self.context = context

    def build(
            self,
            manifest: RecipeManifest
        ) -> RecipeGraph:
        
        graph = RecipeGraph()
        for component in manifest.components:
            # Normaliza a localização do ComponentConfig
            self.context.resource_resolver.resolve(component, component.source)
            # Nesse ponto, é garantido que a referência é absoluta.
            node = ComponentNode(component=component)
            graph.add_node(node)

        return graph


