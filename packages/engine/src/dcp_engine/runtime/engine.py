from dataclasses import dataclass, field
from enum import StrEnum
import logging
from xmlrpc.client import Boolean

from dcp_engine.pipeline.assembling import AssemblingModule
from dcp_engine.pipeline.compilation import CompilationModule
from dcp_engine.pipeline.planning import PlanningModule
from dcp_engine.pipeline.solving import SolvingModule
from dcp_engine.runtime.workspace import Workspace
from dcp_engine.language.manifests.recipe import RecipeManifest
from dcp_engine.runtime.execution.context import ExecutionContext
from dcp_engine.runtime.execution.session import ExecutionSession
from dcp_engine.solving.resolution.resolution_collector import PendingResolution

logger = logging.getLogger("doc_engine.cache")

class Engine:

    def __init__(
        self,
        planning: PlanningModule,
        solving: SolvingModule,
        assembling: AssemblingModule,
        compilation: CompilationModule,
    ):
        self.planning = planning
        self.solving = solving
        self.assembling = assembling
        self.compilation = compilation

    def create_session(
        self,
        workspace: Workspace,
        manifest: RecipeManifest,
        context: ExecutionContext | None = None,
    ) -> ExecutionSession:
        '''
        Creates a ExecutionSession object. 

        This object will be neccessary for trading informations through engine operations.
        '''
        session = ExecutionSession(
            manifest = manifest,
            execution_context = context,
            trace = [],
            workspace=workspace
        )

        return session

    def create_interaction(
        self,
        session: ExecutionSession
        ) -> IteractionResult:
        # Builds graph from RecipeManifest
        session = self.planning.execute(session)
        # Raises exception if not solved/finshed with dependencies
        result = self.solving.execute(session)

        
        if result.resolved:
            return IteractionResult.ready(
                session=result.session
            )

        return IteractionResult.needs_input(
            session=result.session,
            pending=result.pending,
        )

    
    def compile(
        self,
        session: ExecutionSession,
        output_path: str,
    ) -> CompilationResult:
        '''
        Only must be run when graph is completely solved.
        Otherwise raises GraphNotSolvedException.
        '''
        session = self.assembling.execute(session)
        session = self.compilation.execute(session, output_path)

        return None
    

class IteractionStatus(StrEnum):
    NEEDS_INPUT='needs_input'
    READY='ready'


@dataclass(frozen=True)
class IteractionResult:
    solved:IteractionStatus
    session: ExecutionSession
    pending: PendingResolution | None = None

    @classmethod
    def ready(cls, session):
        return cls(
            solved=IteractionStatus.READY,
            session=session
        )
    
    @classmethod
    def needs_input(
        cls,
        session,
        pending:PendingResolution#list[PendingResolution]=[]
    ):
        return cls(
            solved=IteractionStatus.NEEDS_INPUT,
            session=session,
            pending=pending
        )
    

@dataclass(frozen=True)
class CompilationResult:
    format_text: str
    output_compiled: str



# class Engine:
#     '''
#     Assume que execution plan já está pronto
#     Coordena o execução:
#     - manter o contexto de execução
#     - seleciona o compilador adequado
#     - Executa os Steps
#     - Armazena os resultados 
#     '''
#     def __init__(
#         self,
#         inspection_pipeline: InspectionPipeline,
#         plan_context: PlanningContext,
#         runtime: RuntimeResolver,
#         dependency: DependencyResolver,
#         pending: PendingCollector,
#         compiler_registry: CompilerRegistry,
#         adapter_registry: AdapterRegistry | None = None,
#         bootstrap:bool = False
#     ):
#         self.inspection_pipeline = inspection_pipeline
#         self.plan_context = plan_context
#         self.runtime = runtime
#         self.dependency = dependency
#         self.pending = pending
#         self.adapter_registry = adapter_registry or AdapterRegistry()
#         self.compiler_registry = compiler_registry

#         if bootstrap:
#             self._bootstrap_adapters()
#             self._bootstrap_compilers()
    
#     def _bootstrap_adapters(self):
#         """Initializes default system plugins for file format resolution."""
#         self.adapter_registry.register("xlsx", ExcelToMarkdownAdapter())
#         self.adapter_registry.register("pdf", PdfToImageMarkdownAdapter())
#         self.adapter_registry.register("docx", DocxPostCompileAdapter())
#         self.adapter_registry.register("mermaid", MermaidMarkdownAdapter(
#             self.cache
#         ))
#         self.adapter_registry.register("md", MarkdownAdapter(
#             jinja_env=self.jinja_env,
#             cache_manager=self.cache
#         ))

#     def _bootstrap_compilers(self):
#         """Initializes system plugins for compilation output formats."""
#         self.compiler_registry.register_compiler("docx", DocxCompilerAdapter())#(registry=self.registry))
#         self.compiler_registry.register_compiler("pdf", PdfCompilerAdapter(registry=self.adapter_registry))
#         self.compiler_registry.register_compiler("html", HtmlCompilerAdapter())#(registry=self.registry))

#     def create_session(
#         self,
#         manifest: RecipeManifest,
#         context: ExecutionContext
#     ) -> ExecutionSession:
#         '''
#         Creates a ExecutionSession object. 
#         This object will be neccessary for trading informations through engine operations.
#         '''
#         session = ExecutionSession(
#             # working_directory = '',
#             manifest = manifest,
#             # graph = graph,
#             execution_context = context,
#             trace = None
#         )
#         return session
    
