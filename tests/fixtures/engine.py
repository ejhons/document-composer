
import pytest

from build.lib.engine.execution.engine import Engine
from engine.compilation.compilers.registry import CompilerRegistry
from engine.solving.inspection.pipeline import InspectionPipeline
from engine.solving.resolution.resolution_collector import PendingCollector
from engine.solving.resolution.dependency_resolver import DependencyResolver
from engine.solving.resolution.runtime_resolver import RuntimeResolver
from engine.planning.graph.topology import Topology
from engine.solving.solving_context import SolvingContext
from engine.runtime.builder import EngineBuilder
from engine.backup.scheduler import Scheduler


@pytest.fixture
def full_engine():    
    # plan_context = PlanningContext()
    # inspection_pipeline= InspectionPipeline()
    # runtime = RuntimeResolver()
    # dependency = DependencyResolver()
    # pending = PendingCollector()

    # return Engine(engine_context)
    #     inspection_pipeline=inspection_pipeline,
    #     plan_context=planning_context,
    #     runtime=runtime,
    #     dependency=dependency,
    #     pending=pending,
    #     compiler_registry=CompilerRegistry(),
    #     bootstrap=True
    # )
    return EngineBuilder.default().build()

# @pytest.fixture
# def scheduler():
#     return Scheduler(
#         topology=Topology()
#     )