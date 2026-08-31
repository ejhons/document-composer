from warnings import deprecated

from dcp_engine.planning.graph.graph import RecipeGraph


@deprecated('Unused')
class ExecutionSnapshot():
    graph: RecipeGraph

    def __init__(
            self,
            graph: RecipeGraph
    ):
        # Cria uma cópia desvingulada ao orginal
        self.graph = graph.model_copy(deep=True)