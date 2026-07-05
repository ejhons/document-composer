from pydantic import BaseModel

class VariableReference(BaseModel):
    name: str
    raw: str
    index: int | None = None

