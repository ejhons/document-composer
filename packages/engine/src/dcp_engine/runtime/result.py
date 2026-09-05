from enum import Enum, StrEnum

from pydantic import BaseModel, Field
from dcp_engine.planning.graph.graph import RecipeGraph
from dcp_engine.solving.resolution.resolution_collector import PendingResolution

class SolvingStatus(StrEnum):
    RESOLVED = 'resolved'
    PENDING = 'pending'
    CHANGED =  'changed'

class SolvingResult(BaseModel):
    completed: bool
    graph: RecipeGraph | None = None
    pending: PendingResolution | None = None
    # pending: list[PendingResolution] = Field(default_factory=list)
    # outputs: dict[str, OutputArtifact]
    # diagnostics: list[Diagnostic]
    # execution_time: float

    @property
    def resolved(self) -> bool:
        return self.status is SolvingStatus.RESOLVED

class RuntimeResolutionResult(BaseModel):
    changed: bool = False
    pending_inputs: set[str] = Field(default_factory=set)
    # missing_fields: set[str]
    # missing_variables: set[str]

# class ResolutionResult(BaseModel):
#     completed: bool
#     context: ExecutionContext
#     pending: PendingResolution | None