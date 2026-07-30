from engine.planning.graph.graph import RecipeGraph
from engine.solving.solving_context import SolvingContext
from engine.planning.graph.builder import RecipeGraphBuilder
from engine.runtime.context import EngineContext
from engine.runtime.execution.session import ExecutionSession


class PlanningModule:

    def __init__(
        self,
        context: EngineContext
    ):
        self.resource_resolver = context.resource_resolver

    
    def _build_graph(
        self,
        session: ExecutionSession
    ) -> RecipeGraph:
        '''
        Creates graph, neccessary for planning operations.
        '''
        graph = RecipeGraphBuilder(
            resource_resolver=self.resource_resolver
        ).build(
            manifest=session.manifest
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