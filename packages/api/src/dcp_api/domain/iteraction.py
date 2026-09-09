from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class IterationStatus(str, Enum):
    NEEDS_INPUT='needs_input'
    READY = "ready"


class ResolutionKind(str, Enum):
    VARIABLE = "variable"
    DEPENDENCY = "dependency"


@dataclass(frozen=True, slots=True)
class PendingResolution:
    id: str
    kind: ResolutionKind
    name: str
    description: str | None = None
    required: bool = True
    metadata: dict[str, Any] = field(
        default_factory=dict
    )


# @dataclass(slots=True)
# class IterationSession:

#     id: str
#     project_id: str

#     status: IterationStatus = IterationStatus.PENDING
#     variables: dict[str, Any] = field(default_factory=dict)
#     pending: list[PendingResolution] = field(default_factory=list)

#     metadata: dict[str, Any] = field(default_factory=dict)

#     def is_ready(self) -> bool:
#         return not self.pending

#     def update_variables(
#         self,
#         values: dict[str, Any],
#     ) -> None:

#         self.variables.update(values)

#     def update_pending(
#         self,
#         pending: list[PendingResolution],
#     ) -> None:

#         self.pending = pending

#         self.status = (
#             IterationStatus.READY
#             if self.is_ready()
#             else IterationStatus.PENDING
#         )