from enum import Enum
from typing import Any
from pydantic import BaseModel, Field


# class ResolutionStatus(Enum):
#     PENDING_INPUTS
#     PENDING_DEPENDENCIES
#     RESOLVED
#     ERROR
    
class ResolutionState(BaseModel):
    content: str = ""
    # RuntimeResolver
    resolved_inputs: dict[str, Any] = Field(default_factory=dict)
    changed: bool = True
    # variables: dict[str, Any] = Field(default_factory=dict)
    # rendered_variables: dict[str, Any] = Field(default_factory=dict)
    # resolved_resources: dict[str, Any] = Field(default_factory=dict)

    # DependencyResolver
    dependencies: set[str] = Field(default_factory=set)
    # dependents: set[str] = Field(default_factory=set)

    # PendingCollector
    pending_inputs: set[str] = Field(default_factory=set)
    pending_dependencies: set[str] = Field(default_factory=set)

    # Estado geral
    revision: int = 0
    metadata: dict[str, Any] = Field(default_factory=dict)
    # resolved: bool = False


    @property
    def resolved(self):
        # print('content: ', self.content)
        # print('pending inputs: ', self.pending_inputs)
        # print('pending_dependencies: ', self.pending_dependencies)
        return (
            not self.pending_inputs and
            not self.pending_dependencies
        )