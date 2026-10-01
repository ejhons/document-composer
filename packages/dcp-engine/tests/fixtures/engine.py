
import pytest

from dcp_engine.runtime.builder import EngineBuilder

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