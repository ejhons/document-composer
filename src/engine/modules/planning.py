from engine.planner.graph.graph import RecipeGraph
from engine.planner.planning_context import PlanningContext
from engine.planner.recipe_builder import RecipeGraphBuilder
from engine.runtime.context import EngineContext
from engine.runtime.execution.session import ExecutionSession


class PlanningModule:

    def __init__(
        self,
        context: EngineContext
        # resource_resolver
    ):
        self.resource_resolver = context.resource_resolver

    
    def _build_graph(
        self,
        session: ExecutionSession
    ) -> RecipeGraph:
        '''
        Creates graph, neccessary for planning operations.
        '''
        graph = RecipeGraphBuilder().build(
            manifest=session.manifest,
            resource_resolver=self.resource_resolver
        )
        # Creates graph
        session.graph = graph
        return graph

        
    def execute(
            self,
            session: ExecutionSession
        ) -> ExecutionSession:
        graph = self._build_graph(session)

        return session