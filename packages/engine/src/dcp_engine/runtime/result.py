from enum import StrEnum
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


class RuntimeResolutionResult(BaseModel):
    changed: bool = False
    pending_inputs: set[str] = Field(default_factory=set)