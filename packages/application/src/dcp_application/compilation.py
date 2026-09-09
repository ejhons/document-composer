from __future__ import annotations

from pathlib import Path
from pydantic import BaseModel
from dataclasses import dataclass


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
    ):
        self._engine = engine
        self._sessions = execution_sessions
        self._projects = project_repository

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
                "The execution session still has unresolved requirements."
            )
        if target_format == 'default':
            target_format = None
            
        target_format = target_format or session.execution_session.manifest.target_format

        result = self._engine.compile(
            session=session.execution_session,
            target_format=target_format,
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
