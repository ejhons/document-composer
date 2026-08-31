import pytest
from unittest.mock import Mock
from types import SimpleNamespace
from dcp_engine.common.exceptions import GraphNotSolvedException, ResolutionException
from dcp_engine.pipeline.solving import SolvingModule
from dcp_engine.runtime.builder import EngineBuilder


def create_module():

    return SolvingModule(
        EngineBuilder.default().build()
        # runtime_resolver=Mock(),
        # dependency_resolver=Mock(),
        # pending_collector=Mock(),
        # inspector_registry=Mock(),
        # adapter_registry=Mock(),
        # inspection_pipeline=Mock(),
        # max_loops=3,
    )

def test_execute_should_call_adapt(monkeypatch, engine_context):

    module = SolvingModule(engine_context)#create_module()

    session = Mock()

    monkeypatch.setattr(
        module,
        "_resolve",
        Mock(return_value=SimpleNamespace(completed=True)),
    )

    adapt = Mock()

    monkeypatch.setattr(
        module,
        "_adapt",
        adapt,
    )

    module.execute(session)

    adapt.assert_called_once_with(session)

def test_execute_should_raise_when_not_completed(monkeypatch, engine_context):

    module = SolvingModule(engine_context)
    # module = create_module()

    monkeypatch.setattr(
        module,
        "_resolve",
        Mock(return_value=SimpleNamespace(completed=False)),
    )

    with pytest.raises(GraphNotSolvedException):
        module.execute(Mock())

# def test_resolve_should_finish_on_first_iteration(engine_context):

#     module = SolvingModule(engine_context)
#     module.pending = Mock()
#     # module = create_module()

#     graph = Mock()
#     graph.nodes.values.return_value = [Mock()]

#     session = Mock()
#     session.graph = graph
#     session.execution_context = Mock()

#     module.pending.collect.return_value = SimpleNamespace(
#         resolved=True,
#         unchanged=True,
#     )

#     result = module._resolve(session)

#     assert result.completed

#     module.inspection_pipeline.execute.assert_called_once()
#     module.runtime.resolve.assert_called_once()
#     module.dependency.resolve.assert_called_once()


def test_resolve_should_timeout(engine_context):

    module = SolvingModule(engine_context)
    module.pending = Mock()
    # module = create_module()

    graph = Mock()
    graph.nodes.values.return_value = []

    session = Mock()
    session.graph = graph
    session.execution_context = Mock()

    module.pending.collect.return_value = SimpleNamespace(
        resolved=False,
        unchanged=False,
    )

    with pytest.raises(ResolutionException):
        module._resolve(session)


# def test_adapt_should_convert_supported_node(engine_context):

#     module = SolvingModule(engine_context)
#     # module = create_module()

#     node = Mock()
#     node.component.file_format = "md"

#     graph = Mock()
#     graph.nodes.values.return_value = [node]

#     session = Mock()
#     session.graph = graph
#     session.workspace = Mock()

#     adapter = Mock()

#     adapted = Mock()

#     adapter.convert.return_value = adapted

#     module.plan_context.adapter_registry.get.return_value = adapter

#     module._adapt(session)

#     adapter.convert.assert_called_once()

#     assert node.adapted is adapted


# def test_adapt_should_ignore_unknown_format(engine_context):

#     module = SolvingModule(engine_context)
#     # module = create_module()

#     node = Mock()
#     node.component.file_format = "docx"

#     graph = Mock()
#     graph.nodes.values.return_value = [node]

#     session = Mock()
#     session.graph = graph

#     module.plan_context.adapter_registry.get.return_value = None

#     module._adapt(session)

#     assert not hasattr(node, "adapted")