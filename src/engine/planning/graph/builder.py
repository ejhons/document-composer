from engine.common.exceptions import GraphNotSolvedException
from engine.frontend.manifests.recipe import RecipeManifest
from engine.solving.solving_context import SolvingContext
from engine.planning.graph.graph import RecipeGraph, SolvedGraph
from engine.planning.graph.component_node import ComponentNode
from engine.planning.loaders.base import ResourceResolver


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
        ) -> RecipeGraph:
        
        graph = RecipeGraph()
        for component in manifest.components:
            # Normaliza a localização do ComponentConfig
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

