import pytest

from engine.compilation.ir.builder import DocumentIRBuilder
from engine.planning.graph.component_node import Dependency
from engine.planning.graph.graph import RecipeGraph


def test_build_empty_document():
    graph = RecipeGraph()
    builder = DocumentIRBuilder()
    document = builder.build(graph)

    assert document.root.id == "__document_root__"
    assert list(document.walk()) == [document.root]

def test_build_single_root(make_node):
    graph = RecipeGraph()
    root = make_node("intro", "# Introdução")
    graph.add_node(root)
    builder = DocumentIRBuilder()
    document = builder.build(graph)
    block = document.find_by_node("intro")

    assert block is not None
    assert block.content == "# Introdução"

    assert block.parent == document.root

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

    builder = DocumentIRBuilder()

    document = builder.build(graph)

    block_a = document.find_by_node("A")
    block_b = document.find_by_node("B")

    assert block_b.parent == block_a

def test_use_resolution_content(make_node):
    graph = RecipeGraph()
    node = make_node(
        "chapter",
        "# Chapter"
    )
    graph.add_node(node)
    document = DocumentIRBuilder().build(graph)
    assert document.find_by_node("chapter").content == "# Chapter"

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
    document = DocumentIRBuilder().build(graph)
    assert document.find_by_node("chapter").metadata == {
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
    builder = DocumentIRBuilder()

    with pytest.raises(ValueError):
        builder.build(graph)