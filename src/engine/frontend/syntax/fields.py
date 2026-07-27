from pydantic import BaseModel, Field
from typing import Any, Literal, Optional

from engine.frontend.syntax.inputs import InputReference


class InputDefinition(BaseModel):
    name: str
    declared: bool
    type: Literal["text", "number", "date"] = "text"#Field(default="text")
    label: str | None = None
    description: Optional[str] = None
    default: Optional[Any] = None

    references: list[InputReference] = Field(default_factory=list)
    # label: str
    # data_type: Literal["text", "number", "date"] = Field(default="text")
    # description: Optional[str] = None
    # default: Optional[Any] = None

    
# class InputDefinition:
#     name: str
#     # type: str
#     declared: bool
#     data_type: Literal["text", "number", "date"] = Field(default="text")
#     label: str | None = None
#     description: Optional[str] = None
#     default: Optional[Any] = None
