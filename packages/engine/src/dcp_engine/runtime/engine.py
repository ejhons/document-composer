from enum import StrEnum
from pathlib import Path
from dataclasses import dataclass

from dcp_engine.runtime.logging.log import logger
from dcp_engine.runtime.workspace import Workspace
from dcp_engine.pipeline.solving import SolvingModule
from dcp_engine.compilation.result import CompilationResult
from dcp_engine.pipeline.planning import PlanningModule
from dcp_engine.pipeline.assembling import AssemblingModule
from dcp_engine.pipeline.compilation import CompilationModule
from dcp_engine.language.syntax.fields import InputDefinition
from dcp_engine.language.manifests.recipe import RecipeManifest
from dcp_engine.runtime.execution.context import ExecutionContext
from dcp_engine.runtime.execution.session import ExecutionSession
from dcp_engine.solving.resolution.resolution_collector import PendingResolution


class Engine:
    def __init__(
        self,
        planning: PlanningModule,
        solving: SolvingModule,
        assembling: AssemblingModule,
        compilation: CompilationModule,
        # manifest_loader: ManifestLoader | None = None,
    ):
        self.planning = planning
        self.solving = solving
        self.assembling = assembling
        self.compilation = compilation
        # self._manifest_loader = manifest_loader or ManifestLoader()

        
    def init_workspace(
            self,
            root: str | Path
    ) -> Workspace:
        '''
        Creates ExecutionSession and saves it in Repository.
        '''
        if isinstance(root, str):
            root = Path(root)
        
        workspace = Workspace(root=root)
        # Starts workspace creating neccessary folder for project.
        workspace.init()

        return workspace


    def create_session(
        self,
        workspace: Workspace | str | Path,
        *,
        manifest: RecipeManifest | None = None,
        context: ExecutionContext | None = None
    ) -> ExecutionSession:
        '''
        Creates a ExecutionSession object. 
        This object will be neccessary for trading informations through engine operations.
        '''
        if isinstance(workspace, (str, Path)):
            workspace = Workspace(root=Path(workspace))

        session = ExecutionSession(
            workspace=workspace,
            manifest = manifest or workspace.load_recipe(),
            trace = [],
        )
        logger.info(f'Session created: {session.id}')

        if context is not None:
            session.context = context

        return session


    def create_interaction(
        self,
        session: ExecutionSession
    ) -> IteractionResult:
        '''
        Creates a interaction responsable for 
        building graph and solving variables and dependencies.
        '''
        
        # Builds graph from RecipeManifest
        session = self.planning.execute(session)

        # Raises exception if not solved/finshed with dependencies
        result = self.solving.execute(session)
        print(result.pending)
        # for node in session.graph.nodes.values():
        #     if node.inspection and node.inspection.fields:
        #         print(list(node.inspection.fields.values()))
        
        if result.completed:
            return IteractionResult.ready(
                session=session
            )

        return IteractionResult.needs_input(
            session=session,
            pending=result.pending
        )

    
    def compile(
        self,
        session: ExecutionSession,
        target_format: str
    ) -> CompilationResult:
        '''
        Only must be run when graph is completely solved.
        Otherwise raises GraphNotSolvedException.
        '''
        session = self.assembling.execute(
            session=session
        )        
        session = self.compilation.execute(
            session=session,
            target_format=target_format,
        )

        return CompilationResult(
            format_text=target_format,
            output_compiled=self.compilation.last_generated_file
        )
    

class IteractionStatus(StrEnum):
    NEEDS_INPUT='needs_input'
    READY='ready'


@dataclass(frozen=True)
class IteractionResult:
    status:IteractionStatus
    session: ExecutionSession
    pending: PendingResolution | None = None

    @property
    def is_solved(self):
        return self.status is IteractionStatus.READY

    @property
    def pending_inputs(self) -> list[InputDefinition]:
        if self.pending is None:
            return []
        return list(self.pending.pending_input_definitions.values())

    @property
    def pending_dependencies(self) -> set[str]:
        if self.pending is None:
            return set()
        return self.pending.pending_dependencies


    @classmethod
    def ready(cls, session):
        return cls(
            status=IteractionStatus.READY,
            session=session
        )
    
    @classmethod
    def needs_input(
        cls,
        session,
        pending:PendingResolution
    ):
        return cls(
            status=IteractionStatus.NEEDS_INPUT,
            session=session,
            pending=pending
        )
    
