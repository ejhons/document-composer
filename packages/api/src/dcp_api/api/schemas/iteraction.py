from __future__ import annotations

from datetime import date
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

from dcp_api.domain.iteraction import (
    IteractionStatus,
    ResolutionKind,
)


class StartIteractionRequest(BaseModel):
    variables: dict[str, Any] = Field(default_factory=dict)


class ResolveIteractionRequest(BaseModel):
    values: dict[str, Any] = Field(default_factory=dict)


class SessionIteractionResponse(BaseModel):
    project_id: str
    session_id: str
    variables: dict[str, Any] = Field(default_factory=dict)

class SessionIteractionListResponse(BaseModel):
    sessions: list[SessionIteractionResponse] = Field(
        default_factory=list
    )


class ResolveIteractionResponse(BaseModel):
    project_id: str
    session_id: str
    status: IteractionStatus
    # variables: dict[str, Any]
    pending: list[PendingResolutionResponse] = Field(default_factory=list)
    # ready: bool

    @property
    def ready(self):
        return self.status == IteractionStatus.READY

class PendingResolutionResponse(BaseModel):
    id: str
    # kind: ResolutionKind
    name: str
    type: Literal["text", "number", "date"] = "text"
    description: str | None = None    
    default: Optional[Any] = None
    # metadata: dict[str, Any]= Field(default_factory=dict)