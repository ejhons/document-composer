import logging
from warnings import deprecated

from engine.planner.graph.topology import Topology
from engine.runtime.execution.execution_plan import ExecutionPlan, ExecutionStep
from engine.planner.graph.graph import RecipeGraph

logger = logging.getLogger("doc_engine.scheduler")

@deprecated('Unused')
class Scheduler:
    def __init__(
            self,
            topology: Topology | None = None,
            ordered_steps: list[ExecutionStep] = []
    ):
        self.topology = topology or Topology()
        self.ordered_steps = ordered_steps

    def schedule(
        self,
        graph: RecipeGraph
    ) -> ExecutionPlan:
        # print(graph)
        ordered = self.topology.topological_order(graph)
        steps = []

        for order, node in enumerate(ordered):
            steps.append(
                ExecutionStep(
                    node=node,
                    order=order,
                    dependencies=[
                        parent.id
                        for parent in graph.parents(node.id)
                    ]
                )
            )

        self.ordered_steps = steps
        return ExecutionPlan(steps=steps)


# class TaskScheduler:
#     """
#     Manages a LIFO execution stack and dependency graph for document blocks.
#     Ensures nested variables and inner shortcodes are resolved in correct order.
#     """
#     def __init__(self):
#         self.stack: List[ExecutionTask] = []
#         self.registry: Dict[str, ExecutionTask] = {}

#     def push_task(self, task: ExecutionTask):
#         """Pushes a new evaluation task into the execution framework."""
#         if task.id in self.registry:
#             # Evita loops infinitos de dependências circulares
#             return
#         logger.debug(f"[Scheduler] Pushing task to stack: {task.id} ({task.file_format})")
#         self.stack.append(task)
#         self.registry[task.id] = task

#     def pop_task(self) -> Optional[ExecutionTask]:
#         """Retrieves the next executable task from the top of the stack."""
#         if not self.stack:
#             return None
#         return self.stack.pop()

#     def has_tasks(self) -> bool:
#         return len(self.stack) > 0

#     def get_resolved_value(self, task_id: str) -> str:
#         """Fetch finished structural strings from registry data."""
#         task = self.registry.get(task_id)
#         return task.resolved_content if task and task.is_completed else ""