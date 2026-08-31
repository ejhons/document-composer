from pydantic import BaseModel, Field
from dcp_engine.planning.graph.graph import RecipeGraph


class EngineResult(BaseModel):
    completed: bool
    graph: RecipeGraph | None = None
    # outputs: dict[str, OutputArtifact]
    # diagnostics: list[Diagnostic]
    # execution_time: float

class RuntimeResolutionResult(BaseModel):
    changed: bool = False
    pending_inputs: set[str] = Field(default_factory=set)
    # missing_fields: set[str]
    # missing_variables: set[str]

# class ResolutionResult(BaseModel):
#     completed: bool
#     context: ExecutionContext
#     pending: PendingResolution | None