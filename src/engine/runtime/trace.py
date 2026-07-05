from pydantic import BaseModel

class ExecutionTrace(BaseModel):
    revision: int
    changed_inputs: set[str]
    created_nodes: set[str]
    removed_nodes: set[str]
    execution_time: float