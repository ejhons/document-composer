
import pytest

from engine.planner.graph.dependency_queue import PendingCollector
from engine.planner.graph.dependency_resolver import DependencyResolver
from engine.planner.graph.runtime_resolver import RuntimeResolver
from engine.planner.planning_context import PlanningContext
from engine.runtime.engine import Engine


@pytest.fixture
def full_engine(context):    
    # plan_context = PlanningContext()
    runtime = RuntimeResolver()
    dependency = DependencyResolver()
    pending = PendingCollector()

    return Engine(
        plan_context=context,
        runtime=runtime,
        dependency=dependency,
        pending=pending
    )