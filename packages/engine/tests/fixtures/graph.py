import pytest
from dcp_engine.language.manifests.recipe import ComponentConfig
from dcp_engine.planning.graph.component_node import ComponentNode
from dcp_engine.planning.graph.graph import RecipeGraph
from dcp_engine.solving.resolution.resolution_state import ResolutionState


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

@pytest.fixture
def component():
    return ComponentConfig(
        id="component",
        source="main.md",
        metadata={"title": "Main"}
    )
@pytest.fixture
def make_node():
    def _build(node_id: str, content: str):
        node = ComponentNode(
            id=node_id,
            component=ComponentConfig(
                # id=node_id,
                type='template',
                source=f"{node_id}.md",
                metadata={}
            )
        )

        node.resolution = ResolutionState(content=content)

        return node
    return _build


@pytest.fixture
def node_a():
    return ComponentNode(
        id="A",
        component=ComponentConfig(
            type="template",
            source="a.md"
        )
    )


@pytest.fixture
def node_b():
    return ComponentNode(
        id="B",
        component=ComponentConfig(
            type="template",
            source="b.md"
        )
    )


@pytest.fixture
def node_c():
    return ComponentNode(
        id="C",
        component=ComponentConfig(
            type="template",
            source="c.md"
        )
    )


@pytest.fixture
def graph():
    return RecipeGraph()