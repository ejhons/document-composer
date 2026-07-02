from pydantic import BaseModel, Field
from engine.src.doc_engine.planning.recipe.component_node import ComponentNode


class DirectiveResolutionResult(BaseModel):
    created_nodes: list[ComponentNode] = Field(default_factory=list)