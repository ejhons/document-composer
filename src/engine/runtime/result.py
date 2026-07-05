from pydantic import BaseModel, Field

from engine.runtime.artifacts import OutputArtifact
from engine.runtime.context import ExecutionContext
from engine.common.models.inspection import Diagnostic
from engine.planner.graph.dependency_queue import PendingResolution


class EngineResult(BaseModel):
    outputs: dict[str, OutputArtifact]
    diagnostics: list[Diagnostic]
    execution_time: float

class RuntimeResolutionResult(BaseModel):
    changed: bool = False
    pending_inputs: set[str] = Field(default_factory=set)
    # missing_fields: set[str]
    # missing_variables: set[str]

# class ResolutionResult(BaseModel):
#     completed: bool
#     context: ExecutionContext
#     pending: PendingResolution | None