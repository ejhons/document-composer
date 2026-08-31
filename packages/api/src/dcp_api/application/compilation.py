from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol


class DocumentCompiler(Protocol):

    def compile(
        self,
        markdown: str,
        output_path: Path,
    ) -> Path:
        ...


class DocumentEngine(Protocol):

    def assemble_document(
        self,
        recipe: Any,
        variables: dict[str, Any],
    ) -> str:
        ...


@dataclass(frozen=True, slots=True)
class CompilationResult:
    project_id: str
    target_format: str
    output_path: Path


class CompilationService:

    def __init__(
        self,
        engine: DocumentEngine,
        compiler_registry: Any,
        recipe_repository: Any,
        workspace: Any,
    ) -> None:
        self._engine = engine
        self._compiler_registry = compiler_registry
        self._recipe_repository = recipe_repository
        self._workspace = workspace

    def compile(
        self,
        project_id: str,
        target_format: str,
        variables: dict[str, Any] | None = None,
    ) -> CompilationResult:

        variables = variables or {}

        recipe = self._recipe_repository.get(project_id)

        markdown = self._engine.assemble_document(
            recipe=recipe,
            variables=variables,
        )

        compiler = self._compiler_registry.get(
            target_format
        )

        output_directory = (
            self._workspace.project_path(project_id)
            / self._workspace.OUTPUT_DIRECTORY
        )

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = (
            output_directory
            / f"document.{target_format}"
        )

        compiler.compile(
            markdown,
            output_path,
        )

        return CompilationResult(
            project_id=project_id,
            target_format=target_format,
            output_path=output_path,
        )