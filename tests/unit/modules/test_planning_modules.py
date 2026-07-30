from unittest.mock import Mock, patch
from engine.frontend.manifests.recipe import RecipeManifest, StyleConfig
from engine.modules.planning import PlanningModule
from engine.runtime.execution.context import ExecutionContext
from engine.runtime.execution.session import ExecutionSession


@patch("engine.modules.planning.RecipeGraphBuilder")
def test_execute_should_build_graph(builder_cls, engine_context):
    graph = Mock()

    builder = builder_cls.return_value
    builder.build.return_value = graph

    resource_resolver = Mock()

    session = ExecutionSession(
        manifest=RecipeManifest(
            recipe_name='test',
            version='1',
            style=StyleConfig()
        ),
        execution_context=ExecutionContext()
    )

    module = PlanningModule(engine_context)
    #     resource_resolver=resource_resolver
    # )

    returned = module.execute(session)

    # builder.build.assert_called_once_with(
    #     manifest=session.manifest,
    #     resource_resolver=resource_resolver,
    # )

    assert returned is session
    assert session.graph is graph