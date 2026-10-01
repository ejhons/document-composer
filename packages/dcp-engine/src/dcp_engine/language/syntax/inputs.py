from pydantic import BaseModel

class InputReference(BaseModel):
    name: str
    raw: str
    index: int | None = None

