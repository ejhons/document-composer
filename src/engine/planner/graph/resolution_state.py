from typing import Any
from pydantic import BaseModel, Field


class ResolutionState(BaseModel):
    content: str = ""
    # RuntimeResolver
    resolved_inputs: dict[str, Any] = Field(default_factory=dict)
    # variables: dict[str, Any] = Field(default_factory=dict)
    # rendered_variables: dict[str, Any] = Field(default_factory=dict)
    # resolved_resources: dict[str, Any] = Field(default_factory=dict)
    changed: bool = False

    # DependencyResolver
    dependencies: set[str] = Field(default_factory=set)
    # dependents: set[str] = Field(default_factory=set)

    # PendingCollector
    pending_inputs: set[str] = Field(default_factory=set)
    pending_dependencies: set[str] = Field(default_factory=set)

    # Estado geral
    # resolved: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)

    revision: int = 0

    @property
    def resolved(self):
        return (
            not self.pending_inputs and
            not self.pending_dependencies
        )