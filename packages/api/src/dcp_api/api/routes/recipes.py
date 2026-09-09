from dcp_api.api.mappers.files import FilesMapper
from dcp_api.api.schemas.recipe import RecipeContentResponse, RecipeUpdateStatusResponse, UpdateRecipeRequest
from fastapi import APIRouter, Depends
import json
from dcp_api.api.dependencies import get_recipe_service
from dcp_api.application.recipes import RecipeService


router = APIRouter(
    prefix="/projects/{project_id}/recipe",
    tags=["recipes"],
)

mapper = FilesMapper()

@router.get("")
def get_recipe(
    project_id: str,
    service: RecipeService = Depends(
        get_recipe_service
    ),
):
    recipe_dict = service.get_recipe(project_id)
    
    return RecipeContentResponse(
        content = recipe_dict,
        # raw_content=json.dumps(recipe_dict, indent=4)
    )


@router.put("")
def update_recipe(
    project_id: str,
    recipe: UpdateRecipeRequest,
    # recipe: dict,
    service: RecipeService = Depends(
        get_recipe_service
    ),
):
    service.update_recipe(
        project_id,
        recipe.content,
    )

    return RecipeUpdateStatusResponse(
        status="updated",
    )