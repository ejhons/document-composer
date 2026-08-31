from __future__ import annotations

from pathlib import Path

from dcp_api.application.files import FileRepository
from dcp_api.infrastructure.filesystem.project_repository import (
    ProjectNotFoundError,
)
from dcp_api.infrastructure.filesystem.workspace import Workspace


class FilesystemFileRepository(FileRepository):

    def __init__(self, workspace: Workspace) -> None:
        self._workspace = workspace

    def list(self, project_id: str) -> list[Path]:
        components = self._components_path(project_id)

        if not components.is_dir():
            raise ProjectNotFoundError(project_id)

        return sorted(
            path
            for path in components.rglob("*")
            if path.is_file()
        )

    def save(
        self,
        project_id: str,
        filename: str,
        content: bytes,
    ) -> Path:
        components = self._components_path(project_id)

        if not components.is_dir():
            print(components)
            raise ProjectNotFoundError(project_id)

        target = components / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)

        return target

    def read(
        self,
        project_id: str,
        filename: str,
    ) -> bytes:
        target = self._file_path(project_id, filename)

        if not target.is_file():
            raise FileNotFoundError(filename)

        return target.read_bytes()

    def delete(
        self,
        project_id: str,
        filename: str,
    ) -> None:
        target = self._file_path(project_id, filename)

        if not target.is_file():
            raise FileNotFoundError(filename)

        target.unlink()

    def _components_path(self, project_id: str) -> Path:
        project = self._workspace.project_path(project_id)

        if not project.is_dir():
            raise ProjectNotFoundError(project_id)

        return project / self._workspace.COMPONENTS_PROJECTS_DIRECTORY

    def _file_path(
        self,
        project_id: str,
        filename: str,
    ) -> Path:
        return self._components_path(project_id) / filename