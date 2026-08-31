from __future__ import annotations

import json
from typing import Any

from dcp_api.application.recipes import RecipeRepository
from dcp_api.infrastructure.filesystem.project_repository import (
    ProjectNotFoundError,
)
from dcp_api.infrastructure.filesystem.workspace import Workspace


class FilesystemRecipeRepository(RecipeRepository):

    RECIPE_FILENAME = "recipe.json"

    def __init__(self, workspace: Workspace) -> None:
        self._workspace = workspace

    def get(
        self,
        project_id: str,
    ) -> dict[str, Any]:
        path = self._recipe_path(project_id)

        if not path.is_file():
            raise RecipeNotFoundError(project_id)

        try:
            return json.loads(
                path.read_text(encoding="utf-8")
            )
        except json.JSONDecodeError as exc:
            raise InvalidRecipeError(
                f"Invalid recipe: {path}"
            ) from exc

    def save(
        self,
        project_id: str,
        recipe: dict[str, Any],
    ) -> None:
        path = self._recipe_path(project_id)

        path.write_text(
            json.dumps(
                recipe,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def _recipe_path(self, project_id: str):
        project = self._workspace.project_path(project_id)

        if not project.is_dir():
            raise ProjectNotFoundError(project_id)

        return project / self.RECIPE_FILENAME


class RecipeNotFoundError(LookupError):
    ...


class InvalidRecipeError(RuntimeError):
    ...