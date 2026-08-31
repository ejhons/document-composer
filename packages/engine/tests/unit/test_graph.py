from unittest.mock import Mock

import pytest
from typing import Any

from dcp_engine.common.exceptions import NodeAlreadyRegistered, NodeNotFoundException
from dcp_engine.planning.graph.component_node import Dependency


# Add Node
def test_should_add_node(graph, node_a):
    graph.add_node(node_a)

    assert node_a.id in graph.nodes


def test_should_not_allow_duplicate_node(graph, node_a):
    graph.add_node(node_a)

    with pytest.raises(NodeAlreadyRegistered):
        graph.add_node(node_a)


# Find By Source
def test_should_find_node_by_source(graph, node_a):
    graph.add_node(node_a)

    found = graph.find_by_source("a.md")

    assert found == node_a

def test_should_return_none_when_source_not_found(graph):
    assert graph.find_by_source("missing.md") is None

# Add dependency
def test_should_add_dependency(graph, node_a, node_b):
    graph.add_node(node_a)
    graph.add_node(node_b)

    dep = Dependency(
        source_id="A",
        target_id="B",
        kind='test'
    )

    graph.add_dependency(dep)

    assert dep in graph.edges

# Source Inexistente
def test_should_fail_when_source_node_does_not_exist(graph, node_b):
    graph.add_node(node_b)

    dep = Dependency(
        source_id="A",
        target_id="B",
        kind='test'
    )

    with pytest.raises(NodeNotFoundException):
        graph.add_dependency(dep)

# target inexistente
def test_should_fail_when_target_node_does_not_exist(graph, node_a):
    graph.add_node(node_a)

    dep = Dependency(
        source_id="A",
        target_id="B",
        kind='test'
    )

    with pytest.raises(NodeNotFoundException):
        graph.add_dependency(dep)

# Has dependency
def test_should_detect_direct_dependency(graph, node_a, node_b):
    graph.add_node(node_a)
    graph.add_node(node_b)

    graph.add_dependency(
        Dependency(
            source_id="A",
            target_id="B",
            kind='test'
        )
    )

    assert graph.has_dependency("A", "B")

def test_should_return_false_when_dependency_does_not_exist(graph, node_a, node_b):
    graph.add_node(node_a)
    graph.add_node(node_b)

    assert graph.has_dependency("A", "B") is False

# Dependência indireta
def test_should_detect_indirect_dependency(graph, node_a, node_b, node_c):
    graph.add_node(node_a)
    graph.add_node(node_b)
    graph.add_node(node_c)

    graph.add_dependency(Dependency(source_id="A", target_id="B", kind='test'))
    graph.add_dependency(Dependency(source_id="B", target_id="C", kind='test'))

    assert graph.has_direct_dependency("A", "C")

def test_should_return_false_when_nodes_are_not_connected(graph, node_a, node_b):
    graph.add_node(node_a)
    graph.add_node(node_b)

    assert graph.has_direct_dependency("A", "B") is False

# Children
def test_should_return_children(graph, node_a, node_b):
    graph.add_node(node_a)
    graph.add_node(node_b)

    graph.add_dependency(
        Dependency(source_id="A", target_id="B", kind='test')
    )

    children = graph.children("A")

    assert children == [node_b]

# Parents
def test_should_return_parents(graph, node_a, node_b):
    graph.add_node(node_a)
    graph.add_node(node_b)

    graph.add_dependency(
        Dependency(source_id="A", target_id="B", kind='test')
    )

    parents = graph.parents("B")

    assert parents == [node_a]

# Roots
def test_should_return_root_nodes(graph, node_a, node_b):
    graph.add_node(node_a)
    graph.add_node(node_b)

    graph.add_dependency(
        Dependency(source_id="A", target_id="B", kind='test')
    )

    assert graph.roots == [node_a]

# Leaves
def test_should_return_leaf_nodes(graph, node_a, node_b):
    graph.add_node(node_a)
    graph.add_node(node_b)

    graph.add_dependency(
        Dependency(source_id="A", target_id="B", kind='test')
    )

    assert graph.leaves == [node_b]

# Solved
def test_should_be_solved_when_all_nodes_are_resolved(graph, node_a, node_b):
    a = Mock()
    b = Mock()
    a.resolution.resolved.return_value = True
    b.resolution.resolved.return_value = True
    node_a.resolution = a#.resolved = True
    node_b.resolution = b#.resolved = True

    graph.add_node(node_a)
    graph.add_node(node_b)

    assert graph.solved