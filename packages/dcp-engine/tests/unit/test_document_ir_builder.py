import pytest

from dcp_engine.planning.graph.component_node import Dependency
from dcp_engine.planning.graph.graph import RecipeGraph
from dcp_engine.runtime.builder import EngineBuilder
from dcp_engine.runtime.engine import Engine


def test_build_empty_document():
    graph = RecipeGraph()
    # builder = EngineBuilder()
    # document = builder.build(graph)

    assert len(graph.nodes) == 0
    assert len(graph.roots) == 0

    # assert document.root.id == "__document_root__"
    # assert list(document.walk()) == [document.root]

def test_build_single_root(make_node):
    graph = RecipeGraph()
    root = make_node("intro", "# Introdução")
    graph.add_node(root)
    # builder = EngineBuilder()
    # document = builder.build(graph)
    block = graph.get_node("intro")

    assert block is not None
    assert block.resolution.content == "# Introdução"

    assert block in graph.roots

def test_build_hierarchy(make_node):

    graph = RecipeGraph()

    a = make_node("A", "A")
    b = make_node("B", "B")

    graph.add_node(a)
    graph.add_node(b)

    # graph.add_edge(a.id, b.id)
    graph.add_dependency(
        Dependency(
            source_id=a.id,
            target_id=b.id,
            kind='edge'
        )
    )

    # builder = EngineBuilder()

    # document = builder.build(graph)

    block_a = graph.get_node("A")
    block_b = graph.get_node("B")

    assert all([dep.target_id == block_b.id for dep in graph.get_dependency("A")])
    assert graph.has_dependency("A", "B")
    assert graph.has_direct_dependency("A", "B")

def test_use_resolution_content(make_node):
    graph = RecipeGraph()
    node = make_node(
        "chapter",
        "# Chapter"
    )
    graph.add_node(node)
    # document = EngineBuilder().build(graph)
    assert graph.get_node("chapter").resolution.content == "# Chapter"

def test_copy_metadata(make_node):
    node = make_node(
        "chapter",
        "content"
    )
    node.component.metadata = {
        "style": "Heading1"
    }
    graph = RecipeGraph()
    graph.add_node(node)
    # document:Engine = EngineBuilder().build(graph)
    # document.solving()
    # graph.
    assert graph.get_node("chapter").component.metadata == {
        "style": "Heading1"
    }

def test_raise_if_node_not_resolved(make_node):
    node = make_node(
        "chapter",
        ""
    )
    node.resolution.pending_inputs.add("cliente")

    graph = RecipeGraph()
    graph.add_node(node)
    builder = EngineBuilder()

    with pytest.raises(TypeError):
        builder.build(graph)