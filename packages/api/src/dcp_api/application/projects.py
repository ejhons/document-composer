from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Protocol
from dcp_api.domain.project import Project


class BaseProjectRepository(Protocol):
    """
    Porta de persistência de projetos.

    A camada de aplicação depende deste contrato,
    nunca de uma implementação concreta.
    """
    def create(self, name: str) -> Project:
        ...

    def list(self) -> list[Project]:
        ...

    def get(self, project_id: str) -> Project:
        ...

    def delete(self, project_id: str) -> None:
        ...

class ProjectRepository:
    """
    Porta de persistência de projetos.

    A camada de aplicação depende deste contrato,
    nunca de uma implementação concreta.
    """
    def create(self, name: str) -> Project:
        raise NotImplementedError

    def list(self) -> list[Project]:
        raise NotImplementedError

    def get(self, project_id: str) -> Project:
        raise NotImplementedError

    def delete(self, project_id: str) -> None:
        raise NotImplementedError


class ProjectService:
    """
    Casos de uso relacionados a projetos.
    Não possui conhecimento sobre HTTP ou filesystem.
    """
    def __init__(self, repository: BaseProjectRepository) -> None:
        self._repository: BaseProjectRepository = repository

    def create_project(self, name: str) -> Project:
        name = self._normalize_name(name)

        if not name:
            raise ValueError("Project name cannot be empty.")

        return self._repository.create(name)

    def list_projects(self) -> list[Project]:
        return self._repository.list()

    def get_project(self, project_id: str) -> Project:
        if not project_id.strip():
            raise ValueError("Project ID cannot be empty.")

        return self._repository.get(project_id)

    def delete_project(self, project_id: str) -> None:
        if not project_id.strip():
            raise ValueError("Project ID cannot be empty.")

        self._repository.delete(project_id)

    @staticmethod
    def _normalize_name(name: str) -> str:
        return " ".join(name.strip().split())



# class ProjectService():
#     def create_project(self, name: str) -> Project:
#         self.name = name

#     def list_projects(self) -> list[Project]:
#         ...

#     def get_project(self, project_id: str) -> Project:
#         ...

#     def delete_project(self, project_id: str) -> None:
#         ...