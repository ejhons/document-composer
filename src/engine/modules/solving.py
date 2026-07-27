from build.lib.engine.execution.resolver import RuntimeResolver
from engine.backend.adapters.registry import AdapterRegistry
from engine.common.exceptions import GraphNotSolvedException, ResolutionException
from engine.frontend.inspection_pipeline import InspectionPipeline
from engine.planner.graph.component_node import Dependency
from engine.planner.resolution.dependency_resolver import DependencyResolver
from engine.runtime.context import EngineContext
from engine.runtime.execution.result import EngineResult
from engine.runtime.execution.session import ExecutionSession


class SolvingModule:

    def __init__(
        self,
        context: EngineContext,
        # runtime_resolver: RuntimeResolver,
        # dependency_resolver: DependencyResolver,
        # pending_collector,
        # inspector_registry,
        # adapter_registry:AdapterRegistry,
        # inspection_pipeline:InspectionPipeline,
        max_loops: int = 25
    ):
        self.runtime = context.runtime_resolver
        self.dependency = context.dependency_resolver
        self.pending = context.pending_collector
        self.max_loops = max_loops

        # self.directive_registry = directive_registry
        self.adapter_registry = context.adapter_registry
        self.inspector_registry = context.inspector_registry
        self.inspection_pipeline = context.nspection_pipeline

    def execute(
        self,
        session:ExecutionSession
    ) -> ExecutionSession:
        '''
        Solves variables, dependencies and referencies.
        
        If solving proccess can't be executed, raises GraphNotSolvedExeception.
        '''
        result = self._resolve(session)
        if not result.completed:
            raise GraphNotSolvedException('Graph not solved yet')

        self._adapt(session)
        return session

    def _resolve(
        self,
        session: ExecutionSession
    ) -> EngineResult:        
        '''
        Executes solving operation to components for variables and directives.

        That operation is recursve and stops after capturing unchanged graphs during iteractions.
        In case the given number of repetitions are not enough, raises ResolutionException indicating non-convergence.
        '''
        graph = session.graph
        context = session.execution_context

        for _ in range(self.max_loops):
            self.inspection_pipeline.execute(
                graph,
                self.inspector_registry
            )
            # Verifica variáveis e trata os valores
            for node in graph.nodes.values():
                self.runtime.resolve(node, context)
            # Resolve dependências gerando nós
            self.dependency.resolve(graph, self.plan_context)
            # Captura as pendências remanescentes no grafo
            pending = self.pending.collect(graph)

            if pending.resolved or pending.unchanged:
                return EngineResult(
                    completed=pending.resolved and pending.unchanged,
                    graph=graph
                )        
        raise ResolutionException(f'Timeout=[{self.max_loops}]. Planning did not converge.')

    
    def _adapt(
        self,
        session: ExecutionSession
    ):
        graph = session.graph
        for node in graph.nodes.values():
            format_type = node.component.file_format
            registry = self.adapter_registry.get(format_type)
            
            if registry is None:
                continue

            content = registry.convert(
                node=node, 
                # context=self.plan_context,
                workspace=session.workspace
            )
            node.adapted = content
    
