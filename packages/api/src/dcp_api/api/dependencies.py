from pathlib import Path

from dcp_api.application.files import FileService
from dcp_api.application.projects import ProjectService
from dcp_api.application.recipes import RecipeService

from dcp_api.infrastructure.filesystem.file_repository import (
    FilesystemFileRepository,
)
from dcp_api.infrastructure.filesystem.project_repository import (
    FilesystemProjectRepository,
)
from dcp_api.infrastructure.filesystem.recipe_repository import (
    FilesystemRecipeRepository,
)
from dcp_api.infrastructure.filesystem.workspace import Workspace


WORKSPACE_ROOT = Path("workspace")


workspace = Workspace(WORKSPACE_ROOT)
workspace.initialize()

project_repository = FilesystemProjectRepository(workspace)
file_repository = FilesystemFileRepository(workspace)
recipe_repository = FilesystemRecipeRepository(workspace)
project_service = ProjectService(project_repository)
file_service = FileService(file_repository)
recipe_service = RecipeService(recipe_repository)


def get_project_service() -> ProjectService:
    return project_service


def get_file_service() -> FileService:
    return file_service


def get_recipe_service() -> RecipeService:
    return recipe_service

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