from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class ExecutionTask(BaseModel):
    id: str
    source_path: str
    file_format: str
    context_data: Dict[str, Any] = Field(default_factory=dict)
    depends_on: List[str] = [] # IDs de tarefas que precisam terminar antes dela
    resolved_content: Optional[str] = None
    is_completed: bool = False

