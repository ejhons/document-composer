from pydantic import BaseModel


class RuntimeNodeState(BaseModel):
    dirty: bool = False
    resolved: bool = False
    compiled: bool = False