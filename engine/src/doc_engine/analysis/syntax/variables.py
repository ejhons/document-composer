from typing import Optional
from pydantic import BaseModel, Field

class VariableReference(BaseModel):
    name: str
    index: int | None = None

