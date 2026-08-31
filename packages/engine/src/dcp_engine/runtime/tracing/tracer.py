from pydantic import BaseModel, Field

from dcp_engine.runtime.tracing.trace import ExecutionTrace


class ExecutionTracer(BaseModel):
    traces:list[ExecutionTrace] = Field(default_factory=list)