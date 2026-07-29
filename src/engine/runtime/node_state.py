from warnings import deprecated

from pydantic import BaseModel


@deprecated('Unused')
class RuntimeNodeState(BaseModel):
    dirty: bool = False
    resolved: bool = False
    compiled: bool = False