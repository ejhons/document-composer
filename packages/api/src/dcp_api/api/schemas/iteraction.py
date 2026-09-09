from __future__ import annotations

from datetime import date
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

from dcp_api.domain.iteraction import (
    IterationStatus,
    ResolutionKind,
)


class StartIterationRequest(BaseModel):
    variables: dict[str, Any] = Field(default_factory=dict)


class ResolveIterationRequest(BaseModel):
    values: dict[str, Any] = Field(default_factory=dict)


class SessionIterationResponse(BaseModel):
    project_id: str
    session_id: str
    variables: dict[str, Any] = Field(default_factory=dict)

class SessionIterationListResponse(BaseModel):
    sessions: list[SessionIterationResponse] = Field(
        default_factory=list
    )


class ResolveIterationResponse(BaseModel):
    project_id: str
    session_id: str
    status: IterationStatus
    # variables: dict[str, Any]
    pending: list[PendingResolutionResponse] = Field(default_factory=list)
    # ready: bool

    @property
    def ready(self):
        return self.status == IterationStatus.READY

class PendingResolutionResponse(BaseModel):
    id: str
    # kind: ResolutionKind
    name: str
    type: Literal["text", "number", "date"] = "text"
    description: str | None = None    
    default: Optional[Any] = None
    # metadata: dict[str, Any]= Field(default_factory=dict)