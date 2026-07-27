from pydantic import BaseModel, Field
from engine.planner.graph.component_node import ComponentNode, Dependency


class DirectiveResolutionResult(BaseModel):
    # resolved: bool = False
    # placeholder: NodePlaceholder  | None = None
    created_nodes: list[ComponentNode] = Field(default_factory=list)
    dependencies: list[Dependency] = Field(default_factory=list)
