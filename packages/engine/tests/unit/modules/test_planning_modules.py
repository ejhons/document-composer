from unittest.mock import Mock, patch

from dcp_engine.language.manifests.recipe import RecipeManifest, StyleConfig
from dcp_engine.pipeline.planning import PlanningModule
from dcp_engine.runtime.execution.context import ExecutionContext
from dcp_engine.runtime.execution.session import ExecutionSession


@patch("dcp_engine.pipeline.planning.RecipeGraphBuilder")
def test_execute_should_build_graph(builder_cls, engine_context):
    expected_graph = Mock()

    mock_builder_instance = builder_cls.return_value
    mock_builder_instance.build.return_value = expected_graph

    session = ExecutionSession(
        manifest=RecipeManifest(
            recipe_name='test',
            version='1',
            style=StyleConfig()
        ),
        execution_context=ExecutionContext()
    )

    module = PlanningModule(
        context=engine_context,
        builder_cls=builder_cls
    )

    returned = module.execute(session)
    # Assert
    # 1. Verifica se chamou o builder com os parâmetros corretos
    builder_cls.assert_called_once_with(resource_resolver=engine_context.resource_resolver)
    mock_builder_instance.build.assert_called_once_with(manifest=session.manifest)
    
    assert returned is session
    assert session.graph is expected_graph

    # builder.build.assert_called_once_with(
    #     manifest=session.manifest,
    #     resource_resolver=resource_resolver,
    # )