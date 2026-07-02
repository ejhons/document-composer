import logging
from typing import Dict, List, Any, Optional

from engine.src.doc_engine.models.runtime import ExecutionTask

logger = logging.getLogger("doc_engine.scheduler")

class TaskScheduler:
    """
    Manages a LIFO execution stack and dependency graph for document blocks.
    Ensures nested variables and inner shortcodes are resolved in correct order.
    """
    def __init__(self):
        self.stack: List[ExecutionTask] = []
        self.registry: Dict[str, ExecutionTask] = {}

    def push_task(self, task: ExecutionTask):
        """Pushes a new evaluation task into the execution framework."""
        if task.id in self.registry:
            # Evita loops infinitos de dependências circulares
            return
        logger.debug(f"[Scheduler] Pushing task to stack: {task.id} ({task.file_format})")
        self.stack.append(task)
        self.registry[task.id] = task

    def pop_task(self) -> Optional[ExecutionTask]:
        """Retrieves the next executable task from the top of the stack."""
        if not self.stack:
            return None
        return self.stack.pop()

    def has_tasks(self) -> bool:
        return len(self.stack) > 0

    def get_resolved_value(self, task_id: str) -> str:
        """Fetch finished structural strings from registry data."""
        task = self.registry.get(task_id)
        return task.resolved_content if task and task.is_completed else ""