from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from pydantic import BaseModel



@dataclass(frozen=True, slots=True)
class CompilationResult:
    project_id: str
    target_format: str
    output_path: Path


class CompilationService:

    def __init__(
        self,
        *,
        engine,
        execution_sessions,
        project_repository,
        # compiler_registry,
    ):
        self._engine = engine
        self._sessions = execution_sessions
        self._projects = project_repository
        # self._compilers = compiler_registry

    def compile(
        self,
        *,
        project_id: str,
        session_id: str,
        target_format: str = 'default',
    ):
        session = self._sessions.get(
            project_id=project_id,
            session_id=session_id,
        )

        if not session.execution_session.graph.solved:
            raise CompilationNotReadyError(
                "The execution session still has "
                "unresolved requirements."
            )
        if target_format == 'default':
            target_format = None
            
        target_format = target_format or session.execution_session.manifest.target_format

        # project = self._projects.get(project_id)
        # session = self._sessions.get(
        #     project_id=project_id,
        #     session_id=session_id
        # )

        # output_path = (
        #     session
        #     .execution_session
        #     .workspace
        #     .generated_path(
        #         extension=target_format
        #     )
        # )

        result = self._engine.compile(
            session=session.execution_session,
            target_format=target_format,
            # output_path = output_path
        )

        return CompilationResult(
            project_id=project_id,
            target_format=result.format_text,
            output_path=result.output_compiled
        )

    def get_artifact(
        self,
        *,
        project_id:str,
        filename: str
    ) -> CompilationArtifact:
        

        return None


    
class CompilationArtifact(BaseModel):
    path: str
    filename: str
    extension: str

class CompilationNotReadyError(Exception):
    pass


# class CompilationService:

#     def __init__(
#         self,
#         engine: DocumentEngine,
#         compiler_registry: Any,
#         recipe_repository: Any,
#         workspace: Any,
#     ) -> None:
#         self._engine = engine
#         self._compiler_registry = compiler_registry
#         self._recipe_repository = recipe_repository
#         self._workspace = workspace

#     def compile(
#         self,
#         project_id: str,
#         target_format: str,
#         variables: dict[str, Any] | None = None,
#     ) -> CompilationResult:

#         variables = variables or {}

#         recipe = self._recipe_repository.get(project_id)

#         markdown = self._engine.assemble_document(
#             recipe=recipe,
#             variables=variables,
#         )

#         compiler = self._compiler_registry.get(
#             target_format
#         )

#         output_directory = (
#             self._workspace.project_path(project_id)
#             / self._workspace.OUTPUT_DIRECTORY
#         )

#         output_directory.mkdir(
#             parents=True,
#             exist_ok=True,
#         )

#         output_path = (
#             output_directory
#             / f"document.{target_format}"
#         )

#         compiler.compile(
#             markdown,
#             output_path,
#         )

#         return CompilationResult(
#             project_id=project_id,
#             target_format=target_format,
#             output_path=output_path,
#         )
#     def get_artifact(
#         self,
#         project_id: str,
#         filename: str,
#     ) -> Path:
#         return self._workspace.artifact_path(
#             project_id,
#             filename,
#         )

# class CompilationService:

#     def __init__(
#         self,
#         *,
#         iteraction_repository,
#         recipe_repository,
#         engine,
#         # compiler_registry,
#         workspace,
#     ):
#         self._iteractions = (
#             iteraction_repository
#         )

#         self._recipes = (
#             recipe_repository
#         )

#         self._engine = engine
#         # self._compiler_registry = (
#         #     compiler_registry
#         # )

#         self._workspace = workspace

#     def compile(
#         self,
#         *,
#         project_id: str,
#         session_id: str,
#         target_format: str,
#     ):

#         session = (
#             self._iteractions.get(
#                 project_id,
#                 session_id,
#             )
#         )

#         if not session.is_ready():

#             raise CompilationNotReadyError(
#                 "Document still has unresolved "
#                 "variables or dependencies."
#             )

#         recipe = (
#             self._recipes.get(
#                 project_id
#             )
#         )

#         document = (
#             self._engine.assemble_document(
#                 recipe=recipe,
#                 variables=session.variables,
#             )
#         )

#         compiler = (
#             self.engine.compilation._compiler_registry.get(
#                 target_format
#             )
#         )

#         output_directory = (
#             self._workspace.output_path(
#                 project_id
#             )
#         )

#         output_directory.mkdir(
#             parents=True,
#             exist_ok=True,
#         )

#         output_path = (
#             output_directory
#             / f"document.{target_format}"
#         )

#         compiler.compile(
#             document,
#             output_path,
#         )

#         session.status = (
#             IteractionStatus.COMPLETED
#         )

#         self._iteractions.save(
#             session
#         )

#         return output_path  


# class DocumentCompiler(Protocol):

#     def compile(
#         self,
#         markdown: str,
#         output_path: Path,
#     ) -> Path:
#         ...


# class DocumentEngine(Protocol):

#     def assemble_document(
#         self,
#         recipe: Any,
#         variables: dict[str, Any],
#     ) -> str:
#         ...
