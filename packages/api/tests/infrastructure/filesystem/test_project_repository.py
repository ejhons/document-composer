from pathlib import Path

import pytest

from dcp_api.infrastructure.filesystem.project_repository import (
    FilesystemProjectRepository,
    ProjectNotFoundError,
)
from dcp_api.infrastructure.filesystem.workspace import Workspace


@pytest.fixture
def workspace(tmp_path: Path) -> Workspace:
    workspace = Workspace(tmp_path)
    workspace.initialize()
    return workspace


@pytest.fixture
def repository(
    workspace: Workspace,
) -> FilesystemProjectRepository:
    return FilesystemProjectRepository(workspace)


def test_create_project(repository, workspace):
    project = repository.create("Relatório Hidráulico")

    assert project.id == "relatrio-hidrulico"
    assert project.name == "Relatório Hidráulico"
    assert project.path.is_dir()

    assert (project.path / "project.json").is_file()
    assert (project.path / "components").is_dir()
    assert (project.path / "output").is_dir()


def test_list_projects(repository):
    repository.create("Projeto A")
    repository.create("Projeto B")

    projects = repository.list()

    assert len(projects) == 2
    assert {project.name for project in projects} == {
        "Projeto A",
        "Projeto B",
    }


def test_get_project(repository):
    created = repository.create("Meu Projeto")

    project = repository.get(created.id)

    assert project.id == created.id
    assert project.name == created.name
    assert project.path == created.path


def test_get_unknown_project_raises(repository):
    with pytest.raises(ProjectNotFoundError):
        repository.get("inexistente")


def test_delete_project(repository, workspace):
    project = repository.create("Projeto Temporário")

    repository.delete(project.id)

    assert not project.path.exists()
    assert not workspace.project_path(project.id).exists()