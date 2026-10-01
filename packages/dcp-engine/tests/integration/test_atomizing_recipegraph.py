


from dcp_engine.assembly.atomizer import MarkdownAtomizer
from dcp_engine.language.directives.implementations.include_directive import (
    IncludeDirectiveHandler,
)
from dcp_engine.language.syntax.markdown.atom import MarkdownDirective, MarkdownFragment
from dcp_engine.planning.graph.assets import ComponentContent
from dcp_engine.planning.graph.builder import RecipeGraphBuilder
from dcp_engine.planning.resolution.dependency_resolver import DependencyResolver
from dcp_engine.solving.inspection.implementations.markdown_inspector import (
    MarkdownInspector,
)
from dcp_engine.solving.inspection.pipeline import InspectionPipeline
from dcp_engine.solving.resolution.resolution_state import ResolutionState


def test_markdown_pipeline_atomizes_resolved_document(
    temp_workspace,
    markdown_file,
    recipe_manifest,
    planning_context,
    resource_resolver,
):
    markdown_file(
        "cover.md",
        """
# Cover

Texto

@include("annex.md")

Fim
"""
    )

    markdown_file(
        "annex.md",
        """
# Annex
"""
    )

    recipe_manifest.components[0].source = (
        temp_workspace / "cover.md"
    ).as_posix()

    graph = RecipeGraphBuilder(resource_resolver).build(
        recipe_manifest
    )

    planning_context.inspector_registry.register(
        "md",
        MarkdownInspector()
    )

    planning_context.directive_registry.register(
        IncludeDirectiveHandler()
    )

    InspectionPipeline().execute(
        graph=graph,
        inspector_registry=planning_context.inspector_registry,
    )

    for node in graph.nodes.values():
        node.resolution = ResolutionState()

    DependencyResolver().resolve(
        graph=graph,
        context=planning_context,
    )

    #
    # Simula adaptação concluída
    #

    cover = graph.find_by_source(
        (temp_workspace / "cover.md").as_posix()
    )

    cover.adapted = ComponentContent(
        markdown=cover.resolution.content
    )

    atomizer = MarkdownAtomizer()

    fragmented = atomizer.atomize(
        cover.adapted.markdown
    )

    assert len(fragmented.blocks) == 3

    assert isinstance(
        fragmented.blocks[0],
        MarkdownFragment
    )

    assert isinstance(
        fragmented.blocks[1],
        MarkdownDirective
    )

    assert isinstance(
        fragmented.blocks[2],
        MarkdownFragment
    )

    # parsed = MarkdownParser().parse(cover.adapted.body)
    # assert parsed.variables == []