#     def build_graph(
#         self,
#         session: ExecutionSession
#     ):
#         '''
#         Creates graph, neccessary for planning operations
#         '''
#         graph = RecipeGraphBuilder(
#             context=self.plan_context
#         ).build(
#             manifest=session.manifest
#         )
#         # Cria graph
#         session.graph = graph
        
        
#     def resolve(
#         self,
#         session: ExecutionSession,
#         repetitions: int = 25
#     ) -> EngineResult:
#         '''
#         Executes solving operation to components for variables and directives.
#         That operation is recursve and stops after capturing unchanged graphs during iteractions.
#         In case the given number of repetitions are not enough, raises ResolutionException indicating non-convergence.
#         '''
#         graph = session.graph
#         context = session.execution_context

#         for _ in range(repetitions):
#             self.inspection_pipeline.execute(
#                 graph,
#                 self.plan_context
#             )
#             # Verifica variáveis e trata os valores
#             for node in graph.nodes.values():
#                 self.runtime.resolve_node(node, context)
#             # Resolve dependências gerando nós
#             self.dependency.resolve(graph, self.plan_context)
#             # Captura as pendências remanescentes no grafo
#             pending = self.pending.collect(graph)

#             if pending.resolved or pending.unchanged:
#                 return EngineResult(
#                     completed=pending.resolved and pending.unchanged,
#                     graph=graph
#                 )        
#         raise ResolutionException(f'Timeout=[{repetitions}]. Planning did not converge.')
    
#     # def plan(
#     #         self, 
#     #         session: ExecutionSession,
#     #         scheduler: Scheduler
#     # ) -> ExecutionPlan:
#     #     return scheduler.schedule(session.graph)
    
#     def adapt(
#         self,
#         session: ExecutionSession
#     ):
#         graph = session.graph
#         for node in graph.nodes.values():
#             format_type = node.component.file_format
#             registry = self.adapter_registry.get(format_type)
            
#             if registry is None:
#                 continue

#             content = registry.convert(
#                 node=node, 
#                 context=self.plan_context,
#                 workspace=session.workspace
#             )
#             node.adapted = content

#     def fragment(
#         self,
#         session: ExecutionSession
#     ) -> list[FragmentedMarkdown]:
#         atomizer = MarkdownAtomizer()

#         graph = session.graph
#         node_fragment = {
#             node:atomizer.atomize(node.adapted.markdown)
#             for node in graph.nodes.values()
#         }

#         for node, parsed in node_fragment.items():
#             for i, block in enumerate(parsed.blocks):
#                 if not isinstance(block, MarkdownDirective):
#                     continue

#                 node_id = node.id
#                 dependencies = graph.get_dependency(node_id)

#                 index:int = block.directive.index
#                 dependency = [dep for dep in dependencies if (dep.origin == str(index))][0]

#                 parsed.blocks[i] = MarkdownPlaceholder(
#                     node_id=dependency.target_id
#                 )
#         return node_fragment.values

    # def compile(
    #         self,
    #         session: ExecutionSession,
    #         document_builder: DocumentIRBuilder
    # ) -> DocumentIR:
    #     # plan = scheduler.schedule(graph)
    #     document = document_builder.build(
    #         graph=session.graph,
    #         # plan=plan
    #     )
    #     return document
    
    # def parses(
    #         self,
    #         session: ExecutionSession,
    #         document: DocumentIR
    # ):
    #     parsed = document.assemble_document()  

    # def parse(
    #         self,
    #         session: ExecutionSession,
    #         document: DocumentIR
    # ):
    #     for block in document.flatten():
    #         type = block.type
    #         registry = self.adapter_registry.get(type)
    #         if registry is None:
    #             continue
    #         registry.convert(

    #         ) if component.file_format not in ["pdf", "image"]:
    #                     adapter = self.registry.get_adapter(component.file_format)
    #                     converted_content = adapter.convert(component.source, output_resource_dir)
    #                     assembled_segments.append(converted_content)
    #                     continue



    # def execute(
    #     self,
    #     session: ExecutionSession,
    #     plan: ExecutionPlan
    # ):
    #     context = session.execution_context
    #     for step in plan.steps:
    #         compiler = self.compiler_registry.get_compiler(
    #             step.node.component.file_format
    #         )
    #         if compiler:
    #             compiler.compile(step, context)
    #         step.completed = True

    #     return context
    


    # def assemble_document(
    #     self,
    #     user_inputs: Dict[str, Any],
    #     output_resource_dir: str
    # ) -> str:

    #     scheduler, final_order = self._build_execution_plan(user_inputs)

    #     self._execute_scheduler(
    #         scheduler=scheduler,
    #         output_resource_dir=output_resource_dir,
    #     )

    #     return self._assemble_output(
    #         scheduler,
    #         final_order,
    #     )

    # def assemble_document(
    #         self,
    #         user_inputs: Dict[str, Any],
    #         output_resource_dir: str
    #         ) -> str:
    #     """
    #     Orchestrates the dynamic document construction via an execution task stack.
    #     (Clean Architecture Entry Point)
    #     """
    #     scheduler = TaskScheduler()
        
    #     # 1. Carrega o manifesto inicial na pilha
    #     manifest_ordered_ids = self._load_manifest_tasks(scheduler, user_inputs)

    #     # 2. Consome a pilha até esvaziar (Máquina de Estados)
    #     while scheduler.has_tasks():
    #         current_task = scheduler.pop_task()
    #         if not current_task or current_task.is_completed:
    #             continue

    #         # Verifica se está travado por dependências dos filhos
    #         if self._is_task_blocked(current_task, scheduler):
    #             scheduler.stack.append(current_task)
    #             continue

    #         # Processa o ciclo de vida da tarefa atual
    #         self._execute_task_lifecycle(current_task, scheduler, output_resource_dir)

    #     # 3. Remonta as strings de forma linear e ordenada
    #     return "\n\n".join([scheduler.registry[comp_id].resolved_content for comp_id in manifest_ordered_ids])
