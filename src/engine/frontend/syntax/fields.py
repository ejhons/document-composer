from pydantic import BaseModel, Field
from typing import Any, Literal, Optional


class FieldDefinition(BaseModel):
    label: str
    data_type: Literal["text", "number", "date"] = Field(default="text")
    description: Optional[str] = None
    default: Optional[Any] = None
