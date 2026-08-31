from __future__ import annotations

import json
import re
import shutil

from dcp_api.domain.project import Project
from dcp_api.application.projects import ProjectRepository
from dcp_api.infrastructure.filesystem.workspace import Workspace


class FilesystemProjectRepository(ProjectRepository):
    """
    Implementação do ProjectRepository baseada no filesystem.
    """
    PROJECT_METADATA = "project.json"

    def __init__(self, workspace: Workspace) -> None:
        self._workspace = workspace

    def create(self, name: str) -> Project:
        project_id = self._generate_id(name)
        project_path = self._workspace.initialize_project(project_id)

        project = Project(
            id=project_id,
            name=name,
            path=project_path,
        )
        self._write_metadata(project)

        return project

    def list(self) -> list[Project]:
        self._workspace.initialize()

        projects: list[Project] = []

        for path in sorted(self._workspace.projects.iterdir()):
            if not path.is_dir():
                continue

            try:
                projects.append(self._read_metadata(path))
            except InvalidProjectError:
                continue
            # projects.append(
            #     Project(
            #         id=path.name,
            #         name=self._display_name(path.name),
            #         path=path,
            #     )
            # )

        return projects

    def get(self, project_id: str) -> Project:
        project_path = self._workspace.project_path(project_id)

        if not project_path.is_dir():
            raise ProjectNotFoundError(project_id)

        return self._read_metadata(project_path)
        # return Project(
        #     id=project_id,
        #     name=self._display_name(project_id),
        #     path=project_path,
        # )

    def delete(self, project_id: str) -> None:
        project_path = self._workspace.project_path(project_id)

        if not project_path.is_dir():
            raise ProjectNotFoundError(project_id)

        shutil.rmtree(project_path)

    def _write_metadata(self, project: Project) -> None:
        metadata_path = project.path / self.PROJECT_METADATA

        metadata = {
            "id": project.id,
            "name": project.name,
        }

        metadata_path.write_text(
            json.dumps(
                metadata,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def _read_metadata(self, project_path) -> Project:
        metadata_path = project_path / self.PROJECT_METADATA

        if not metadata_path.is_file():
            raise InvalidProjectError(
                f"Missing project metadata: {project_path}"
            )

        try:
            metadata = json.loads(
                metadata_path.read_text(encoding="utf-8")
            )
        except json.JSONDecodeError as exc:
            raise InvalidProjectError(
                f"Invalid project metadata: {metadata_path}"
            ) from exc

        return Project(
            id=metadata["id"],
            name=metadata["name"],
            path=project_path,
        )
    
    @staticmethod
    def _generate_id(name: str) -> str:
        slug = name.lower().strip()

        slug = re.sub(r"[^a-z0-9\s-]", "", slug)
        slug = re.sub(r"[\s_-]+", "-", slug)
        slug = slug.strip("-")
        slug = slugify(slug)

        if not slug:
            raise ValueError(
                "Project name cannot be converted into a valid project ID."
            )

        return slug

    @staticmethod
    def _display_name(project_id: str) -> str:
        return project_id.replace("-", " ").title()

import re
import unicodedata


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)

    ascii_value = normalized.encode(
        "ascii",
        "ignore",
    ).decode("ascii")

    slug = re.sub(r"[^a-zA-Z0-9\s-]", "", ascii_value)
    slug = re.sub(r"[\s_-]+", "-", slug)

    return slug.strip("-").lower()

class ProjectNotFoundError(LookupError):
    def __init__(self, project_id: str) -> None:
        super().__init__(f"Project '{project_id}' was not found.")


class InvalidProjectError(RuntimeError):
    def __init__(self, project_id: str) -> None:
        super().__init__(f"Project '{project_id}' invalid.")