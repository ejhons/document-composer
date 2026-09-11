from dcp_engine.runtime.context import EngineContext
from dcp_engine.planning.graph.graph import RecipeGraph
from dcp_engine.planning.graph.builder import RecipeGraphBuilder
from dcp_engine.runtime.execution.session import ExecutionSession

from dcp_engine.runtime.logging.logger import logger




class PlanningModule:

    def __init__(
        self,
        context: EngineContext,
        builder_cls=RecipeGraphBuilder
    ):
        self.resource_resolver = context.resource_resolver
        self.builder_cls = builder_cls

    
    def _build_graph(
        self,
        session: ExecutionSession
    ) -> RecipeGraph:
        '''
        Creates graph, neccessary for planning operations.
        '''
        logger.info(f'building graph...')
        return self.builder_cls(
            resource_resolver=self.resource_resolver
        ).build(
            manifest=session.manifest,
            root=session.workspace.components_dir
        )
        
    def execute(
            self,
            session: ExecutionSession
        ) -> ExecutionSession:
        '''
        Transforms recipe manifest into graph object ready for solving.
        Updates session.graph
        '''
        session.graph = self._build_graph(session)
        logger.info('graph successfully build.')
        return session