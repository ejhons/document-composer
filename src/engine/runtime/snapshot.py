from engine.planner.graph.graph import RecipeGraph


class ExecutionSnapshot():
    graph: RecipeGraph

    def __init__(
            self,
            graph: RecipeGraph
    ):
        # Cria uma cópia desvingulada ao orginal
        self.graph = graph.model_copy(deep=True)