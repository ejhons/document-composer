import pytest
from unittest.mock import MagicMock, Mock, call

from engine.common.exceptions import GraphNotSolvedException
from engine.common.models.recipe import ComponentConfig, RecipeManifest, StyleConfig
from engine.planner.graph.graph import RecipeGraph, SolvedGraph
from engine.planner.recipe_builder import RecipeGraphBuilder
from engine.planner.resources.base import ResourceResolver

def test_build_empty_manifest_returns_empty_graph():
    manifest = RecipeManifest(
        recipe_name="Recipe",
        version="1.0",
        style=StyleConfig(),
        components=[]
    )

    resolver = Mock(spec=ResourceResolver)

    graph = RecipeGraphBuilder(resolver).build(manifest)

    assert len(graph.nodes) == 0
    assert len(graph.edges) == 0


def test_build_should_resolve_every_component():
    components = [
        ComponentConfig(type="template", source="a.md"),
        ComponentConfig(type="template", source="b.md"),
    ]

    manifest = RecipeManifest(
        recipe_name="Recipe",
        version="1.0",
        style=StyleConfig(),
        components=components
    )

    resolver = Mock(spec=ResourceResolver)

    RecipeGraphBuilder(resolver).build(manifest)

    resolver.resolve.assert_has_calls([
        call(components[0], "a.md"),
        call(components[1], "b.md"),
    ])

    assert resolver.resolve.call_count == 2

def test_build_should_create_all_nodes():
    components = [
        ComponentConfig(type="template", source="a.md"),
        ComponentConfig(type="template", source="b.md"),
        ComponentConfig(type="template", source="c.md"),
    ]

    manifest = RecipeManifest(
        recipe_name="Recipe",
        version="1.0",
        style=StyleConfig(),
        components=components
    )

    resolver = Mock(spec=ResourceResolver)

    graph = RecipeGraphBuilder(resolver).build(manifest)

    assert len(graph.nodes) == 3


def test_build_should_use_normalized_source():
    component = ComponentConfig(
        type="template",
        source="relative.md"
    )

    manifest = RecipeManifest(
        recipe_name="Recipe",
        version="1.0",
        style=StyleConfig(),
        components=[component]
    )

    resolver = Mock(spec=ResourceResolver)

    def normalize(component, source):
        component.source = "/tmp/relative.md"

    resolver.resolve.side_effect = normalize

    graph = RecipeGraphBuilder(resolver).build(manifest)

    node = next(iter(graph.nodes.values()))

    assert node.component.source == "/tmp/relative.md"


def test_build_solved_should_fail_when_graph_is_not_solved(node_a, resource_resolver):
    graph = RecipeGraph()
    # Adiciona nó não solucionado.
    node_a.resolution.pending_inputs.add('B')
    graph.add_node(node_a)

    with pytest.raises(GraphNotSolvedException):
        RecipeGraphBuilder(resource_resolver).build_solved(graph)

def test_build_solved_should_return_solved_graph(resource_resolver):
    graph = Mock(spec=RecipeGraph)

    graph.solved.return_value = True
    graph.model_dump.return_value = {}

    solved = RecipeGraphBuilder(resource_resolver).build_solved(graph)

    assert isinstance(solved, SolvedGraph)