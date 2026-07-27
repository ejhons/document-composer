
import pytest

from build.lib.engine.execution.engine import Engine
from engine.backend.compilers.registry import CompilerRegistry
from engine.frontend.inspection_pipeline import InspectionPipeline
from engine.planner.resolution.resolution_collector import PendingCollector
from engine.planner.resolution.dependency_resolver import DependencyResolver
from engine.planner.resolution.runtime_resolver import RuntimeResolver
from engine.planner.graph.topology import Topology
from engine.planner.planning_context import PlanningContext
from engine.runtime.scheduler import Scheduler


@pytest.fixture
def full_engine(planning_context):    
    # plan_context = PlanningContext()
    inspection_pipeline= InspectionPipeline()
    runtime = RuntimeResolver()
    dependency = DependencyResolver()
    pending = PendingCollector()

    return Engine(
        inspection_pipeline=inspection_pipeline,
        plan_context=planning_context,
        runtime=runtime,
        dependency=dependency,
        pending=pending,
        compiler_registry=CompilerRegistry(),
        bootstrap=True
    )

@pytest.fixture
def scheduler():
    return Scheduler(
        topology=Topology()
    )