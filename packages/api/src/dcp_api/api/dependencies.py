from pathlib import Path
from fastapi import Request
from dataclasses import dataclass

from dcp_engine import Engine, EngineBuilder, ManifestLoader
from dcp_api.application.compilation import CompilationService
from dcp_api.application.files import FileRepository, FileService
from dcp_api.application.iteraction import ExecutionSessionRepository, IteractionService
from dcp_api.application.projects import ProjectRepository, ProjectService
from dcp_api.application.recipes import RecipeRepository, RecipeService
from dcp_api.infrastructure.filesystem.sessions_repository import FileExecutionSessionRepository

from dcp_api.infrastructure.filesystem.file_repository import (
    FilesystemFileRepository,
)
# from dcp_api.infrastructure.filesystem._iteraction_repository import FilesystemIteractionRepository
from dcp_api.infrastructure.filesystem.project_repository import (
    FilesystemProjectRepository,
)
from dcp_api.infrastructure.filesystem.recipe_repository import (
    FilesystemRecipeRepository,
)
from dcp_api.infrastructure.filesystem.workspace import WorkspaceEntity





def get_project_service(request: Request) -> ProjectService:
    return request.app.state.container.project_service


def get_file_service(request: Request) -> FileService:
    return request.app.state.container.file_service


def get_recipe_service(request: Request) -> RecipeService:
    return request.app.state.container.recipe_service

def get_iteraction_service(request: Request) -> IteractionService:
    return request.app.state.container.iteraction_service

def get_compilation_service(request: Request) -> CompilationService:
    return request.app.state.container.compilation_service




@dataclass(slots=True)
class ApplicationContainer:
    workspace: WorkspaceEntity
    engine: Engine
    recipe_loader: ManifestLoader

    project_repository: ProjectRepository
    file_repository: FileRepository
    recipe_repository: RecipeRepository
    sessions_repository: ExecutionSessionRepository
    # iteraction_repository: IteractionRepository

    project_service: ProjectService
    file_service: FileService
    recipe_service: RecipeService
    iteraction_service: IteractionService
    compilation_service: CompilationService


def create_container() -> ApplicationContainer:
    WORKSPACE_ROOT = Path("workspace")
    workspace = WorkspaceEntity(WORKSPACE_ROOT)
    workspace.initialize()

    # Call default() method for using default scenario
    builder: EngineBuilder = EngineBuilder.default()
    # Builds engine by calling build() method
    engine: Engine = builder.build()
    recipe_loader: ManifestLoader = ManifestLoader()


    # ---------------------------------------------------------
    # Repositories
    # ---------------------------------------------------------
    project_repository = FilesystemProjectRepository(workspace)
    file_repository = FilesystemFileRepository(workspace)
    recipe_repository = FilesystemRecipeRepository(workspace)
    # iteraction_repository = FilesystemIteractionRepository(workspace)
    sessions_repository = FileExecutionSessionRepository(workspace.root)

    project_service = ProjectService(project_repository)
    file_service = FileService(file_repository)
    recipe_service = RecipeService(recipe_repository)


    # ---------------------------------------------------------
    # Application services
    # ---------------------------------------------------------
    iteraction_service = IteractionService(
        engine=engine,
        execution_sessions=sessions_repository,
        project_repository=project_repository
    )

    compilation_service = CompilationService(
        engine=engine,
        execution_sessions=sessions_repository,
        project_repository=project_repository,
        # iteraction_repository=iteraction_repository,
        # recipe_repository=recipe_repository,
        
        # engine=engine,
        # workspace=workspace,
    )

    return ApplicationContainer(
        workspace=workspace,
        engine=engine,
        recipe_loader=recipe_loader,
        recipe_repository=recipe_repository,
        file_repository=file_repository,
        project_repository=project_repository,
        # iteraction_repository=iteraction_repository,
        sessions_repository=sessions_repository,
        project_service=project_service,
        recipe_service=recipe_service,
        file_service=file_service,
        iteraction_service=iteraction_service,
        compilation_service=compilation_service,
    )


# def create_container() -> ApplicationContainer:
#     workspace = WorkspaceEntity(Path("workspace"))
#     workspace.initialize()

#     # Call default() method for using default scenario
#     builder: EngineBuilder = EngineBuilder.default()
#     # Builds engine by calling build() method
#     engine: Engine = builder.build()


#     recipe_repository = (
#         FilesystemRecipeRepository(
#             workspace
#         )
#     )


#     iteraction_repository = (
#         FilesystemIteractionRepository(
#             workspace
#         )
#     )


#     iteraction_service = IteractionService(
#         repository=iteraction_repository,
#         engine=engine,
#         recipe_repository=recipe_repository,
#     )


#     compilation_service = CompilationService(
#         iteraction_repository=iteraction_repository,
#         recipe_repository=recipe_repository,
#         engine=engine,
#         compiler_registry=compiler_registry,
#         workspace=workspace,
#     )


#     return ApplicationContainer(
#         workspace=workspace,
#         engine=engine,
#         recipe_repository=recipe_repository,
#         iteraction_repository=iteraction_repository,
#         iteraction_service=iteraction_service,
#         compilation_service=compilation_service,
#     )

# from pathlib import Path
# from dcp_engine.runtime.workspace import Workspace
# from dcp_api.application.projects import ProjectService
# from dcp_api.infrastructure.filesystem.project_repository import FilesystemProjectRepository

# def start_application():
#     workspace = Workspace(
#         root=Path("workspace")
#     )

#     workspace.initialize()

#     project_repository = FilesystemProjectRepository(
#         workspace=workspace
#     )

#     project_service = ProjectService(
#         repository=project_repository
#     )