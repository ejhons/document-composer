from typing import Any
from pydantic import BaseModel, Field
from engine.planner.graph.component_node import ComponentNode


class ExecutionPlan(BaseModel):
    steps: list[ExecutionStep]

class ExecutionStep(BaseModel):
    node: ComponentNode
    order: int
    dependencies: list[str]
    context: dict[str, Any] = Field(default_factory=dict)