from typing import Any
from pydantic import BaseModel, Field
from engine.planner.graph.component_node import ComponentNode


class ExecutionPlan(BaseModel):
    steps: list[ExecutionStep]

    def initializate(self):
        for step in self.steps:
            step.executed = False

class ExecutionStep(BaseModel):
    node: ComponentNode
    order: int
    dependencies: list[str]
    executed: bool = False
    context: dict[str, Any] = Field(default_factory=dict)