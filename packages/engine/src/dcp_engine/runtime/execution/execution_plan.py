from typing import Any
from warnings import deprecated
from pydantic import BaseModel, Field
from dcp_engine.planning.graph.component_node import ComponentNode



@deprecated('Unused')
class ExecutionPlan(BaseModel):
    steps: list[ExecutionStep]

    def initializate(self):
        for step in self.steps:
            step.executed = False


@deprecated('Unused')
class ExecutionStep(BaseModel):
    node: ComponentNode
    order: int
    dependencies: list[str]
    executed: bool = False
    context: dict[str, Any] = Field(default_factory=dict)