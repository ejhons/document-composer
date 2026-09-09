
from dataclasses import Field, dataclass, field
from uuid import uuid4

from dcp_engine.runtime.execution.session import ExecutionSession


@dataclass
class Session:
    project_id: str
    execution_session: ExecutionSession
    id: str = field(default_factory = lambda: str(uuid4()))