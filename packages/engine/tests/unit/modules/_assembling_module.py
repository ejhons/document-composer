from unittest.mock import Mock

import pytest
from dcp_engine.common.exceptions import GraphNotSolvedException
from dcp_engine.language.manifests.recipe import ComponentConfig
from dcp_engine.language.syntax.directives import DirectiveCall, TextSpan
from dcp_engine.language.syntax.markdown.atom import (
    MarkdownDirective,
    MarkdownFragment,
    MarkdownPlaceholder,
)
from dcp_engine.language.syntax.markdown.atomized_markdown import AtomizedMarkdown
from dcp_engine.pipeline.assembling import AssemblingModule
from dcp_engine.planning.graph.component_node import ComponentNode, Dependency
from dcp_engine.planning.graph.graph import RecipeGraph
from dcp_engine.runtime.execution.session import ExecutionSession
from dcp_engine.solving.resolution.resolution_state import ResolutionState


@pytest.fixture
def atomizer():
    return Mock()

@pytest.fixture
def module(atomizer):
    return AssemblingModule(atomizer)

def test_execute_should_raise_when_graph_not_solved(module):

    graph = Mock(spec=RecipeGraph)
    type(graph).solved = property(lambda _: False)

    session = ExecutionSession(
        graph=graph
    )

    with pytest.raises(GraphNotSolvedException):
        module.execute(session)

def test_execute_should_keep_plain_fragments(module, atomizer):

    component = ComponentConfig(
        type="template",
        source="cover.md"
    )

    node = ComponentNode(component=component)
    node.resolution = ResolutionState(resolved=True)
    node.adapted = Mock(markdown="# Cover")

    graph = RecipeGraph()
    graph.add_node(node)

    fragmented = AtomizedMarkdown(
        blocks=[
            MarkdownFragment(
                content="# Cover"
            )
        ]
    )

    atomizer.atomize.return_value = fragmented

    session = ExecutionSession(
        graph=graph
    )

    module.execute(session)

    atomizer.atomize.assert_called_once_with("# Cover")

    assert len(fragmented.blocks) == 1
    assert isinstance(
        fragmented.blocks[0],
        MarkdownFragment,
    )

def test_execute_should_replace_directive_by_placeholder(
    module,
    atomizer,
):

    component1 = ComponentConfig(
        type="template",
        source="cover.md",
    )

    component2 = ComponentConfig(
        type="template",
        source="annex.md",
    )

    parent = ComponentNode(component=component1)
    child = ComponentNode(component=component2)

    parent.resolution = ResolutionState(resolved=True)
    child.resolution = ResolutionState(resolved=True)

    parent.adapted = Mock(markdown="dummy")
    child.adapted = Mock(markdown="# Annex")

    graph = RecipeGraph()

    graph.add_node(parent)
    graph.add_node(child)

    graph.add_dependency(
        Dependency(
            source_id=parent.id,
            target_id=child.id,
            origin="0",
        )
    )

    directive = DirectiveCall(
        directive="include",
        expression='include("annex.md")',
        index=0,
        start=TextSpan(line=0, column=0,index=8),
        end=TextSpan(line=0, column=0,index=30),
    )

    fragmented = AtomizedMarkdown(
        blocks=[
            MarkdownFragment(content="Antes"),
            MarkdownDirective(directive=directive),
            MarkdownFragment(content="Depois"),
        ]
    )

    atomizer.atomize.side_effect = [
        fragmented,
        AtomizedMarkdown(
            blocks=[
                MarkdownFragment("# Annex")
            ]
        ),
    ]

    session = ExecutionSession(
        graph=graph
    )

    module.execute(session)

    assert isinstance(
        fragmented.blocks[1],
        MarkdownPlaceholder,
    )

    assert (
        fragmented.blocks[1].node_id
        == child.id
    )


def test_execute_should_atomize_every_node(
    module,
    atomizer,
):

    graph = RecipeGraph()

    for i in range(3):

        component = ComponentConfig(
            type="template",
            source=f"{i}.md",
        )

        node = ComponentNode(component=component)

        node.resolution = ResolutionState(
            resolved=True
        )

        node.adapted = Mock(
            markdown=f"Node {i}"
        )

        graph.add_node(node)

    atomizer.atomize.return_value = AtomizedMarkdown()

    session = ExecutionSession(
        graph=graph
    )

    module.execute(session)

    assert atomizer.atomize.call_count == 3