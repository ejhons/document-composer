from pathlib import Path

from engine.compilation.adapters.base import BaseContentAdapter
from engine.planning.graph.assets import AssetBundle, ComponentContent
from engine.planning.graph.builder import RecipeGraphBuilder
from engine.solving.resolution.adaptation_resolver import AdaptationResolver
from engine.runtime.execution.context import ExecutionContext
from engine.runtime.execution.session import ExecutionSession

class FakeMarkdownAdapter(BaseContentAdapter):

    def __init__(self):
        self.called = False
        self.received_node = None

    def convert(
        self,
        node,
        # context,
        workspace
    ):
        self.called = True
        self.received_node = node

        return ComponentContent(
            markdown="<!-- adapted -->",
            # assets=AssetBundle()
        )

def test_adapter_pipeline_should_adapt_supported_nodes(
    temp_workspace_object,
    markdown_file,
    recipe_manifest,
    planning_context,
    resource_resolver,
):
    markdown_file(
        "cover.md",
        """
# Cover

{{ client }}
"""
    )

    recipe_manifest.components[0].source = (
        temp_workspace_object.root / "cover.md"
    ).as_posix()

    graph = RecipeGraphBuilder(
        resource_resolver
    ).build(recipe_manifest)

    adapter = FakeMarkdownAdapter()

    planning_context.adapter_registry.register(
        "md",
        adapter
    )

    session = ExecutionSession(
        graph=graph,
        manifest=recipe_manifest,
        execution_context = ExecutionContext(),
        workspace=temp_workspace_object
    )

    solver = AdaptationResolver(
        adapter_registry = planning_context.adapter_registry
    )
    solver.resolve(session.graph, session.workspace)
    # solver._adapt(session)

    node = next(iter(graph.nodes.values()))

    assert adapter.called is True
    assert adapter.received_node == node

    assert node.adapted is not None
    assert node.adapted.markdown == "<!-- adapted -->"

# def test_adapter_pipeline_should_ignore_unknown_formats(...):
#     ...

#     node = next(iter(graph.nodes.values()))

#     assert node.adapted is None

#     assert len(node.adapted.assets) == 1
# assert node.adapted.assets[0].tag == "annex_1"
# assert node.adapted.assets[0].output.exists()