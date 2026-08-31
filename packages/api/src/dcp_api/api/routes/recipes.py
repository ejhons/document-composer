from fastapi import APIRouter, Depends

from dcp_api.api.dependencies import get_recipe_service
from dcp_api.application.recipes import RecipeService


router = APIRouter(
    prefix="/api/projects/{project_id}/recipe",
    tags=["recipes"],
)


@router.get("")
def get_recipe(
    project_id: str,
    service: RecipeService = Depends(
        get_recipe_service
    ),
):
    return service.get_recipe(project_id)


@router.put("")
def update_recipe(
    project_id: str,
    recipe: dict,
    service: RecipeService = Depends(
        get_recipe_service
    ),
):
    service.update_recipe(
        project_id,
        recipe,
    )

    return {
        "status": "updated",
    }