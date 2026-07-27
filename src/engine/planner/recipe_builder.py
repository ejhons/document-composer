from engine.common.exceptions import GraphNotSolvedException
from engine.common.models.recipe import RecipeManifest
from engine.planner.planning_context import PlanningContext
from engine.planner.graph.graph import RecipeGraph, SolvedGraph
from engine.planner.graph.component_node import ComponentNode
from engine.planner.resources.base import ResourceResolver


class RecipeGraphBuilder():
    '''
    Build a graph from REcipe Manifest by Planning Context Definition.
    '''
    def __init__(
            self,
            resource_resolver: ResourceResolver
        ):
        self.resource_resolver = resource_resolver


    def build(
            self,
            manifest: RecipeManifest,
            # resource_resolver: ResourceResolver
        ) -> RecipeGraph:
        
        graph = RecipeGraph()
        for component in manifest.components:
            # Normaliza a localização do ComponentConfig
            # self.context.
            self.resource_resolver.resolve(component, component.source)
            # Nesse ponto, é garantido que a referência é absoluta.
            node = ComponentNode(component=component)
            graph.add_node(node)

        return graph
    
    def build_solved(
        self,
        recipe_graph: RecipeGraph
    ) -> SolvedGraph:
        if not recipe_graph.solved:
            raise GraphNotSolvedException('graph still have pending nodes')
        
        # Cria uma nova instância de SolvedGraph com os dados do Graph
        return SolvedGraph.model_validate(recipe_graph.model_dump())

