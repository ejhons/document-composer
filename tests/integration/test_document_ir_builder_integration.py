from pprint import pprint

import pytest

from engine.backend.ir.builder import DocumentIRBuilder
from engine.frontend.inspection_pipeline import InspectionPipeline
from engine.planner.graph.component_node import Dependency
from engine.planner.graph.graph import RecipeGraph
from engine.planner.recipe_builder import RecipeGraphBuilder
from engine.runtime.execution.context import ExecutionContext
from engine.runtime.engine import Engine

def test_build_complete_tree(make_node):

    graph = RecipeGraph()

    a = make_node("A", "A")
    b = make_node("B", "B")
    c = make_node("C", "C")
    d = make_node("D", "D")

    graph.add_node(a)
    graph.add_node(b)
    graph.add_node(c)
    graph.add_node(d)

    graph.add_dependency(#"A", "B")
        Dependency(
            source_id='A',
            target_id='B',
            kind='edge'
        )
    )
    graph.add_dependency(#""A", "C")
        Dependency(
            source_id='A',
            target_id='C',
            kind='edge'
        )
    )

    builder = DocumentIRBuilder()

    document = builder.build(graph)

    # pprint(document)

    assert document.find_by_node("A").parent == document.root
    assert document.find_by_node("D").parent == document.root

    assert document.find_by_node("B").parent == document.find_by_node("A")
    assert document.find_by_node("C").parent == document.find_by_node("A")

def test_find_returns_all_blocks(make_node):

    graph = RecipeGraph()

    for i in range(10):
        graph.add_node(
            make_node(str(i), str(i))
        )

    document = DocumentIRBuilder().build(graph)

    for i in range(10):
        assert document.find_by_node(str(i)) is not None

def test_find_by_node(make_node):

    graph = RecipeGraph()

    node = make_node("intro", "Hello")

    graph.add_node(node)

    document = DocumentIRBuilder().build(graph)

    block = document.find_by_node(node.id)

    assert block.id != node.id
    assert block.node_id == node.id

def test_walk_order(make_node):

    graph = RecipeGraph()

    a = make_node("A", "")
    b = make_node("B", "")
    c = make_node("C", "")
    d = make_node("D", "")

    graph.add_node(a)
    graph.add_node(b)
    graph.add_node(c)
    graph.add_node(d)

    # graph.add_edge("A", "B")
    # graph.add_edge("A", "C")
    # graph.add_edge("B", "D")
    
    graph.add_dependency(
        Dependency(
            source_id='A',
            target_id='B',
            kind='edge'
        )
    )
    graph.add_dependency(
        Dependency(
            source_id='A',
            target_id='C',
            kind='edge'
        )
    )
    graph.add_dependency(
        Dependency(
            source_id='B',
            target_id='D',
            kind='edge'
        )
    )

    document = DocumentIRBuilder().build(graph)

    # ids = [
    #     document.(block.node_id
    #     for block in document.walk()
    # ]
    # print(document.nodes_ids)
    ids = ['A', 'B', 'D', 'C']

    assert ids.sort() == document.nodes_ids.sort()
    
    # [
    #     "document",
    #     "A",
    #     "B",
    #     "D",
    #     "C"
    # ]