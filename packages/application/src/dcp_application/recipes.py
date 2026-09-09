from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class RecipeRepository(ABC):

    @abstractmethod
    def get(self, project_id: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        project_id: str,
        recipe: dict[str, Any],
    ) -> None:
        raise NotImplementedError


class RecipeService:

    def __init__(self, repository: RecipeRepository) -> None:
        self._repository = repository

    def get_recipe(
        self,
        project_id: str,
    ) -> dict[str, Any]:
        return self._repository.get(project_id)

    def update_recipe(
        self,
        project_id: str,
        recipe: dict[str, Any],
    ) -> None:
        self._repository.save(
            project_id,
            recipe,
        )