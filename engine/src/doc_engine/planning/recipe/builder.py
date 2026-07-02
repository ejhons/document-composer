from engine.src.doc_engine.models.recipe import RecipeManifest
from engine.src.doc_engine.planning.recipe.recipe_graph import RecipeGraph
from engine.src.doc_engine.planning.recipe.component_node import ComponentNode


class RecipeGraphBuilder():
    def build(self, manifest: RecipeManifest) -> RecipeGraph:
        graph = RecipeGraph()
        for component in manifest.components:
            node = ComponentNode(component=component)
            graph.add_node(node)

        return graph


