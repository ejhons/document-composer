from dcp_engine.common.exceptions import GraphNotSolvedException, ResolutionException
from dcp_engine.solving.solving_context import SolvingContext
from dcp_engine.runtime.context import EngineContext
from dcp_engine.runtime.result import SolvingResult
from dcp_engine.runtime.execution.session import ExecutionSession


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
        # self.adapter_registry = context.adapter_registry
        # self.inspector_registry = context.inspector_registry
        self.inspection_pipeline = context.inspection_pipeline
        self.solve_context = SolvingContext(
            resource_resolver=context.resource_resolver,
            adapter_registry=context.adapter_registry,
            directive_registry=context.directive_registry,
            inspector_registry=context.inspector_registry
        )

    def execute(
        self,
        session:ExecutionSession
    ) -> SolvingResult:
        '''
        Solves variables, dependencies and referencies.
        
        If solving proccess can't be executed, raises GraphNotSolvedExeception.
        '''
        result = self._resolve(session)
        if result.completed:
            self._adapt(session)
            # raise GraphNotSolvedException('Graph not solved yet')

        return result#session

    def _resolve(
        self,
        session: ExecutionSession
    ) -> SolvingResult:        
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
                self.solve_context.inspector_registry
            )
            # Verifica variáveis e trata os valores
            # for node in graph.nodes.values():
            #     self.runtime.resolve(node, context)
            self.runtime.resolve(graph, context)
            # Resolve dependências gerando nós
            self.dependency.resolve(graph, self.solve_context)
            # Captura as pendências remanescentes no grafo
            pending = self.pending.collect(graph)

            if pending.resolved and pending.unchanged:
                return SolvingResult(
                    completed=pending.resolved and pending.unchanged,
                    graph=graph
                )
        
        # if pending is not None:
        return SolvingResult(
            completed=False,
            graph=graph,
            pending=pending#pending.pending_inputs if pending is not None else set()
        )
               
        # raise ResolutionException(f'Timeout=[{self.max_loops}]. Planning did not converge.')

    
    def _adapt(
        self,
        session: ExecutionSession
    ):
        graph = session.graph
        for node in graph.nodes.values():
            format_type = node.component.file_format
            registry = self.solve_context.adapter_registry.get(format_type)
            
            if registry is None:
                continue

            content = registry.convert(
                node=node, 
                # context=self.plan_context,
                workspace=session.workspace
            )
            node.adapted = content
    
