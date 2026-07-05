import pytest

from engine.common.models.recipe import ComponentConfig
from engine.planner.graph.component_node import ComponentNode
from engine.planner.graph.graph import RecipeGraph


@pytest.fixture
def empty_graph():

    return RecipeGraph()

@pytest.fixture
def graph_with_root():

    graph = RecipeGraph()

    node = ComponentNode(

        component=ComponentConfig(
            # id="cover",
            type="template",
            source="cover.md",
            file_format='md'
        )
    )

    graph.add_node(node)

    return graph

@pytest.fixture
def graph_chain():

    graph = RecipeGraph()

    a = ComponentNode(...)
    b = ComponentNode(...)
    c = ComponentNode(...)

    graph.add_node(a)
    graph.add_node(b)
    graph.add_node(c)

    graph.add_dependency(a.id, b.id)

    graph.add_dependency(b.id, c.id)

    return graph

