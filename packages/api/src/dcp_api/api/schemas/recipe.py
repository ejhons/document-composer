
from typing import Any, List, Literal
from pydantic import BaseModel, Field

class UpdateRecipeRequest(BaseModel):
    content: dict[str, Any]


class RecipeContentResponse(BaseModel):
    content: dict[str, Any]
    # raw_content: str

class RecipeUpdateStatusResponse(BaseModel):
    status: Literal["updated", "failed", "cancelled"]