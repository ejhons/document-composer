from pydantic import Field
from typing import Any, Literal, Optional


class DeprecatedInputDefinition:
    name: str
    # type: str
    declared: bool
    data_type: Literal["text", "number", "date"] = Field(default="text")
    label: str | None = None
    description: Optional[str] = None
    default: Optional[Any] = None