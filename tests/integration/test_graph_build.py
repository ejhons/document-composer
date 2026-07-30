from engine.frontend.manifests.recipe import ComponentConfig, RecipeManifest, StyleConfig
from engine.planning.graph.builder import RecipeGraphBuilder
from engine.planning.loaders.base import ResourceResolver


def test_manifest_should_be_converted_to_graph():
    manifest = RecipeManifest(
        recipe_name="Recipe",
        version="1.0",
        style=StyleConfig(),
        components=[
            ComponentConfig(
                type="template",
                source="a.md"
            ),
            ComponentConfig(
                type="external",
                source="b.pdf"
            ),
        ]
    )

    class DummyResolver(ResourceResolver):
        def normalize(self, source):
            return super().normalize(source)
        
        def resolve(self, component, source):
            component.source = f"/tmp/{source}"

    graph = RecipeGraphBuilder(
        DummyResolver()
    ).build(
        manifest
    )

    assert len(graph.nodes) == 2

    assert graph.find_by_source("/tmp/a.md") is not None
    assert graph.find_by_source("/tmp/b.pdf") is not None