from unittest.mock import Mock, patch
from engine.modules.planning import PlanningModule
from engine.runtime.execution.session import ExecutionSession


@patch("engine.modules.planning.RecipeGraphBuilder")
def test_execute_should_build_graph(builder_cls):
    graph = Mock()

    builder = builder_cls.return_value
    builder.build.return_value = graph

    resource_resolver = Mock()

    session = ExecutionSession(
        manifest=Mock()
    )

    module = PlanningModule(
        resource_resolver=resource_resolver
    )

    returned = module.execute(session)

    builder.build.assert_called_once_with(
        manifest=session.manifest,
        resource_resolver=resource_resolver,
    )

    assert returned is session
    assert session.graph is graph